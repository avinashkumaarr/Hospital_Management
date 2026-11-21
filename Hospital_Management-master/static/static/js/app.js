/**
 * MediLink Enterprise — Application Controller & UI Logic
 * Interoperable Healthcare Management & EMR Client.
 */

// Global State
const appState = {
  activePage: 'page-home',
  currentUser: {
    username: 'admin',
    role: 'Administrator',
    full_name: 'System Administrator'
  },
  currentFacilityId: 1,
  facilities: [],
  doctors: [],
  patients: [],
  currentPatient: null,
  activeEncounterRecord: null,
  notifications: [],
  charts: {
    deptVolume: null,
    hospitalVolume: null,
    vitalsTrend: null
  }
};

// ==========================================================================
// UTILITY FUNCTIONS
// ==========================================================================

function escapeHtml(str) {
  if (str === null || str === undefined) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function maskAadhaar(aadhaar) {
  if (!aadhaar) return 'XXXX-XXXX-XXXX';
  const clean = String(aadhaar).replace(/\D/g, '');
  if (clean.length >= 4) {
    return `XXXX-XXXX-${clean.slice(-4)}`;
  }
  return 'XXXX-XXXX-XXXX';
}

function formatAadhaarInput(el) {
  let val = el.value.replace(/\D/g, '').substring(0, 12);
  let formatted = '';
  for (let i = 0; i < val.length; i++) {
    if (i > 0 && i % 4 === 0) formatted += ' ';
    formatted += val[i];
  }
  el.value = formatted;
}

function toast(message, isDanger = false) {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const t = document.createElement('div');
  t.className = `toast ${isDanger ? 'danger' : ''}`;
  t.innerHTML = `<span>${isDanger ? '⚠️' : '✅'}</span> <span>${escapeHtml(message)}</span>`;
  container.appendChild(t);
  setTimeout(() => {
    t.style.opacity = '0';
    t.style.transform = 'translateY(8px)';
    setTimeout(() => t.remove(), 250);
  }, 3500);
}

function openModal(modalId) {
  const m = document.getElementById(modalId);
  if (m) m.classList.add('active');
}

function closeModal(modalId) {
  const m = document.getElementById(modalId);
  if (m) m.classList.remove('active');
}

// ==========================================================================
// NAVIGATION & THEME
// ==========================================================================

function showPage(pageId) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  const target = document.getElementById(pageId);
  if (target) {
    target.classList.add('active');
    appState.activePage = pageId;
  }

  // Update sidebar active link
  document.querySelectorAll('.nav-link').forEach(l => {
    l.classList.remove('active');
    if (l.getAttribute('data-page') === pageId) {
      l.classList.add('active');
    }
  });

  // Update breadcrumb
  const pageTitles = {
    'page-home': 'Command Dashboard',
    'page-patients': 'Patient Directory',
    'page-search': 'Unified EHR Patient Viewer',
    'page-register': 'Patient Registration',
    'page-encounter': 'Doctor Clinical Consultation',
    'page-appointments': 'Appointment Scheduling',
    'page-doctors': 'Doctor Availability',
    'page-beds': 'Ward & Bed Management',
    'page-queue': 'OPD Live Token Queue',
    'page-labs': 'Digital Lab Reports',
    'page-triage': 'Emergency Trauma Triage (ESI 1-5)',
    'page-analytics': 'Hospital Network Analytics',
    'page-audit': 'Security Access Audit Logs',
    'page-sql': 'SQL DBMS Query Workbench',
    'page-backup': 'Database Engine & Health'
  };
  const title = pageTitles[pageId] || 'Hospital Management';
  const crumb = document.getElementById('breadcrumb-current');
  if (crumb) crumb.textContent = title;

  // Trigger page-specific data refreshes
  if (pageId === 'page-home') loadDashboard();
  if (pageId === 'page-patients') loadPatientDirectory();
  if (pageId === 'page-beds') loadBedMatrix();
  if (pageId === 'page-queue') loadOpdQueue();
  if (pageId === 'page-appointments') loadAppointments();
  if (pageId === 'page-doctors') loadDoctors();
  if (pageId === 'page-labs') loadAllLabs();
  if (pageId === 'page-audit') loadAuditLogs();
  if (pageId === 'page-sql') loadSqlWorkbench();
  if (pageId === 'page-backup') loadBackupStatus();
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme') || 'light';
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('medilink_theme', next);
  toast(`Switched to ${next === 'dark' ? 'Night Shift Clinical' : 'Clinical Light'} mode`);
}

function initTheme() {
  const saved = localStorage.getItem('medilink_theme') || 'light';
  document.documentElement.setAttribute('data-theme', saved);
}

function toggleSidebar() {
  const sidebar = document.getElementById('app-sidebar');
  if (sidebar) sidebar.classList.toggle('open');
}

// ==========================================================================
// AUTHENTICATION & ROLE SWITCHING (Phase 4 Bug 6)
// ==========================================================================

async function initAuth() {
  try {
    const roles = await window.api.getRoles();
    const roleSelect = document.getElementById('active-role-select');
    if (roleSelect && roles) {
      roleSelect.innerHTML = roles.map(r => 
        `<option value="${r.username}">${r.role} (${r.username})</option>`
      ).join('');
    }

    // Attempt default login as admin
    await switchRoleUser('admin', 'admin123');
  } catch (err) {
    console.warn('Auth init fallback:', err);
  }
}

async function switchRoleUser(username, password) {
  try {
    const creds = {
      'admin': 'admin123',
      'doctor': 'doctor123',
      'receptionist': 'reception123',
      'emergency': 'emergency123'
    };
    const pwd = password || creds[username] || 'admin123';
    const authData = await window.api.login(username, pwd);
    appState.currentUser = authData;

    const label = document.getElementById('user-role-label');
    const nameLabel = document.getElementById('user-name-label');
    if (label) label.textContent = authData.role;
    if (nameLabel) nameLabel.textContent = authData.full_name;

    // Apply role view constraints
    applyRolePermissions(authData.role);
    toast(`Authenticated as ${authData.role} (${authData.full_name})`);
    loadDashboard();
  } catch (err) {
    toast(`Authentication error: ${err.message}`, true);
  }
}

function applyRolePermissions(role) {
  // Doctor highlights consultations, Receptionist highlights registration/appointments, Emergency highlights triage/beds
  const encounterLink = document.querySelector('.nav-link[data-page="page-encounter"]');
  const triageLink = document.querySelector('.nav-link[data-page="page-triage"]');
  const auditLink = document.querySelector('.nav-link[data-page="page-audit"]');
  const sqlLink = document.querySelector('.nav-link[data-page="page-sql"]');

  if (role === 'Receptionist') {
    if (sqlLink) sqlLink.style.display = 'none';
    if (auditLink) auditLink.style.display = 'none';
  } else {
    if (sqlLink) sqlLink.style.display = 'flex';
    if (auditLink) auditLink.style.display = 'flex';
  }
}

// ==========================================================================
// DASHBOARD & ANALYTICS
// ==========================================================================

async function loadDashboard() {
  try {
    const stats = await window.api.getDashboardStats(appState.currentFacilityId);
    
    document.getElementById('dash-stat-patients').textContent = stats.total_patients;
    document.getElementById('dash-stat-records').textContent = stats.total_records;
    document.getElementById('dash-stat-beds').textContent = `${stats.occupied_beds}/${stats.total_beds} (${stats.bed_occupancy_percent}%)`;
    document.getElementById('dash-stat-queue').textContent = stats.waiting_queue_count;
    document.getElementById('dash-stat-appts').textContent = stats.scheduled_appointments;
    document.getElementById('dash-stat-emergency').textContent = stats.recent_emergency_count;

    // Update sidebar navigation badges
    const patBadge = document.getElementById('badge-patients');
    if (patBadge) patBadge.textContent = stats.total_patients;
    const bedBadge = document.getElementById('badge-beds');
    if (bedBadge) bedBadge.textContent = `${stats.occupied_beds}/${stats.total_beds}`;
    const queueBadge = document.getElementById('badge-queue');
    if (queueBadge) queueBadge.textContent = stats.waiting_queue_count;
    const apptBadge = document.getElementById('badge-appts');
    if (apptBadge) apptBadge.textContent = stats.scheduled_appointments;

    // Render Recent Encounters table
    const records = await window.api.getRecords({ limit: 6 });
    const tbody = document.getElementById('dash-recent-tbody');
    if (tbody) {
      if (records.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding:1.5rem; color:var(--text-muted)">No recent clinical records.</td></tr>`;
      } else {
        tbody.innerHTML = records.map(r => `
          <tr>
            <td><strong style="color:var(--primary)">REC-${String(r.record_id).padStart(4, '0')}</strong></td>
            <td>${escapeHtml(r.visit_date)}</td>
            <td><span class="badge ${r.visit_type === 'Emergency' ? 'badge-danger' : 'badge-primary'}">${escapeHtml(r.visit_type)}</span></td>
            <td><strong>${escapeHtml(r.diagnosis)}</strong></td>
            <td>${escapeHtml(r.hospital_name)}</td>
            <td>${escapeHtml(r.doctor_name || 'Physician')}</td>
          </tr>
        `).join('');
      }
    }

    // Load Charts
    loadDashboardCharts();
  } catch (err) {
    console.error('Failed to load dashboard stats:', err);
  }
}

async function loadDashboardCharts() {
  if (typeof Chart === 'undefined') return;

  try {
    const deptData = await window.api.getDepartmentVolume();
    const hospData = await window.api.getHospitalVolume();

    // 1. Department Volume Chart
    const ctxDept = document.getElementById('chart-dept-volume');
    if (ctxDept) {
      if (appState.charts.deptVolume) appState.charts.deptVolume.destroy();
      appState.charts.deptVolume = new Chart(ctxDept, {
        type: 'doughnut',
        data: {
          labels: deptData.labels,
          datasets: [{
            data: deptData.data,
            backgroundColor: ['#004b87', '#0d9488', '#f59e0b', '#dc2626', '#8b5cf6', '#06b6d4'],
            borderWidth: 2,
            borderColor: 'var(--surface)'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11 } } }
          }
        }
      });
    }

    // 2. Hospital Volume Chart
    const ctxHosp = document.getElementById('chart-hosp-volume');
    if (ctxHosp) {
      if (appState.charts.hospitalVolume) appState.charts.hospitalVolume.destroy();
      appState.charts.hospitalVolume = new Chart(ctxHosp, {
        type: 'bar',
        data: {
          labels: hospData.labels,
          datasets: [{
            label: 'Consultation Volume',
            data: hospData.data,
            backgroundColor: '#004b87',
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: { beginAtZero: true, grid: { color: 'rgba(0,0,0,0.06)' } },
            x: { grid: { display: false } }
          },
          plugins: {
            legend: { display: false }
          }
        }
      });
    }
  } catch (err) {
    console.error('Error rendering dashboard charts:', err);
  }
}

// ==========================================================================
// PATIENT DIRECTORY & REGISTRATION (Phase 4 Bug 7)
// ==========================================================================

async function loadPatientDirectory(searchKeyword = '') {
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
}

async function submitPatientRegistration(event) {
  if (event) event.preventDefault();

  const aadhaar = document.getElementById('reg-aadhaar').value.trim();
  const name = document.getElementById('reg-name').value.trim();
  const dob = document.getElementById('reg-dob').value;
  const gender = document.getElementById('reg-gender').value;
  const blood = document.getElementById('reg-blood').value;
  const mobile = document.getElementById('reg-mobile').value.trim();
  const email = document.getElementById('reg-email').value.trim();
  const address = document.getElementById('reg-address').value.trim();
  const allergies = document.getElementById('reg-allergies').value.trim();
  const chronic = document.getElementById('reg-chronic').value.trim();
  const emergency = document.getElementById('reg-emergency').value.trim();

  // Strict Validation (Bug 7)
  const cleanAadhaar = aadhaar.replace(/\D/g, '');
  if (cleanAadhaar.length !== 12) {
    toast('Aadhaar must be exactly 12 digits.', true);
    return;
  }
  if (!name) {
    toast('Please enter full legal name.', true);
    return;
  }
  if (!dob || new Date(dob) > new Date()) {
    toast('Please enter a valid date of birth (not in the future).', true);
    return;
  }

  const patientPayload = {
    aadhaar_number: cleanAadhaar,
    full_name: name,
    date_of_birth: dob,
    gender: gender,
    blood_group: blood,
    mobile: mobile || null,
    email: email || null,
    address: address || null,
    allergies: allergies || 'None',
    chronic_conditions: chronic || 'None',
    emergency_contact: emergency || null
  };

  try {
    const created = await window.api.registerPatient(patientPayload);
    toast(`Patient ${created.full_name} enrolled successfully!`);
    document.getElementById('patient-enroll-form').reset();
    viewPatientEhr(created.aadhaar_number);
  } catch (err) {
    toast(`Registration failed: ${err.message}`, true);
  }
}

// ==========================================================================
// UNIFIED EHR PATIENT VIEWER (Phase 4 Bugs 1 & 3)
// ==========================================================================

async function viewPatientEhr(aadhaarStr) {
  try {
    const patient = await window.api.getPatient(aadhaarStr);
    appState.currentPatient = patient;

    // Show EHR container
    document.getElementById('ehr-search-input').value = patient.aadhaar_number;
    document.getElementById('ehr-result-container').style.display = 'block';
    document.getElementById('ehr-no-result').style.display = 'none';

    renderPatientBanner(patient);
    renderEhrTimeline(patient);
    renderVitalsSection(patient);
    renderLabsSection(patient);
    renderAbhaCard(patient);

    showPage('page-search');
  } catch (err) {
    document.getElementById('ehr-result-container').style.display = 'none';
    document.getElementById('ehr-no-result').style.display = 'block';
    toast(`Patient record lookup failed: ${err.message}`, true);
  }
}

function renderPatientBanner(p) {
  const banner = document.getElementById('patient-banner');
  if (!banner) return;

  const age = new Date().getFullYear() - new Date(p.date_of_birth).getFullYear();
  const initials = p.full_name.split(' ').map(w => w[0]).join('').substring(0, 2).toUpperCase();

  banner.innerHTML = `
    <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:1rem;">
      <div style="display:flex; gap:1rem; align-items:center;">
        <div style="width:52px; height:52px; border-radius:var(--radius-full); background:var(--primary); color:#fff; display:flex; align-items:center; justify-content:center; font-size:1.3rem; font-weight:800; font-family:var(--font-heading)">
          ${escapeHtml(initials)}
        </div>
        <div>
          <div style="display:flex; align-items:center; gap:0.65rem;">
            <h2 style="font-size:1.25rem; font-weight:800; font-family:var(--font-heading)">${escapeHtml(p.full_name)}</h2>
            <span class="badge badge-primary">ABHA Active</span>
          </div>
          <div style="font-size:0.82rem; color:var(--text-muted); margin-top:2px; display:flex; gap:0.85rem; flex-wrap:wrap;">
            <span>UID: <strong style="font-family:var(--font-mono); color:var(--primary)">${escapeHtml(p.masked_aadhaar || p.aadhaar_number)}</strong></span>
            <span>DOB: <strong>${escapeHtml(p.date_of_birth)} (${age}Y)</strong></span>
            <span>Gender: <strong>${escapeHtml(p.gender)}</strong></span>
            <span>Blood: <strong style="color:var(--danger)">${escapeHtml(p.blood_group || 'O+')}</strong></span>
            <span>Phone: <strong>${escapeHtml(p.mobile || '—')}</strong></span>
          </div>
        </div>
      </div>
      <div style="display:flex; gap:0.5rem; align-items:center;">
        <button class="btn btn-danger btn-sm" onclick="triggerBreakGlassModal()">🚨 Break-Glass Override</button>
        <button class="btn btn-primary btn-sm" onclick="startConsultationForPatient('${p.aadhaar_number}')">➕ New Visit</button>
      </div>
    </div>
    <div style="margin-top:0.85rem; padding-top:0.65rem; border-top:1px solid var(--border-light); display:flex; gap:1.25rem; flex-wrap:wrap; font-size:0.8rem;">
      <div>Allergies: <span style="font-weight:700; color:${p.allergies !== 'None' ? 'var(--danger)' : 'var(--success)'}">${escapeHtml(p.allergies || 'None documented')}</span></div>
      <div>Chronic: <span style="font-weight:600; color:var(--text)">${escapeHtml(p.chronic_conditions || 'None')}</span></div>
      <div>Emergency Contact: <span style="color:var(--text-muted)">${escapeHtml(p.emergency_contact || 'None')}</span></div>
    </div>
  `;

  // Subtab count badges
  const encBadge = document.getElementById('subtab-encounter-count');
  if (encBadge) encBadge.textContent = p.records ? p.records.length : 0;
  const labBadge = document.getElementById('subtab-labs-count');
  if (labBadge) labBadge.textContent = p.lab_reports ? p.lab_reports.length : 0;
}

// Subtab switcher
function switchEhrSubTab(tabName) {
  ['timeline', 'vitals', 'labs', 'abha'].forEach(t => {
    const el = document.getElementById(`ehr-tab-${t}`);
    const btn = document.getElementById(`tab-btn-${t}`);
    if (el) el.style.display = (t === tabName) ? 'block' : 'none';
    if (btn) {
      if (t === tabName) btn.classList.add('active');
      else btn.classList.remove('active');
    }
  });
}

// Phase 4 Bug 1: Patient Medical Timeline Filter & Prescription Slip ID
function renderEhrTimeline(patient) {
  const p = patient || appState.currentPatient;
  if (!p) return;

  const list = document.getElementById('patient-timeline-list');
  const filterType = document.getElementById('timeline-filter-type')?.value || 'ALL';

  let records = p.records || [];
  if (filterType !== 'ALL') {
    records = records.filter(r => r.visit_type === filterType);
  }

  if (records.length === 0) {
    list.innerHTML = `<div style="color:var(--text-muted); padding:2rem 0; text-align:center;">No encounter records match filter '${escapeHtml(filterType)}'.</div>`;
    return;
  }

  // Uses r.record_id directly! (Fixes Bug 1)
  list.innerHTML = records.map(r => {
    const isEmergency = r.visit_type === 'Emergency';
    const isSurgery = r.visit_type === 'Surgery';
    const bulletClass = isEmergency ? 'danger' : (isSurgery ? 'warning' : '');

    return `
      <div class="timeline-node">
        <div class="timeline-bullet ${bulletClass}"></div>
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:6px; flex-wrap:wrap; gap:8px;">
          <div>
            <div style="font-family:var(--font-heading); font-size:1.05rem; font-weight:700;">${escapeHtml(r.diagnosis)}</div>
            <div style="display:flex; align-items:center; gap:8px; font-size:0.78rem; color:var(--text-muted); margin-top:2px; flex-wrap:wrap;">
              <span>🏥 <strong>${escapeHtml(r.hospital_name || 'Hospital')}</strong></span>
              <span>👨‍⚕️ ${escapeHtml(r.doctor_name || 'Physician')}</span>
              <span>🏷️ ${escapeHtml(r.department || 'General')}</span>
              <span class="badge ${isEmergency ? 'badge-danger' : (isSurgery ? 'badge-warning' : 'badge-primary')}">${escapeHtml(r.visit_type)}</span>
              ${r.icd10_code ? `<span class="badge" style="background:var(--bg-alt); color:var(--text)">ICD-10: ${escapeHtml(r.icd10_code)}</span>` : ''}
            </div>
          </div>
          <div style="text-align:right;">
            <div style="font-weight:700; font-size:0.82rem;">${escapeHtml(r.visit_date)}</div>
            <button class="btn btn-secondary btn-sm" style="margin-top:4px;" onclick="openPrescriptionSlipByRecordId(${r.record_id})">🖨️ Print Slip</button>
          </div>
        </div>

        ${r.vitals_summary ? `<div style="background:var(--bg-alt); padding:5px 8px; border-radius:4px; font-size:0.76rem; font-family:var(--font-mono); color:var(--primary); margin-bottom:6px;">Vitals: ${escapeHtml(r.vitals_summary)}</div>` : ''}

        ${r.notes ? `<div style="font-size:0.82rem; color:var(--text-muted); margin-bottom:6px; line-height:1.45;">${escapeHtml(r.notes)}</div>` : ''}

        ${r.prescription ? `
          <div style="background:var(--bg-alt); border-left:3px solid var(--primary); padding:6px 10px; font-family:var(--font-mono); font-size:0.8rem; white-space:pre-wrap; margin-top:6px;">
            <div style="font-weight:700; font-size:0.7rem; text-transform:uppercase; color:var(--primary); margin-bottom:2px;">Rx Prescribed:</div>${escapeHtml(r.prescription)}
          </div>
        ` : ''}

        ${r.follow_up_date ? `<div style="font-size:0.75rem; color:var(--warning); margin-top:6px; font-weight:600;">📅 Follow-up: ${escapeHtml(r.follow_up_date)}</div>` : ''}
      </div>
    `;
  }).join('');
}

// Phase 4 Bug 3: Accurate Patient Vitals (Derived strictly from real encounters)
function renderVitalsSection(p) {
  const container = document.getElementById('vitals-summary-cards');
  if (!container) return;

  const records = p.records || [];
  let latestVitals = null;
  for (const r of records) {
    if (r.vitals_summary && r.vitals_summary.trim()) {
      latestVitals = r.vitals_summary;
      break;
    }
  }

  let bpVal = 'Not recorded';
  let hrVal = 'Not recorded';
  let spo2Val = 'Not recorded';
  let tempVal = 'Not recorded';

  if (latestVitals) {
    const bpMatch = latestVitals.match(/(\d{2,3}\/\d{2,3})/);
    if (bpMatch) bpVal = `${bpMatch[1]} mmHg`;

    const hrMatch = latestVitals.match(/HR[:\s]+(\d{2,3})/i);
    if (hrMatch) hrVal = `${hrMatch[1]} bpm`;

    const spo2Match = latestVitals.match(/SpO2[:\s]+(\d{2,3})%?/i);
    if (spo2Match) spo2Val = `${spo2Match[1]}%`;

    const tempMatch = latestVitals.match(/Temp[:\s]+([0-9\.]+°?[CF]?)/i);
    if (tempMatch) tempVal = tempMatch[1];
  }

  container.innerHTML = `
    <div class="vital-item">
      <div class="vital-item-title">Blood Pressure</div>
      <div class="vital-item-val" style="color:${bpVal !== 'Not recorded' ? 'var(--primary)' : 'var(--text-dim)'}">${escapeHtml(bpVal)}</div>
      <div style="font-size:0.72rem; color:var(--text-muted); margin-top:3px;">${latestVitals ? 'From latest encounter' : 'No recorded measurement'}</div>
    </div>
    <div class="vital-item">
      <div class="vital-item-title">Heart Rate</div>
      <div class="vital-item-val" style="color:${hrVal !== 'Not recorded' ? 'var(--success)' : 'var(--text-dim)'}">${escapeHtml(hrVal)}</div>
      <div style="font-size:0.72rem; color:var(--text-muted); margin-top:3px;">${hrVal !== 'Not recorded' ? 'Resting pulse' : 'Not recorded'}</div>
    </div>
    <div class="vital-item">
      <div class="vital-item-title">Oxygen SpO2</div>
      <div class="vital-item-val" style="color:${spo2Val !== 'Not recorded' ? 'var(--info)' : 'var(--text-dim)'}">${escapeHtml(spo2Val)}</div>
      <div style="font-size:0.72rem; color:var(--text-muted); margin-top:3px;">${spo2Val !== 'Not recorded' ? 'Pulse Oximetry' : 'Not recorded'}</div>
    </div>
    <div class="vital-item">
      <div class="vital-item-title">Body Temp</div>
      <div class="vital-item-val" style="color:${tempVal !== 'Not recorded' ? 'var(--warning)' : 'var(--text-dim)'}">${escapeHtml(tempVal)}</div>
      <div style="font-size:0.72rem; color:var(--text-muted); margin-top:3px;">${tempVal !== 'Not recorded' ? 'Oral / Tympanic' : 'Not recorded'}</div>
    </div>
  `;

  // Render Vitals Chart
  renderVitalsChart(records);
}

function renderVitalsChart(records) {
  const ctx = document.getElementById('vitalsChart');
  if (!ctx || typeof Chart === 'undefined') return;

  const validRecords = (records || []).filter(r => r.vitals_summary && r.vitals_summary.match(/\d{2,3}\/\d{2,3}/)).reverse();

  const dates = validRecords.map(r => r.visit_date);
  const sysBp = [];
  const diaBp = [];
  const hrArr = [];

  validRecords.forEach(r => {
    const bpMatch = r.vitals_summary.match(/(\d{2,3})\/(\d{2,3})/);
    if (bpMatch) {
      sysBp.push(parseInt(bpMatch[1]));
      diaBp.push(parseInt(bpMatch[2]));
    } else {
      sysBp.push(null);
      diaBp.push(null);
    }
    const hrMatch = r.vitals_summary.match(/HR[:\s]+(\d{2,3})/i);
    hrArr.push(hrMatch ? parseInt(hrMatch[1]) : null);
  });

  if (appState.charts.vitalsTrend) appState.charts.vitalsTrend.destroy();

  appState.charts.vitalsTrend = new Chart(ctx, {
    type: 'line',
    data: {
      labels: dates.length > 0 ? dates : ['No Records'],
      datasets: [
        { label: 'Systolic BP (mmHg)', data: sysBp, borderColor: '#dc2626', backgroundColor: '#dc2626', tension: 0.2 },
        { label: 'Diastolic BP (mmHg)', data: diaBp, borderColor: '#004b87', backgroundColor: '#004b87', tension: 0.2 },
        { label: 'Heart Rate (bpm)', data: hrArr, borderColor: '#059669', backgroundColor: '#059669', borderDash: [5, 5], tension: 0.2 }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { beginAtZero: false, min: 50, max: 200 }
      }
    }
  });
}

function renderLabsSection(p) {
  const tbody = document.getElementById('patient-lab-tbody');
  if (!tbody) return;

  const labs = p.lab_reports || [];
  if (labs.length === 0) {
    tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding:1.5rem; color:var(--text-muted)">No diagnostic laboratory reports on file.</td></tr>`;
    return;
  }

  tbody.innerHTML = labs.map(l => `
    <tr>
      <td><strong>${escapeHtml(l.test_name)}</strong></td>
      <td>
        <span style="font-weight:700; color:${l.is_abnormal ? 'var(--danger)' : 'var(--success)'}">
          ${escapeHtml(l.result || '—')} ${escapeHtml(l.unit || '')}
        </span>
      </td>
      <td>${escapeHtml(l.normal_range || 'Standard')}</td>
      <td>
        <span class="badge ${l.is_abnormal ? 'badge-danger' : 'badge-success'}">
          ${l.is_abnormal ? '⚠️ Abnormal' : '✓ Normal'}
        </span>
      </td>
      <td>${escapeHtml(l.report_date)}</td>
      <td>
        ${l.file_path ? `<a href="${window.api.getLabDownloadUrl(l.report_id)}" target="_blank" class="btn btn-secondary btn-sm">📎 Download PDF</a>` : '<span style="color:var(--text-dim); font-size:0.75rem">Structured Result</span>'}
      </td>
    </tr>
  `).join('');
}

function renderAbhaCard(p) {
  const nameEl = document.getElementById('abha-name');
  const uidEl = document.getElementById('abha-uid');
  const demogEl = document.getElementById('abha-dob-gender');
  const bloodEl = document.getElementById('abha-blood');

  if (nameEl) nameEl.textContent = p.full_name;
  if (uidEl) uidEl.textContent = `Aadhaar UID: ${maskAadhaar(p.aadhaar_number)}`;
  if (demogEl) demogEl.textContent = `DOB: ${p.date_of_birth} | Gender: ${p.gender}`;
  if (bloodEl) bloodEl.textContent = p.blood_group || 'O+';
}

// Prescription Slip Print (Fix Bug 1)
function openPrescriptionSlipByRecordId(recordId) {
  if (!appState.currentPatient) return;
  const p = appState.currentPatient;
  const r = (p.records || []).find(x => x.record_id === recordId);
  if (!r) {
    toast('Encounter record not found', true);
    return;
  }

  document.getElementById('slip-hospital-name').textContent = r.hospital_name || 'Hospital Authority';
  document.getElementById('slip-record-id').textContent = `REC-${String(r.record_id).padStart(4, '0')}`;
  document.getElementById('slip-date').textContent = `Date: ${r.visit_date}`;
  document.getElementById('slip-pat-name').textContent = p.full_name;
  document.getElementById('slip-pat-aadhaar').textContent = maskAadhaar(p.aadhaar_number);
  const age = new Date().getFullYear() - new Date(p.date_of_birth).getFullYear();
  document.getElementById('slip-pat-demog').textContent = `${age}Y / ${p.gender} / Blood: ${p.blood_group || 'O+'}`;
  document.getElementById('slip-doc-name').textContent = r.doctor_name || 'Medical Officer';
  document.getElementById('slip-vitals').textContent = r.vitals_summary || 'Vitals stable on file';
  document.getElementById('slip-diagnosis').textContent = `${r.diagnosis} ${r.icd10_code ? `[${r.icd10_code}]` : ''}`;
  document.getElementById('slip-prescription').textContent = r.prescription || 'No oral medications prescribed.';
  document.getElementById('slip-sig-text').textContent = r.doctor_name || 'Attending Physician';

  openModal('modal-rx-slip');
}

function triggerBreakGlassModal() {
  if (!appState.currentPatient) return;
  openModal('modal-break-glass');
}

async function confirmBreakGlassAccess() {
  if (!appState.currentPatient) return;
  const reason = document.getElementById('bg-reason-input')?.value || 'Acute Emergency Trauma Resuscitation';

  try {
    const res = await window.api.triggerBreakGlass(appState.currentPatient.aadhaar_number, reason);
    closeModal('modal-break-glass');
    toast(`Emergency break-glass access granted (Audit #${res.audit_id})`);
    
    // Show Emergency Snapshot modal
    document.getElementById('bg-snap-name').textContent = res.name;
    document.getElementById('bg-snap-blood').textContent = res.blood_group;
    document.getElementById('bg-snap-allergies').textContent = res.allergies;
    document.getElementById('bg-snap-chronic').textContent = res.chronic_conditions;
    document.getElementById('bg-snap-meds').textContent = res.active_prescriptions;
    document.getElementById('bg-snap-contact').textContent = res.emergency_contact;
    openModal('modal-emergency-snapshot');
  } catch (err) {
    toast(`Break-glass failed: ${err.message}`, true);
  }
}

// ==========================================================================
// CLINICAL CONSULTATION & CDSS (Phase 4 Bugs 7 & 8)
// ==========================================================================

function startConsultationForPatient(aadhaar) {
  showPage('page-encounter');
  const input = document.getElementById('enc-aadhaar-input');
  if (input) {
    input.value = aadhaar;
    onConsultationPatientSelect(aadhaar);
  }
}

async function onConsultationPatientSelect(aadhaar) {
  try {
    const p = await window.api.getPatient(aadhaar);
    appState.currentPatient = p;
    document.getElementById('enc-pat-name-display').textContent = `${p.full_name} (${p.gender}, ${p.blood_group || 'O+'})`;
    document.getElementById('enc-pat-allergies-display').textContent = p.allergies || 'None';
    
    // Check allergy conflict live
    checkCdssSafety();
  } catch (err) {
    document.getElementById('enc-pat-name-display').textContent = 'Patient not found';
    document.getElementById('enc-pat-allergies-display').textContent = '—';
  }
}

// Clinical Decision Support System (CDSS)
function checkCdssSafety() {
  const p = appState.currentPatient;
  const rxText = document.getElementById('enc-rx-input')?.value || '';
  const alertBox = document.getElementById('cdss-live-alert');
  if (!alertBox) return;

  if (!rxText.trim() || !p) {
    alertBox.style.display = 'none';
    return;
  }

  const rxLower = rxText.toLowerCase();
  const alerts = [];

  // Cross Allergy Check
  if (p.allergies && p.allergies !== 'None') {
    const allergies = p.allergies.toLowerCase();
    if (allergies.includes('penicillin') && (rxLower.includes('amoxicillin') || rxLower.includes('ampicillin') || rxLower.includes('augmentin'))) {
      alerts.push('🚨 <strong>PENICILLIN ALLERGY ALERT:</strong> Prescription contains beta-lactam antibiotic which has cross-reactivity risk with documented Penicillin allergy!');
    }
    if (allergies.includes('sulfa') && (rxLower.includes('septra') || rxLower.includes('bactrim') || rxLower.includes('sulfamethoxazole'))) {
      alerts.push('🚨 <strong>SULFA ALLERGY ALERT:</strong> Severe hypersensitivity risk with documented Sulfa drug allergy!');
    }
    if (allergies.includes('aspirin') && (rxLower.includes('ibuprofen') || rxLower.includes('naproxen') || rxLower.includes('diclofenac'))) {
      alerts.push('🚨 <strong>NSAID ALLERGY ALERT:</strong> Patient has documented Aspirin/NSAID allergy!');
    }
  }

  // Dangerous Drug-Drug Interactions
  if (rxLower.includes('warfarin') && rxLower.includes('aspirin')) {
    alerts.push('⚠️ <strong>CRITICAL DRUG INTERACTION:</strong> Warfarin + Aspirin markedly increases major gastrointestinal and intracranial hemorrhage risk!');
  }
  if (rxLower.includes('sildenafil') && rxLower.includes('nitroglycerin')) {
    alerts.push('⚠️ <strong>FATAL DRUG INTERACTION:</strong> Sildenafil + Nitrates can produce profound, life-threatening hypotension!');
  }

  if (alerts.length > 0) {
    alertBox.style.display = 'block';
    alertBox.innerHTML = alerts.join('<br>');
  } else {
    alertBox.style.display = 'none';
  }
}

// ICD-10 Search & Suggestion
const ICD10_KNOWLEDGE_BASE = [
  { code: 'I10', desc: 'Essential (primary) hypertension', rx: 'Tab Amlodipine 5mg OD morning x 30 days\nLow sodium diet (< 2g/day)\n30 min daily brisk aerobic walk' },
  { code: 'E11.9', desc: 'Type 2 diabetes mellitus without complications', rx: 'Tab Metformin 500mg BD with meals\nDietary carbohydrate control\nExercise 30 min daily' },
  { code: 'J45.909', desc: 'Bronchial asthma, unspecified', rx: 'Budesonide/Formoterol 200/6 Inhaler 2 puffs BD\nTab Montelukast 10mg OD at bedtime' },
  { code: 'I21.4', desc: 'Non-ST elevation myocardial infarction (NSTEMI)', rx: 'Tab Clopidogrel 75mg OD\nTab Atorvastatin 80mg OD HS\nCardiology ICU review' },
  { code: 'M23.22', desc: 'Derangement of meniscus due to old tear, right knee', rx: 'Tab Paracetamol 650mg TDS PRN\nIce pack application\nQuadriceps physiotherapy' },
  { code: 'A09', desc: 'Infectious gastroenteritis and colitis, unspecified', rx: 'Oral Rehydration Salts (ORS) ad libitum\nTab Ondansetron 4mg TDS\nAdequate oral hydration' }
];

function onIcd10Search(keyword) {
  const list = document.getElementById('icd10-suggestions-list');
  if (!list) return;

  if (!keyword.trim()) {
    list.style.display = 'none';
    return;
  }

  const k = keyword.toLowerCase();
  const matches = ICD10_KNOWLEDGE_BASE.filter(item => 
    item.code.toLowerCase().includes(k) || item.desc.toLowerCase().includes(k)
  );

  if (matches.length === 0) {
    list.style.display = 'none';
    return;
  }

  list.style.display = 'block';
  list.innerHTML = matches.map(m => `
    <div style="padding:6px 10px; cursor:pointer; border-bottom:1px solid var(--border-light); font-size:0.8rem;" onclick="applyIcd10('${m.code}', '${escapeHtml(m.desc)}', \`${m.rx}\`)">
      <strong style="color:var(--primary)">${escapeHtml(m.code)}</strong> — ${escapeHtml(m.desc)}
    </div>
  `).join('');
}

function applyIcd10(code, desc, rx) {
  document.getElementById('enc-diagnosis-input').value = desc;
  document.getElementById('enc-icd10-input').value = code;
  const rxInput = document.getElementById('enc-rx-input');
  if (!rxInput.value.trim()) {
    rxInput.value = rx;
  }
  document.getElementById('icd10-suggestions-list').style.display = 'none';
  checkCdssSafety();
}

async function submitClinicalConsultation(event) {
  if (event) event.preventDefault();

  const aadhaar = document.getElementById('enc-aadhaar-input').value.trim();
  const doctorId = document.getElementById('enc-doctor-select').value;
  const hospitalId = appState.currentFacilityId || 1;
  const visitType = document.getElementById('enc-visittype-select').value;
  const department = document.getElementById('enc-dept-select').value;
  const complaint = document.getElementById('enc-complaint-input').value.trim();
  const diagnosis = document.getElementById('enc-diagnosis-input').value.trim();
  const icd10 = document.getElementById('enc-icd10-input').value.trim();
  const vitals = document.getElementById('enc-vitals-input').value.trim();
  const rx = document.getElementById('enc-rx-input').value.trim();
  const notes = document.getElementById('enc-notes-input').value.trim();
  const followup = document.getElementById('enc-followup-input').value;

  if (!aadhaar || !diagnosis) {
    toast('Aadhaar UID and Clinical Diagnosis are required.', true);
    return;
  }

  const recordPayload = {
    aadhaar_number: aadhaar,
    hospital_id: parseInt(hospitalId),
    doctor_id: doctorId ? parseInt(doctorId) : null,
    visit_date: new Date().toISOString().split('T')[0],
    visit_type: visitType,
    department: department,
    chief_complaint: complaint || null,
    diagnosis: diagnosis,
    icd10_code: icd10 || null,
    vitals_summary: vitals || null,
    prescription: rx || null,
    notes: notes || null,
    follow_up_date: followup || null
  };

  try {
    const created = await window.api.createRecord(recordPayload);
    toast(`Encounter saved successfully! (Record #${created.record_id})`);
    document.getElementById('clinical-encounter-form').reset();
    document.getElementById('cdss-live-alert').style.display = 'none';
    viewPatientEhr(aadhaar);
  } catch (err) {
    toast(`Failed to save encounter: ${err.message}`, true);
  }
}

// ==========================================================================
// WARD & BED MANAGEMENT (Phase 4 Bug 4)
// ==========================================================================

async function loadBedMatrix(wardFilter = 'ALL') {
  try {
    const beds = await window.api.getBeds(appState.currentFacilityId, wardFilter);
    appState.beds = beds;
    const grid = document.getElementById('bed-matrix-grid');
    if (!grid) return;

    if (beds.length === 0) {
      grid.innerHTML = `<div style="grid-column:1/-1; text-align:center; padding:2rem; color:var(--text-muted)">No beds found in selected ward.</div>`;
      return;
    }

    grid.innerHTML = beds.map(b => {
      const isOccupied = b.status === 'Occupied';
      const isVacant = b.status === 'Vacant';
      const isCleaning = b.status === 'Cleaning';

      return `
        <div class="bed-card ${isOccupied ? 'occupied' : (isVacant ? 'vacant' : 'cleaning')}">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
              <strong style="font-size:1.05rem; font-family:var(--font-heading)">${escapeHtml(b.bed_number)}</strong>
              <span class="badge ${isOccupied ? 'badge-danger' : (isVacant ? 'badge-success' : 'badge-warning')}">${escapeHtml(b.status)}</span>
            </div>
            <div style="font-size:0.75rem; color:var(--text-muted); margin-bottom:6px;">${escapeHtml(b.ward_name)}</div>
            ${isOccupied ? `
              <div style="background:var(--bg-alt); padding:5px 8px; border-radius:4px; font-size:0.76rem; margin-bottom:8px;">
                <div style="font-weight:700; color:var(--text)">${escapeHtml(b.patient_name || 'Patient')}</div>
                <div style="font-size:0.72rem; color:var(--text-muted); font-family:var(--font-mono)">${escapeHtml(maskAadhaar(b.aadhaar_number))}</div>
                <div style="font-size:0.7rem; color:var(--text-dim); margin-top:2px;">Admitted: ${b.admitted_at ? b.admitted_at.substring(0, 10) : 'Today'}</div>
              </div>
            ` : (isCleaning ? `
              <div style="padding:6px; font-size:0.75rem; color:var(--warning); margin-bottom:8px;">Sanitization in progress</div>
            ` : `
              <div style="padding:6px; font-size:0.75rem; color:var(--success); margin-bottom:8px;">Ready for patient allocation</div>
            `)}
          </div>
          <div>
            ${isVacant ? `
              <button class="btn btn-primary btn-sm" style="width:100%" onclick="openAdmitBedModal('${b.bed_number}')">➕ Admit Patient</button>
            ` : (isOccupied ? `
              <button class="btn btn-danger btn-sm" style="width:100%" onclick="dischargeBed(${b.allocation_id})">Discharge Patient</button>
            ` : `
              <button class="btn btn-secondary btn-sm" style="width:100%" onclick="cleanBed(${b.allocation_id})">✓ Mark Cleaned</button>
            `)}
          </div>
        </div>
      `;
    }).join('');
  } catch (err) {
    toast(`Failed to load bed matrix: ${err.message}`, true);
  }
}

async function openAdmitBedModal(bedNumber) {
  // Populate patient select options
  const patients = await window.api.getPatients('', 100);
  const select = document.getElementById('admit-patient-select');
  if (select) {
    select.innerHTML = patients.map(p => 
      `<option value="${p.aadhaar_number}">${p.full_name} (${p.aadhaar_number})</option>`
    ).join('');
  }
  document.getElementById('admit-bed-number-input').value = bedNumber;
  openModal('modal-bed-admit');
}

async function confirmBedAdmission(event) {
  if (event) event.preventDefault();
  const bedNum = document.getElementById('admit-bed-number-input').value;
  const aadhaar = document.getElementById('admit-patient-select').value;
  const dischargeDate = document.getElementById('admit-discharge-date').value || null;

  try {
    await window.api.admitBed({
      hospital_id: appState.currentFacilityId || 1,
      bed_number: bedNum,
      aadhaar_number: aadhaar,
      expected_discharge: dischargeDate
    });
    closeModal('modal-bed-admit');
    toast(`Patient admitted to Bed ${bedNum} successfully!`);
    loadBedMatrix();
  } catch (err) {
    toast(`Admission blocked: ${err.message}`, true);
  }
}

async function dischargeBed(allocationId) {
  if (!confirm('Confirm patient discharge? Bed will transition to Cleaning status.')) return;
  try {
    await window.api.dischargeBed(allocationId);
    toast('Patient discharged. Bed marked for sanitization.');
    loadBedMatrix();
  } catch (err) {
    toast(`Discharge failed: ${err.message}`, true);
  }
}

async function cleanBed(allocationId) {
  try {
    await window.api.cleanBed(allocationId);
    toast('Bed sanitized and marked Vacant.');
    loadBedMatrix();
  } catch (err) {
    toast(`Failed to update bed: ${err.message}`, true);
  }
}

// ==========================================================================
// OPD LIVE QUEUE (Phase 4 Bug 2)
// ==========================================================================

async function loadOpdQueue() {
  try {
    const queue = await window.api.getQueue(appState.currentFacilityId);
    appState.queue = queue;

    const servingItem = queue.find(q => q.status === 'Serving');
    const heroToken = document.getElementById('now-serving-token');
    const heroPatient = document.getElementById('now-serving-patient');
    const heroDoctor = document.getElementById('now-serving-doctor');

    if (servingItem) {
      if (heroToken) heroToken.textContent = servingItem.token_number;
      if (heroPatient) heroPatient.textContent = servingItem.patient_name;
      if (heroDoctor) heroDoctor.textContent = servingItem.doctor_name;
    } else {
      if (heroToken) heroToken.textContent = '—';
      if (heroPatient) heroPatient.textContent = 'No patient currently called';
      if (heroDoctor) heroDoctor.textContent = 'Room available';
    }

    const tbody = document.getElementById('opd-queue-tbody');
    if (!tbody) return;

    if (queue.length === 0) {
      tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding:2rem; color:var(--text-muted)">No patients in today's OPD queue.</td></tr>`;
      return;
    }

    tbody.innerHTML = queue.map(q => {
      const isServing = q.status === 'Serving';
      const isWaiting = q.status === 'Waiting';
      const isCompleted = q.status === 'Completed';

      return `
        <tr>
          <td><strong style="font-family:var(--font-mono); font-size:1.1rem; color:var(--primary)">${escapeHtml(q.token_number)}</strong></td>
          <td><strong>${escapeHtml(q.patient_name)}</strong></td>
          <td>${escapeHtml(q.doctor_name)}</td>
          <td>${escapeHtml(q.time_issued)}</td>
          <td>
            <span class="badge ${isServing ? 'badge-danger' : (isWaiting ? 'badge-warning' : (isCompleted ? 'badge-success' : 'badge-primary'))}">
              ${escapeHtml(q.status)}
            </span>
          </td>
          <td>
            ${isWaiting ? `
              <button class="btn btn-primary btn-sm" onclick="setTokenServing(${q.queue_id})">Call</button>
              <button class="btn btn-danger btn-sm" onclick="cancelToken(${q.queue_id})">Cancel</button>
            ` : (isServing ? `
              <button class="btn btn-success btn-sm" onclick="completeToken(${q.queue_id})">✓ Complete</button>
            ` : '<span style="color:var(--text-dim); font-size:0.75rem">Archived</span>')}
          </td>
        </tr>
      `;
    }).join('');
  } catch (err) {
    toast(`Failed to load OPD queue: ${err.message}`, true);
  }
}

async function openAddQueueModal() {
  const patients = await window.api.getPatients('', 100);
  const select = document.getElementById('queue-patient-select');
  if (select) {
    select.innerHTML = patients.map(p => 
      `<option value="${p.aadhaar_number}">${p.full_name} (${p.aadhaar_number})</option>`
    ).join('');
  }

  const doctors = await window.api.getDoctors();
  const docSelect = document.getElementById('queue-doctor-select');
  if (docSelect) {
    docSelect.innerHTML = doctors.map(d => 
      `<option value="${d.doctor_id}">${d.doctor_name} (${d.specialization})</option>`
    ).join('');
  }

  openModal('modal-add-queue');
}

async function confirmIssueToken(event) {
  if (event) event.preventDefault();
  const aadhaar = document.getElementById('queue-patient-select').value;
  const docId = document.getElementById('queue-doctor-select').value;

  try {
    const q = await window.api.issueQueueToken({
      aadhaar_number: aadhaar,
      doctor_id: docId ? parseInt(docId) : null,
      hospital_id: appState.currentFacilityId || 1
    });
    closeModal('modal-add-queue');
    toast(`Token ${q.token_number} issued for ${q.patient_name}`);
    loadOpdQueue();
  } catch (err) {
    toast(`Issue failed: ${err.message}`, true);
  }
}

async function setTokenServing(queueId) {
  try {
    await window.api.updateQueueStatus(queueId, 'Serving');
    playChime();
    loadOpdQueue();
  } catch (err) {
    toast(`Error: ${err.message}`, true);
  }
}

async function completeToken(queueId) {
  try {
    await window.api.updateQueueStatus(queueId, 'Completed');
    toast('Token marked Completed');
    loadOpdQueue();
  } catch (err) {
    toast(`Error: ${err.message}`, true);
  }
}

async function cancelToken(queueId) {
  try {
    await window.api.updateQueueStatus(queueId, 'Cancelled');
    toast('Token Cancelled');
    loadOpdQueue();
  } catch (err) {
    toast(`Error: ${err.message}`, true);
  }
}

function playChime() {
  try {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.type = 'sine';
    osc.frequency.setValueAtTime(587.33, ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 0.3);
    gain.gain.setValueAtTime(0.3, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.7);
    osc.start();
    osc.stop(ctx.currentTime + 0.75);
  } catch (e) {
    // Audio context may require user gesture
  }
}

// ==========================================================================
// APPOINTMENTS SCHEDULING (New Feature A)
// ==========================================================================

async function loadAppointments() {
  try {
    const appts = await window.api.getAppointments({ hospital_id: appState.currentFacilityId });
    appState.appointments = appts;
    const tbody = document.getElementById('appointments-tbody');
    if (!tbody) return;

    if (appts.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:2rem; color:var(--text-muted)">No scheduled appointments.</td></tr>`;
      return;
    }

    tbody.innerHTML = appts.map(a => `
      <tr>
        <td><strong style="color:var(--primary)">APT-${String(a.appointment_id).padStart(4, '0')}</strong></td>
        <td><strong>${escapeHtml(a.appointment_date)}</strong> at <span class="badge badge-info">${escapeHtml(a.time_slot)}</span></td>
        <td><strong>${escapeHtml(a.patient_name)}</strong> <span style="font-size:0.75rem; color:var(--text-muted)">(${maskAadhaar(a.aadhaar_number)})</span></td>
        <td>${escapeHtml(a.doctor_name)}</td>
        <td>${escapeHtml(a.department || 'General')}</td>
        <td><span class="badge ${a.status === 'Scheduled' ? 'badge-primary' : (a.status === 'Completed' ? 'badge-success' : 'badge-danger')}">${escapeHtml(a.status)}</span></td>
        <td>
          ${a.status === 'Scheduled' ? `
            <button class="btn btn-secondary btn-sm" onclick="openRescheduleModal(${a.appointment_id})">Reschedule</button>
            <button class="btn btn-danger btn-sm" onclick="cancelAppointment(${a.appointment_id})">Cancel</button>
          ` : '<span style="color:var(--text-dim); font-size:0.75rem">—</span>'}
        </td>
      </tr>
    `).join('');
  } catch (err) {
    toast(`Failed to load appointments: ${err.message}`, true);
  }
}

async function openBookAppointmentModal() {
  const patients = await window.api.getPatients('', 100);
  const patSelect = document.getElementById('appt-patient-select');
  if (patSelect) {
    patSelect.innerHTML = patients.map(p => 
      `<option value="${p.aadhaar_number}">${p.full_name} (${p.aadhaar_number})</option>`
    ).join('');
  }

  const doctors = await window.api.getDoctors();
  const docSelect = document.getElementById('appt-doctor-select');
  if (docSelect) {
    docSelect.innerHTML = doctors.map(d => 
      `<option value="${d.doctor_id}">${d.doctor_name} (${d.specialization})</option>`
    ).join('');
  }

  document.getElementById('appt-date-input').value = new Date().toISOString().split('T')[0];
  openModal('modal-book-appointment');
}

async function confirmBookAppointment(event) {
  if (event) event.preventDefault();
  const aadhaar = document.getElementById('appt-patient-select').value;
  const docId = document.getElementById('appt-doctor-select').value;
  const date = document.getElementById('appt-date-input').value;
  const slot = document.getElementById('appt-slot-select').value;
  const reason = document.getElementById('appt-reason-input').value.trim();

  try {
    const appt = await window.api.bookAppointment({
      aadhaar_number: aadhaar,
      doctor_id: parseInt(docId),
      hospital_id: appState.currentFacilityId || 1,
      appointment_date: date,
      time_slot: slot,
      reason: reason || 'Consultation'
    });
    closeModal('modal-book-appointment');
    toast(`Appointment booked with ${appt.doctor_name} on ${appt.appointment_date} at ${appt.time_slot}`);
    loadAppointments();
  } catch (err) {
    toast(`Booking blocked: ${err.message}`, true);
  }
}

async function openRescheduleModal(appointmentId) {
  document.getElementById('resched-id-input').value = appointmentId;
  document.getElementById('resched-date-input').value = new Date().toISOString().split('T')[0];
  openModal('modal-reschedule-appointment');
}

async function confirmRescheduleAppointment(event) {
  if (event) event.preventDefault();
  const apptId = document.getElementById('resched-id-input').value;
  const date = document.getElementById('resched-date-input').value;
  const slot = document.getElementById('resched-slot-select').value;

  try {
    await window.api.rescheduleAppointment(apptId, {
      appointment_date: date,
      time_slot: slot
    });
    closeModal('modal-reschedule-appointment');
    toast('Appointment rescheduled successfully!');
    loadAppointments();
  } catch (err) {
    toast(`Reschedule failed: ${err.message}`, true);
  }
}

async function cancelAppointment(appointmentId) {
  if (!confirm('Cancel this appointment?')) return;
  try {
    await window.api.updateAppointmentStatus(appointmentId, 'Cancelled');
    toast('Appointment cancelled');
    loadAppointments();
  } catch (err) {
    toast(`Cancel failed: ${err.message}`, true);
  }
}

// ==========================================================================
// DOCTORS MANAGEMENT & AVAILABILITY (New Feature B)
// ==========================================================================

async function loadDoctors() {
  try {
    const doctors = await window.api.getDoctors();
    appState.doctors = doctors;
    const grid = document.getElementById('doctors-grid');
    if (!grid) return;

    grid.innerHTML = doctors.map(d => `
      <div class="card" style="margin-bottom:0">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:8px;">
          <div>
            <h3 style="font-size:1.05rem; font-weight:800; font-family:var(--font-heading)">${escapeHtml(d.doctor_name)}</h3>
            <div style="color:var(--primary); font-size:0.8rem; font-weight:600;">${escapeHtml(d.specialization)}</div>
            <div style="font-size:0.75rem; color:var(--text-muted);">${escapeHtml(d.qualification || 'MBBS')}</div>
          </div>
          <span class="badge badge-success">Available</span>
        </div>
        <div style="background:var(--bg-alt); padding:8px; border-radius:var(--radius-md); font-size:0.78rem; margin-bottom:10px;">
          <div>🏥 ${escapeHtml(d.hospital_name)}</div>
          <div>📞 ${escapeHtml(d.contact || '—')}</div>
          <div>📜 Lic: <span style="font-family:var(--font-mono)">${escapeHtml(d.license_no || '—')}</span></div>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:0.78rem; border-top:1px solid var(--border-light); padding-top:8px; margin-bottom:10px;">
          <div>Today's Consults: <strong style="color:var(--primary)">${d.today_consultations}</strong></div>
          <div>Upcoming Appts: <strong style="color:var(--info)">${d.upcoming_appointments}</strong></div>
        </div>
        <div>
          <button class="btn btn-primary btn-sm" style="width:100%" onclick="openBookAppointmentModal()">Book Slot</button>
        </div>
      </div>
    `).join('');
  } catch (err) {
    toast(`Failed to load doctors: ${err.message}`, true);
  }
}

// ==========================================================================
// DIGITAL LAB REPORTS (New Feature C)
// ==========================================================================

async function loadAllLabs() {
  try {
    const labs = await window.api.getLabs({ limit: 50 });
    const tbody = document.getElementById('all-labs-tbody');
    if (!tbody) return;

    if (labs.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:2rem; color:var(--text-muted)">No lab investigations on file.</td></tr>`;
      return;
    }

    tbody.innerHTML = labs.map(l => `
      <tr>
        <td><strong style="color:var(--primary)">LAB-${String(l.report_id).padStart(4, '0')}</strong></td>
        <td><strong>${escapeHtml(l.test_name)}</strong></td>
        <td><span style="font-family:var(--font-mono)">${maskAadhaar(l.aadhaar_number)}</span></td>
        <td>
          <span style="font-weight:700; color:${l.is_abnormal ? 'var(--danger)' : 'var(--success)'}">
            ${escapeHtml(l.result || '—')} ${escapeHtml(l.unit || '')}
          </span>
        </td>
        <td>${escapeHtml(l.normal_range || 'Standard')}</td>
        <td><span class="badge ${l.is_abnormal ? 'badge-danger' : 'badge-success'}">${l.is_abnormal ? '⚠️ Abnormal' : '✓ Normal'}</span></td>
        <td>
          ${l.file_path ? `<a href="${window.api.getLabDownloadUrl(l.report_id)}" target="_blank" class="btn btn-secondary btn-sm">📎 Download PDF</a>` : '<span style="color:var(--text-dim); font-size:0.75rem">Recorded</span>'}
        </td>
      </tr>
    `).join('');
  } catch (err) {
    toast(`Failed to load lab reports: ${err.message}`, true);
  }
}

async function submitLabReportUpload(event) {
  if (event) event.preventDefault();

  const fileInput = document.getElementById('lab-file-input');
  if (!fileInput.files || fileInput.files.length === 0) {
    toast('Please select a PDF report file.', true);
    return;
  }

  const formData = new FormData();
  formData.append('aadhaar_number', document.getElementById('lab-aadhaar-input').value.trim());
  formData.append('test_name', document.getElementById('lab-test-input').value.trim());
  formData.append('result', document.getElementById('lab-result-input').value.trim());
  formData.append('normal_range', document.getElementById('lab-range-input').value.trim());
  formData.append('unit', document.getElementById('lab-unit-input').value.trim());
  formData.append('is_abnormal', document.getElementById('lab-abnormal-check').checked);
  formData.append('report_date', document.getElementById('lab-date-input').value || new Date().toISOString().split('T')[0]);
  formData.append('file', fileInput.files[0]);

  try {
    await window.api.uploadLabPdf(formData);
    closeModal('modal-upload-lab');
    toast('Digital lab report uploaded and linked successfully!');
    loadAllLabs();
  } catch (err) {
    toast(`Upload failed: ${err.message}`, true);
  }
}

// ==========================================================================
// ACCESS AUDIT LOGS (Phase 4 Bug 5)
// ==========================================================================

async function loadAuditLogs(aadhaarFilter = '') {
  try {
    const logs = await window.api.getAuditLogs(aadhaarFilter, 50);
    const tbody = document.getElementById('audit-logs-tbody');
    if (!tbody) return;

    if (logs.length === 0) {
      tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding:2rem; color:var(--text-muted)">No audit trail records found.</td></tr>`;
      return;
    }

    tbody.innerHTML = logs.map(l => `
      <tr>
        <td><strong style="color:var(--primary)">LOG-${String(l.log_id).padStart(4, '0')}</strong></td>
        <td><span style="font-size:0.78rem; font-family:var(--font-mono)">${l.access_time.replace('T', ' ').substring(0, 19)}</span></td>
        <td><strong style="font-family:var(--font-mono)">${escapeHtml(l.masked_aadhaar || l.aadhaar_number)}</strong></td>
        <td><strong>${escapeHtml(l.accessed_by)}</strong></td>
        <td>${escapeHtml(l.purpose || 'Lookup')}</td>
        <td><span style="font-family:var(--font-mono); font-size:0.75rem; color:var(--text-dim)">${escapeHtml(l.ip_address || '127.0.0.1')}</span></td>
      </tr>
    `).join('');
  } catch (err) {
    toast(`Failed to load audit logs: ${err.message}`, true);
  }
}

// ==========================================================================
// SQL QUERY WORKBENCH (Phase 4 Bug 9)
// ==========================================================================

async function loadSqlWorkbench() {
  try {
    const queries = await window.api.getSqlQueries();
    const select = document.getElementById('sql-query-select');
    if (select) {
      select.innerHTML = queries.map(q => 
        `<option value="${q.key}">${q.title}</option>`
      ).join('');
    }
    onSqlQuerySelectChange();
  } catch (err) {
    toast(`Failed to load approved queries: ${err.message}`, true);
  }
}

async function onSqlQuerySelectChange() {
  const select = document.getElementById('sql-query-select');
  if (!select) return;
  const queries = await window.api.getSqlQueries();
  const qMeta = queries.find(q => q.key === select.value);
  if (qMeta) {
    document.getElementById('sql-query-display').textContent = qMeta.sql;
    const paramInput = document.getElementById('sql-param-input');
    if (paramInput) {
      paramInput.value = qMeta.default_param;
      paramInput.placeholder = qMeta.param_label;
    }
  }
}

async function executeActiveSqlQuery() {
  const key = document.getElementById('sql-query-select').value;
  const param = document.getElementById('sql-param-input')?.value || '';

  try {
    const res = await window.api.executeSqlQuery(key, param);
    document.getElementById('sql-exec-stat').textContent = `Query executed in ${res.execution_time_ms} ms • ${res.row_count} rows returned against real persistent database`;

    const thead = document.getElementById('sql-output-thead');
    const tbody = document.getElementById('sql-output-tbody');

    if (res.rows.length === 0) {
      thead.innerHTML = '';
      tbody.innerHTML = `<tr><td style="text-align:center; padding:1.5rem; color:var(--text-muted)">0 rows returned.</td></tr>`;
      return;
    }

    thead.innerHTML = `<tr>${res.columns.map(c => `<th>${escapeHtml(c)}</th>`).join('')}</tr>`;
    tbody.innerHTML = res.rows.map(r => `
      <tr>${res.columns.map(c => `<td>${escapeHtml(r[c])}</td>`).join('')}</tr>
    `).join('');
  } catch (err) {
    toast(`Query execution error: ${err.message}`, true);
  }
}

// ==========================================================================
// DATABASE BACKUP, IMPORT & HEALTH (Phase 3 & Phase 4)
// ==========================================================================

async function loadBackupStatus() {
  try {
    const health = await window.api.checkHealth();
    document.getElementById('health-engine-badge').textContent = health.database.engine.toUpperCase();
    document.getElementById('health-latency').textContent = `${health.database.latency_ms} ms`;
    document.getElementById('health-patients-count').textContent = health.database.counts.patients;
    document.getElementById('health-records-count').textContent = health.database.counts.records;
    document.getElementById('health-beds-count').textContent = health.database.counts.beds;
  } catch (err) {
    console.error('Failed to load health status:', err);
  }
}

async function exportDatabaseJson() {
  try {
    const data = await window.api.exportBackup();
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `medilink_db_export_${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
    toast('Database exported successfully!');
  } catch (err) {
    toast(`Export failed: ${err.message}`, true);
  }
}

async function importDatabaseJson(event) {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = async (e) => {
    try {
      const json = JSON.parse(e.target.result);
      const res = await window.api.importBackup(json);
      toast(res.message);
      loadDashboard();
    } catch (err) {
      toast(`Import failed: ${err.message}`, true);
    }
  };
  reader.readAsText(file);
}

// ==========================================================================
// IN-APP NOTIFICATIONS (New Feature D)
// ==========================================================================

async function loadNotifications() {
  try {
    const notifs = await window.api.getNotifications();
    appState.notifications = notifs;
    const badge = document.getElementById('notif-unread-dot');
    const unread = notifs.filter(n => !n.is_read);
    if (badge) badge.style.display = unread.length > 0 ? 'block' : 'none';

    const list = document.getElementById('notifications-dropdown-list');
    if (list) {
      if (notifs.length === 0) {
        list.innerHTML = `<div style="padding:1rem; text-align:center; color:var(--text-muted); font-size:0.8rem">No notifications</div>`;
      } else {
        list.innerHTML = notifs.slice(0, 8).map(n => `
          <div style="padding:8px 12px; border-bottom:1px solid var(--border-light); font-size:0.8rem; background:${n.is_read ? 'transparent' : 'var(--primary-light)'}">
            <div style="font-weight:700; color:var(--text)">${escapeHtml(n.title)}</div>
            <div style="font-size:0.75rem; color:var(--text-muted); margin-top:2px;">${escapeHtml(n.message)}</div>
            <div style="font-size:0.68rem; color:var(--text-dim); margin-top:2px;">${n.created_at.substring(0, 16).replace('T', ' ')}</div>
          </div>
        `).join('');
      }
    }
  } catch (err) {
    console.error('Failed to load notifications:', err);
  }
}

function toggleNotificationDropdown() {
  const dropdown = document.getElementById('notifications-dropdown');
  if (dropdown) {
    const isHidden = dropdown.style.display === 'none' || !dropdown.style.display;
    dropdown.style.display = isHidden ? 'block' : 'none';
  }
}

// ==========================================================================
// GLOBAL SEARCH (New Feature E)
// ==========================================================================

function handleGlobalSearchKey(event) {
  if (event.key === 'Enter') {
    executeGlobalSearch();
  }
}

async function executeGlobalSearch() {
  const query = document.getElementById('global-search-input')?.value.trim();
  if (!query) return;

  // Search patients
  const patients = await window.api.getPatients(query);
  if (patients.length > 0) {
    viewPatientEhr(patients[0].aadhaar_number);
  } else {
    toast(`No patients found matching '${query}'`, true);
  }
}

// ==========================================================================
// EMERGENCY TRIAGE (ESI 1-5 ENGINE)
// ==========================================================================

function calculateEsiTriage() {
  const vitalsUnstable = document.getElementById('triage-unstable-vitals')?.checked;
  const highRisk = document.getElementById('triage-high-risk')?.checked;
  const resources = parseInt(document.getElementById('triage-resources')?.value || '0');

  let level = 5;
  let label = 'ESI 5 — Non-urgent';
  let bay = 'Standard Outpatient Clinic';
  let badgeClass = 'badge-primary';

  if (document.getElementById('triage-resuscitation')?.checked) {
    level = 1;
    label = 'ESI 1 — Resuscitation (Immediate Life Threat)';
    bay = 'Emergency Trauma Bay ER-101';
    badgeClass = 'badge-danger';
  } else if (highRisk || vitalsUnstable) {
    level = 2;
    label = 'ESI 2 — Emergent (High Risk / Severe Pain / Altered Sensorium)';
    bay = 'Acute Monitored Bed (ER-102 / HDU)';
    badgeClass = 'badge-danger';
  } else if (resources >= 2) {
    level = 3;
    label = 'ESI 3 — Urgent (Multiple Resources Required)';
    bay = 'Observation Ward / Medical Care';
    badgeClass = 'badge-warning';
  } else if (resources === 1) {
    level = 4;
    label = 'ESI 4 — Less Urgent (Single Investigation/Treatment)';
    bay = 'Fast Track Treatment Area';
    badgeClass = 'badge-info';
  }

  const resultBox = document.getElementById('triage-result-card');
  if (resultBox) {
    resultBox.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
          <span class="badge ${badgeClass}" style="font-size:0.85rem; padding:4px 10px;">${label}</span>
          <div style="font-size:0.85rem; margin-top:8px;">Recommended Bed/Ward: <strong>${bay}</strong></div>
          <div style="font-size:0.75rem; color:var(--text-dim); margin-top:4px;">
            ⚠️ <em>Demonstration clinical decision support based on ESI v4 algorithm. Clinical physician confirmation required.</em>
          </div>
        </div>
        <button class="btn btn-primary" onclick="showPage('page-beds')">Go to Bed Allocation</button>
      </div>
    `;
  }
}

// ==========================================================================
// INITIALIZATION ON PAGE LOAD
// ==========================================================================

window.addEventListener('DOMContentLoaded', async () => {
  initTheme();
  await initAuth();
  showPage('page-home');
  loadNotifications();

  // Keyboard shortcut Ctrl+K for global search
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      const input = document.getElementById('global-search-input');
      if (input) input.focus();
    }
  });
});
