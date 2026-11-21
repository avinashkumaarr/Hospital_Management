with open('static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update version strings in app.js if any
js = js.replace('v3.0', 'v4.0')
js = js.replace('3.0.0', '4.0.0')

# 2. Hook dirty form check into showPage
old_show_page = '''function showPage(pageId) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));'''

new_show_page = '''function showPage(pageId) {
  if (typeof isConsultationFormDirty !== 'undefined' && (isConsultationFormDirty || isRegistrationFormDirty) && appState.activePage !== pageId) {
    const leave = confirm('You have unsaved changes in your form. Discard changes and navigate away?');
    if (!leave) return;
    isConsultationFormDirty = false;
    isRegistrationFormDirty = false;
  }

  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));'''

assert old_show_page in js, "Could not find showPage in app.js"
js = js.replace(old_show_page, new_show_page)

# 3. Replace loadPatientDirectory with upgraded version with pagination & filters
old_load_patients = '''async function loadPatientDirectory(searchKeyword = '') {
  try {
    const patients = await window.api.getPatients(searchKeyword);
    appState.patients = patients;
    const tbody = document.getElementById('patient-directory-tbody');
    if (!tbody) return;

    if (patients.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:2rem; color:var(--text-muted)">No patients found matching '${escapeHtml(searchKeyword)}'.</td></tr>`;
      return;
    }

    tbody.innerHTML = patients.map(p => {
      const age = new Date().getFullYear() - new Date(p.date_of_birth).getFullYear();
      return `
        <tr>
          <td><strong style="font-family:var(--font-mono); color:var(--primary)">${escapeHtml(p.masked_aadhaar || p.aadhaar_number)}</strong></td>
          <td><strong>${escapeHtml(p.full_name)}</strong></td>
          <td>${age}Y / ${escapeHtml(p.gender)}</td>
          <td><span class="badge badge-info">${escapeHtml(p.blood_group || 'O+')}</span></td>
          <td>${escapeHtml(p.mobile || '—')}</td>
          <td><span style="font-size:0.78rem; color:${p.allergies !== 'None' ? 'var(--danger)' : 'var(--text-muted)'}">${escapeHtml(p.allergies || 'None')}</span></td>
          <td>
            <button class="btn btn-secondary btn-sm" onclick="viewPatientEhr('${p.aadhaar_number}')">View EHR</button>
            <button class="btn btn-primary btn-sm" onclick="startConsultationForPatient('${p.aadhaar_number}')">Consult</button>
          </td>
        </tr>
      `;
    }).join('');
  } catch (err) {
    toast(`Failed to load patient directory: ${err.message}`, true);
  }
}'''

new_load_patients = '''let patientDirState = {
  search: '',
  gender: '',
  blood: '',
  page: 1,
  pageSize: 6
};

async function loadPatientDirectory() {
  try {
    const searchVal = document.getElementById('patient-dir-search-input')?.value || '';
    const genderVal = document.getElementById('patient-dir-gender-filter')?.value || '';
    const bloodVal = document.getElementById('patient-dir-blood-filter')?.value || '';

    patientDirState.search = searchVal.trim().toLowerCase();
    patientDirState.gender = genderVal;
    patientDirState.blood = bloodVal;

    let patients = await window.api.getPatients();
    appState.patients = patients;

    // Filter
    let filtered = patients.filter(p => {
      if (patientDirState.search) {
        const q = patientDirState.search;
        const matchName = (p.full_name || '').toLowerCase().includes(q);
        const matchAadhaar = (p.aadhaar_number || '').includes(q);
        const matchMobile = (p.mobile || '').includes(q);
        if (!matchName && !matchAadhaar && !matchMobile) return false;
      }
      if (patientDirState.gender && p.gender !== patientDirState.gender) return false;
      if (patientDirState.blood && p.blood_group !== patientDirState.blood) return false;
      return true;
    });

    const total = filtered.length;
    const totalPages = Math.max(1, Math.ceil(total / patientDirState.pageSize));
    if (patientDirState.page > totalPages) patientDirState.page = totalPages;
    if (patientDirState.page < 1) patientDirState.page = 1;

    const startIdx = (patientDirState.page - 1) * patientDirState.pageSize;
    const endIdx = Math.min(startIdx + patientDirState.pageSize, total);
    const pagePatients = filtered.slice(startIdx, endIdx);

    const tbody = document.getElementById('patient-directory-tbody');
    if (tbody) {
      if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:2rem; color:var(--text-muted)">No patients found matching the selected filters.</td></tr>`;
      } else {
        tbody.innerHTML = pagePatients.map(p => {
          const age = new Date().getFullYear() - new Date(p.date_of_birth).getFullYear();
          return `
            <tr>
              <td><strong style="font-family:var(--font-mono); color:var(--primary)">${escapeHtml(p.masked_aadhaar || p.aadhaar_number)}</strong></td>
              <td><strong>${escapeHtml(p.full_name)}</strong></td>
              <td>${age}Y / ${escapeHtml(p.gender)}</td>
              <td><span class="badge badge-info">${escapeHtml(p.blood_group || 'O+')}</span></td>
              <td>${escapeHtml(p.mobile || '—')}</td>
              <td><span style="font-size:0.78rem; color:${p.allergies !== 'None' ? 'var(--danger)' : 'var(--text-muted)'}">${escapeHtml(p.allergies || 'None')}</span></td>
              <td style="white-space:nowrap;">
                <button class="btn btn-secondary btn-sm" onclick="viewPatientEhr('${p.aadhaar_number}')">View EHR</button>
                <button class="btn btn-primary btn-sm" onclick="startConsultationForPatient('${p.aadhaar_number}')">Consult</button>
                <button class="btn btn-secondary btn-sm" onclick="openEditPatientModal('${p.aadhaar_number}')" title="Edit Demographics & Allergies">✏️ Edit</button>
              </td>
            </tr>
          `;
        }).join('');
      }
    }

    // Update pagination UI
    const pageInfo = document.getElementById('patient-dir-page-info');
    if (pageInfo) {
      pageInfo.textContent = total > 0 ? `Showing ${startIdx + 1} to ${endIdx} of ${total} patients` : 'No patients found';
    }
    const pageDisplay = document.getElementById('patient-dir-current-page');
    if (pageDisplay) {
      pageDisplay.textContent = `${patientDirState.page} / ${totalPages}`;
    }
    const prevBtn = document.getElementById('btn-patient-prev');
    if (prevBtn) prevBtn.disabled = patientDirState.page <= 1;
    const nextBtn = document.getElementById('btn-patient-next');
    if (nextBtn) nextBtn.disabled = patientDirState.page >= totalPages;

  } catch (err) {
    toast(`Failed to load patient directory: ${err.message}`, true);
  }
}

function onPatientDirFilterChange() {
  patientDirState.page = 1;
  loadPatientDirectory();
}

function resetPatientDirFilters() {
  const s = document.getElementById('patient-dir-search-input');
  if (s) s.value = '';
  const g = document.getElementById('patient-dir-gender-filter');
  if (g) g.value = '';
  const b = document.getElementById('patient-dir-blood-filter');
  if (b) b.value = '';
  patientDirState.page = 1;
  loadPatientDirectory();
}

function changePatientPage(delta) {
  patientDirState.page += delta;
  loadPatientDirectory();
}

function exportPatientsCSV() {
  const patients = appState.patients || [];
  if (patients.length === 0) {
    toast('No patient records to export.', true);
    return;
  }
  const headers = ['Aadhaar Number', 'Full Name', 'DOB', 'Gender', 'Blood Group', 'Mobile', 'Email', 'Address', 'Allergies', 'Chronic Conditions'];
  const rows = patients.map(p => [
    `"${p.aadhaar_number}"`,
    `"${(p.full_name || '').replace(/"/g, '""')}"`,
    `"${p.date_of_birth}"`,
    `"${p.gender}"`,
    `"${p.blood_group}"`,
    `"${p.mobile}"`,
    `"${(p.email || '').replace(/"/g, '""')}"`,
    `"${(p.address || '').replace(/"/g, '""')}"`,
    `"${(p.allergies || '').replace(/"/g, '""')}"`,
    `"${(p.chronic_conditions || '').replace(/"/g, '""')}"`
  ]);
  const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(r => r.join(','))].join('\\n');
  const encodedUri = encodeURI(csvContent);
  const link = document.createElement('a');
  link.setAttribute('href', encodedUri);
  link.setAttribute('download', `medilink_patients_${new Date().toISOString().slice(0, 10)}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  toast('Patient directory exported to CSV.');
}'''

assert old_load_patients in js, "Could not find old_load_patients in app.js"
js = js.replace(old_load_patients, new_load_patients)

# 4. Append Edit Patient Modal, Global Search, and Dirty Form guards to end of app.js
additions = '''

// ==========================================================================
// MEDILINK ENTERPRISE v4.0 — NEW CLINICAL MODULES & UX ENHANCEMENTS
// ==========================================================================

// --- Edit Patient Demographic & Clinical Details ---
async function openEditPatientModal(aadhaar) {
  let patient = (appState.patients || []).find(p => p.aadhaar_number === aadhaar);
  if (!patient) {
    try {
      patient = await window.api.getPatient(aadhaar);
    } catch (e) {
      toast('Failed to load patient: ' + e.message, true);
      return;
    }
  }
  if (!patient) return;

  document.getElementById('edit-pat-aadhaar').value = patient.aadhaar_number;
  document.getElementById('edit-pat-name-display').textContent = patient.full_name;
  document.getElementById('edit-pat-aadhaar-display').textContent = maskAadhaar(patient.aadhaar_number);
  document.getElementById('edit-pat-phone').value = patient.mobile || '';
  document.getElementById('edit-pat-email').value = patient.email || '';
  document.getElementById('edit-pat-address').value = patient.address || '';
  document.getElementById('edit-pat-allergies').value = patient.allergies || 'None';
  document.getElementById('edit-pat-chronic').value = patient.chronic_conditions || 'None';
  document.getElementById('edit-pat-em-name').value = patient.emergency_contact_name || '';
  document.getElementById('edit-pat-em-phone').value = patient.emergency_contact_phone || '';

  openModal('modal-edit-patient');
}

async function submitEditPatient(event) {
  if (event) event.preventDefault();
  const aadhaar = document.getElementById('edit-pat-aadhaar').value;
  if (!aadhaar) return;

  const payload = {
    mobile: document.getElementById('edit-pat-phone').value.trim(),
    email: document.getElementById('edit-pat-email').value.trim(),
    address: document.getElementById('edit-pat-address').value.trim(),
    allergies: document.getElementById('edit-pat-allergies').value.trim(),
    chronic_conditions: document.getElementById('edit-pat-chronic').value.trim(),
    emergency_contact_name: document.getElementById('edit-pat-em-name').value.trim(),
    emergency_contact_phone: document.getElementById('edit-pat-em-phone').value.trim()
  };

  const btn = document.getElementById('btn-save-patient-edit');
  if (btn) { btn.disabled = true; btn.textContent = 'Saving...'; }

  try {
    await window.api.updatePatient(aadhaar, payload);
    toast('Patient demographic & clinical record updated successfully!');
    closeModal('modal-edit-patient');
    await loadPatientDirectory();
    if (appState.currentPatient && appState.currentPatient.aadhaar_number === aadhaar) {
      await viewPatientEhr(aadhaar);
    }
  } catch (err) {
    toast(`Failed to update patient: ${err.message}`, true);
  } finally {
    if (btn) { btn.disabled = false; btn.textContent = '💾 Save Patient Details'; }
  }
}

// --- Global Search Command Palette (Ctrl+K) ---
let paletteFilter = 'all';
let paletteResults = [];
let paletteActiveIndex = -1;

function openGlobalSearch() {
  openModal('modal-global-search');
  const input = document.getElementById('global-search-palette-input');
  if (input) {
    input.value = '';
    input.focus();
  }
  setPaletteFilter('all', document.getElementById('palette-filter-all'));
  handlePaletteSearch('');
}

function closeGlobalSearch() {
  closeModal('modal-global-search');
}

function handleGlobalSearchKey(event) {
  if (event.key === 'Enter') {
    openGlobalSearch();
  }
}

function setPaletteFilter(filterType, btn) {
  paletteFilter = filterType;
  document.querySelectorAll('.palette-chip').forEach(c => c.classList.remove('active'));
  if (btn) btn.classList.add('active');
  const query = document.getElementById('global-search-palette-input')?.value || '';
  handlePaletteSearch(query);
}

const APP_NAVIGATION_ITEMS = [
  { id: 'page-home', title: 'Command Center Dashboard', icon: '📊', sub: 'Real-time KPIs, bed census & patient metrics' },
  { id: 'page-patients', title: 'Unified Patient Directory', icon: '👥', sub: 'Citizen records, demographics & contact list' },
  { id: 'page-search', title: 'Unified EHR Patient Viewer', icon: '📋', sub: 'Longitudinal clinical history & encounter timeline' },
  { id: 'page-register', title: 'Enroll New Patient', icon: '➕', sub: 'Register citizen with 12-digit Aadhaar UID' },
  { id: 'page-encounter', title: 'Doctor Clinical Consultation', icon: '🩺', sub: 'Chief complaint, vitals, ICD-10 diagnosis & Rx' },
  { id: 'page-appointments', title: 'Appointment Scheduling', icon: '📅', sub: 'OPD booking, conflict detection & calendar' },
  { id: 'page-doctors', title: 'Doctor Roster & Availability', icon: '👨‍⚕️', sub: 'Active clinical staff, specialties & wards' },
  { id: 'page-beds', title: 'Inpatient Beds & Wards', icon: '🛏️', sub: 'Bed occupancy matrix, admissions & transfers' },
  { id: 'page-queue', title: 'OPD Live Queue Board', icon: '🎫', sub: 'Token generation, live call & consultations' },
  { id: 'page-labs', title: 'Diagnostic Laboratory Reports', icon: '🧪', sub: 'Attach, review & download clinical pathology reports' },
  { id: 'page-triage', title: 'Emergency Trauma Triage (ESI 1-5)', icon: '🚨', sub: 'ESI triage algorithm & Break-Glass protocol' },
  { id: 'page-analytics', title: 'Hospital Intelligence & Analytics', icon: '📈', sub: 'Department volume, trends & CSV exports' },
  { id: 'page-audit', title: 'Security Access Audit Logs', icon: '🛡️', sub: 'HIPAA/ABDM immutable compliance audit trails' },
  { id: 'page-sql', title: 'SQL DBMS Query Workbench', icon: '💾', sub: 'Course evaluation queries & schema workbench' },
  { id: 'page-backup', title: 'Database Engine & Health', icon: '⚙️', sub: 'Engine failover, JSON backup & health diagnostics' },
  { id: 'page-profile', title: 'My Staff Profile & Settings', icon: '👤', sub: 'Account info, password change & preferences' }
];

async function handlePaletteSearch(query = '') {
  const container = document.getElementById('global-search-palette-results');
  if (!container) return;
  const q = query.trim().toLowerCase();

  paletteResults = [];

  // 1. Pages
  if (paletteFilter === 'all' || paletteFilter === 'pages') {
    const matchedPages = APP_NAVIGATION_ITEMS.filter(item => {
      if (!q) return true;
      return item.title.toLowerCase().includes(q) || item.sub.toLowerCase().includes(q);
    }).slice(0, q ? 6 : 4);

    matchedPages.forEach(p => {
      paletteResults.push({
        type: 'page',
        id: p.id,
        title: p.title,
        icon: p.icon,
        sub: p.sub,
        actionText: 'Go to page'
      });
    });
  }

  // 2. Patients
  if (paletteFilter === 'all' || paletteFilter === 'patients') {
    let patients = appState.patients || [];
    if (patients.length === 0) {
      try {
        patients = await window.api.getPatients();
        appState.patients = patients;
      } catch (e) {}
    }
    const matchedPatients = patients.filter(p => {
      if (!q) return true;
      return (p.full_name || '').toLowerCase().includes(q) ||
             (p.aadhaar_number || '').includes(q) ||
             (p.mobile || '').includes(q);
    }).slice(0, 5);

    matchedPatients.forEach(p => {
      paletteResults.push({
        type: 'patient',
        id: p.aadhaar_number,
        title: `${p.full_name} (${p.blood_group || 'O+'})`,
        icon: '👤',
        sub: `Aadhaar: ${p.masked_aadhaar || maskAadhaar(p.aadhaar_number)} • Phone: ${p.mobile || '—'}`,
        actionText: 'Open EHR'
      });
    });
  }

  // 3. Doctors
  if (paletteFilter === 'all' || paletteFilter === 'doctors') {
    let doctors = appState.doctors || [];
    if (doctors.length === 0) {
      try {
        doctors = await window.api.getDoctors();
        appState.doctors = doctors;
      } catch (e) {}
    }
    const matchedDoctors = doctors.filter(d => {
      if (!q) return true;
      return (d.doctor_name || '').toLowerCase().includes(q) ||
             (d.specialization || '').toLowerCase().includes(q) ||
             (d.department || '').toLowerCase().includes(q);
    }).slice(0, 4);

    matchedDoctors.forEach(d => {
      paletteResults.push({
        type: 'doctor',
        id: d.doctor_id,
        title: d.doctor_name,
        icon: '🩺',
        sub: `${d.specialization} • Dept: ${d.department} • Status: ${d.availability_status}`,
        actionText: 'View Doctor'
      });
    });
  }

  paletteActiveIndex = paletteResults.length > 0 ? 0 : -1;

  if (paletteResults.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding: 2.5rem 1rem; color:var(--text-muted); font-size:0.88rem;">
        No results found matching "<strong>${escapeHtml(query)}</strong>"
      </div>
    `;
    return;
  }

  container.innerHTML = paletteResults.map((r, idx) => `
    <div class="palette-result-item ${idx === 0 ? 'active' : ''}" data-idx="${idx}" onclick="selectPaletteItem(${idx})">
      <div class="palette-item-left">
        <div class="palette-item-icon">${r.icon}</div>
        <div class="palette-item-info">
          <div class="palette-item-title">${escapeHtml(r.title)}</div>
          <div class="palette-item-sub">${escapeHtml(r.sub)}</div>
        </div>
      </div>
      <div class="palette-item-action">
        <span>${r.actionText}</span>
        <span>↵</span>
      </div>
    </div>
  `).join('');
}

function selectPaletteItem(index) {
  const item = paletteResults[index];
  if (!item) return;

  closeGlobalSearch();

  if (item.type === 'page') {
    showPage(item.id);
  } else if (item.type === 'patient') {
    viewPatientEhr(item.id);
  } else if (item.type === 'doctor') {
    showPage('page-doctors');
  }
}

function handlePaletteKeydown(e) {
  if (e.key === 'ArrowDown') {
    e.preventDefault();
    if (paletteResults.length === 0) return;
    paletteActiveIndex = (paletteActiveIndex + 1) % paletteResults.length;
    updatePaletteActiveItem();
  } else if (e.key === 'ArrowUp') {
    e.preventDefault();
    if (paletteResults.length === 0) return;
    paletteActiveIndex = (paletteActiveIndex - 1 + paletteResults.length) % paletteResults.length;
    updatePaletteActiveItem();
  } else if (e.key === 'Enter') {
    e.preventDefault();
    if (paletteActiveIndex >= 0 && paletteActiveIndex < paletteResults.length) {
      selectPaletteItem(paletteActiveIndex);
    }
  } else if (e.key === 'Escape') {
    closeGlobalSearch();
  }
}

function updatePaletteActiveItem() {
  const items = document.querySelectorAll('.palette-result-item');
  items.forEach((el, idx) => {
    if (idx === paletteActiveIndex) {
      el.classList.add('active');
      el.scrollIntoView({ block: 'nearest' });
    } else {
      el.classList.remove('active');
    }
  });
}

// Global Keyboard Shortcut: Ctrl+K or Cmd+K
window.addEventListener('keydown', (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
    e.preventDefault();
    openGlobalSearch();
  }
});

// --- Dirty Form Unsaved Changes Guard ---
let isConsultationFormDirty = false;
let isRegistrationFormDirty = false;

function initDirtyFormGuards() {
  const encForm = document.getElementById('form-encounter');
  if (encForm) {
    encForm.addEventListener('input', () => { isConsultationFormDirty = true; });
    encForm.addEventListener('submit', () => { isConsultationFormDirty = false; });
  }
  const regForm = document.getElementById('form-register');
  if (regForm) {
    regForm.addEventListener('input', () => { isRegistrationFormDirty = true; });
    regForm.addEventListener('submit', () => { isRegistrationFormDirty = false; });
  }
}

window.addEventListener('beforeunload', (e) => {
  if (isConsultationFormDirty || isRegistrationFormDirty) {
    e.preventDefault();
    e.returnValue = 'You have unsaved changes in your form. Are you sure you want to leave?';
    return e.returnValue;
  }
});

// Hook dirty form guards into initialization
document.addEventListener('DOMContentLoaded', () => {
  initDirtyFormGuards();
});
'''

new_js = js + additions

with open('static/js/app.js', 'w', encoding='utf-8') as f:
    f.write(new_js)

print("Updated static/js/app.js successfully! New length:", len(new_js))
