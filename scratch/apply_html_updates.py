with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update version strings
html = html.replace(
    '<title>MediLink Enterprise — Hospital Management & Unified Medical Records Network</title>',
    '<title>MediLink Enterprise v4.0 — Hospital Management & Unified Medical Records Network</title>'
)
html = html.replace(
    '<span>Enterprise Healthcare Platform v3.0</span>',
    '<span>Enterprise Healthcare Platform v4.0</span>'
)
html = html.replace(
    '<strong style="font-size:0.85rem; margin-left:8px;">MediLink Command Center v3.0 — AIIMS Node</strong>',
    '<strong style="font-size:0.85rem; margin-left:8px;">MediLink Command Center v4.0 — AIIMS Node</strong>'
)
html = html.replace(
    '<div>© 2026 MediLink Enterprise v3.0. All rights reserved.</div>',
    '<div>© 2026 MediLink Enterprise v4.0. All rights reserved.</div>'
)
html = html.replace(
    'Hospital Network Node v3.0 • Verified ABHA/Aadhaar Linked EMR',
    'Hospital Network Node v4.0 • Verified ABHA/Aadhaar Linked EMR'
)

# 2. Update topbar search box
old_search_box = '''          <div class="global-search-box">
            <span class="search-icon">🔍</span>
            <input type="text" id="global-search-input" placeholder="Search patient by Aadhaar, name, phone..." onkeydown="handleGlobalSearchKey(event)" />
            <span class="search-shortcut">Ctrl+K</span>
          </div>'''

new_search_box = '''          <div class="global-search-box" onclick="openGlobalSearch()" title="Open Global Command Search (Ctrl+K)">
            <span class="search-icon">🔍</span>
            <input type="text" id="global-search-input" placeholder="Search patients, doctors, records... (Ctrl+K)" readonly onclick="openGlobalSearch()" style="cursor:pointer;" />
            <span class="search-shortcut">Ctrl+K</span>
          </div>'''

assert old_search_box in html, "Could not find old_search_box in index.html"
html = html.replace(old_search_box, new_search_box)

# 3. Update page-patients
old_page_patients = '''        <section id="page-patients" class="page">
          <div class="card">
            <div class="card-header">
              <div class="card-title">👥 Unified Citizen Patient Directory</div>
              <div style="display:flex; gap:0.5rem;">
                <button class="btn btn-primary btn-sm" onclick="showPage('page-register')">➕ Enroll New Patient</button>
              </div>
            </div>

            <div style="display:flex; gap:1rem; margin-bottom:1rem; flex-wrap:wrap;">
              <input type="text" id="patient-dir-search-input" class="form-control" style="max-width:340px;" placeholder="Filter by name, Aadhaar, blood group..." oninput="loadPatientDirectory(this.value)" />
              <button class="btn btn-secondary btn-sm" onclick="loadPatientDirectory()">Refresh</button>
            </div>

            <div class="table-container">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Aadhaar UID</th>
                    <th>Patient Full Name</th>
                    <th>Demographics</th>
                    <th>Blood</th>
                    <th>Mobile</th>
                    <th>Documented Allergies</th>
                    <th>Clinical Actions</th>
                  </tr>
                </thead>
                <tbody id="patient-directory-tbody"></tbody>
              </table>
            </div>
          </div>
        </section>'''

new_page_patients = '''        <section id="page-patients" class="page">
          <div class="card">
            <div class="card-header">
              <div class="card-title">👥 Unified Citizen Patient Directory</div>
              <div style="display:flex; gap:0.5rem; align-items:center;">
                <button class="btn btn-outline btn-sm" onclick="exportPatientsCSV()" title="Export current patient list as CSV">📥 Export CSV</button>
                <button class="btn btn-primary btn-sm" onclick="showPage('page-register')">➕ Enroll New Patient</button>
              </div>
            </div>

            <div style="display:flex; gap:0.75rem; margin-bottom:1rem; flex-wrap:wrap; align-items:center;">
              <input type="text" id="patient-dir-search-input" class="form-control" style="max-width:280px;" placeholder="Search name, Aadhaar, phone..." oninput="onPatientDirFilterChange()" />
              <select id="patient-dir-gender-filter" class="form-control" style="max-width:140px;" onchange="onPatientDirFilterChange()">
                <option value="">All Genders</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
              <select id="patient-dir-blood-filter" class="form-control" style="max-width:150px;" onchange="onPatientDirFilterChange()">
                <option value="">All Blood Types</option>
                <option value="A+">A+</option>
                <option value="A-">A-</option>
                <option value="B+">B+</option>
                <option value="B-">B-</option>
                <option value="AB+">AB+</option>
                <option value="AB-">AB-</option>
                <option value="O+">O+</option>
                <option value="O-">O-</option>
              </select>
              <button class="btn btn-secondary btn-sm" onclick="resetPatientDirFilters()">Reset</button>
            </div>

            <div class="table-container">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Aadhaar UID</th>
                    <th>Patient Full Name</th>
                    <th>Demographics</th>
                    <th>Blood</th>
                    <th>Mobile</th>
                    <th>Documented Allergies</th>
                    <th>Clinical Actions</th>
                  </tr>
                </thead>
                <tbody id="patient-directory-tbody"></tbody>
              </table>
            </div>

            <div class="table-pagination" id="patient-dir-pagination" style="display:flex; justify-content:space-between; align-items:center; margin-top:1rem; padding-top:0.75rem; border-top:1px solid var(--border-light); font-size:0.82rem; color:var(--text-muted);">
              <div id="patient-dir-page-info">Showing patients</div>
              <div style="display:flex; gap:0.5rem; align-items:center;">
                <button class="btn btn-secondary btn-sm" id="btn-patient-prev" onclick="changePatientPage(-1)" disabled>◀ Prev</button>
                <span id="patient-dir-current-page" style="font-weight:700; padding:0 8px; color:var(--primary);">1 / 1</span>
                <button class="btn btn-secondary btn-sm" id="btn-patient-next" onclick="changePatientPage(1)" disabled>Next ▶</button>
              </div>
            </div>
          </div>
        </section>'''

assert old_page_patients in html, "Could not find old_page_patients in index.html"
html = html.replace(old_page_patients, new_page_patients)

# 4. Modals: Add modal-global-search and modal-edit-patient
new_modals = '''
  <!-- Modal: Global Search Command Palette (Ctrl+K) -->
  <div id="modal-global-search" class="modal-backdrop" onclick="if(event.target===this) closeGlobalSearch()">
    <div class="modal-content global-search-modal-card" style="max-width: 660px; padding: 0; overflow: hidden; border-radius: var(--radius-lg); box-shadow: var(--shadow-xl);">
      <div class="global-search-modal-header" style="display:flex; align-items:center; gap:0.75rem; padding: 1rem 1.25rem; border-bottom: 1px solid var(--border-light); background: var(--surface);">
        <span style="font-size:1.2rem; color:var(--primary); line-height:1;">🔍</span>
        <input type="text" id="global-search-palette-input" class="form-control" placeholder="Search patients, doctors, records, or quick navigation..." style="border:none; box-shadow:none; font-size:1rem; padding:0; background:transparent; width:100%; outline:none;" oninput="handlePaletteSearch(this.value)" onkeydown="handlePaletteKeydown(event)" />
        <span class="badge badge-secondary" style="font-size:0.72rem; padding: 2px 6px; border:1px solid var(--border-light);">ESC</span>
        <button class="btn-icon" onclick="closeGlobalSearch()" style="margin-left:4px;">✕</button>
      </div>
      <div style="display:flex; gap:0.5rem; padding: 0.5rem 1.25rem; background: var(--bg-alt); border-bottom: 1px solid var(--border-light); font-size:0.75rem;">
        <button class="palette-chip active" id="palette-filter-all" onclick="setPaletteFilter('all', this)">All</button>
        <button class="palette-chip" id="palette-filter-patients" onclick="setPaletteFilter('patients', this)">Patients</button>
        <button class="palette-chip" id="palette-filter-doctors" onclick="setPaletteFilter('doctors', this)">Doctors</button>
        <button class="palette-chip" id="palette-filter-pages" onclick="setPaletteFilter('pages', this)">Pages</button>
      </div>
      <div id="global-search-palette-results" style="max-height: 380px; overflow-y: auto; padding: 0.5rem 0;">
        <!-- Populated dynamically -->
      </div>
      <div style="display:flex; justify-content:space-between; align-items:center; padding: 0.5rem 1.25rem; background: var(--bg-alt); border-top:1px solid var(--border-light); font-size: 0.72rem; color: var(--text-muted);">
        <span><kbd>↑</kbd> <kbd>↓</kbd> to navigate • <kbd>Enter</kbd> to select • <kbd>ESC</kbd> to close</span>
        <span>MediLink Enterprise v4.0 Quick Search</span>
      </div>
    </div>
  </div>

  <!-- Modal: Edit Patient Demographic & Clinical Details -->
  <div id="modal-edit-patient" class="modal-backdrop">
    <div class="modal-content" style="max-width: 600px;">
      <div class="modal-header">
        <h3 style="font-size:1.05rem; font-weight:800; font-family:var(--font-heading)">✏️ Edit Patient Demographic & Clinical Details</h3>
        <button class="btn-icon" onclick="closeModal('modal-edit-patient')">✕</button>
      </div>
      <form id="form-edit-patient" onsubmit="submitEditPatient(event)">
        <input type="hidden" id="edit-pat-aadhaar" />
        <div class="modal-body" style="display:flex; flex-direction:column; gap:0.9rem;">
          <div style="background:var(--bg-alt); padding:8px 12px; border-radius:var(--radius-md); font-size:0.82rem; display:flex; justify-content:space-between; align-items:center;">
            <div>Patient: <strong id="edit-pat-name-display">—</strong></div>
            <div>UID: <span id="edit-pat-aadhaar-display" style="font-family:var(--font-mono); color:var(--primary); font-weight:700;">—</span></div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Phone Number *</label>
              <input type="tel" id="edit-pat-phone" class="form-control" required pattern="[0-9]{10}" placeholder="10-digit mobile" />
            </div>
            <div class="form-group">
              <label class="form-label">Email Address</label>
              <input type="email" id="edit-pat-email" class="form-control" placeholder="patient@example.com" />
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Residential Address *</label>
            <input type="text" id="edit-pat-address" class="form-control" required placeholder="Flat, Street, City, State" />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Documented Allergies</label>
              <input type="text" id="edit-pat-allergies" class="form-control" placeholder="e.g. Penicillin, Peanuts (or None)" />
            </div>
            <div class="form-group">
              <label class="form-label">Chronic Conditions</label>
              <input type="text" id="edit-pat-chronic" class="form-control" placeholder="e.g. Hypertension, Type-2 Diabetes (or None)" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Emergency Contact Name</label>
              <input type="text" id="edit-pat-em-name" class="form-control" placeholder="Next of Kin / Relative Name" />
            </div>
            <div class="form-group">
              <label class="form-label">Emergency Contact Phone</label>
              <input type="tel" id="edit-pat-em-phone" class="form-control" placeholder="10-digit contact number" />
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" onclick="closeModal('modal-edit-patient')">Cancel</button>
          <button type="submit" class="btn btn-primary" id="btn-save-patient-edit">💾 Save Patient Details</button>
        </div>
      </form>
    </div>
  </div>
'''

target_tag = '  <!-- Toast Notification Container -->'
assert target_tag in html, "Could not find Toast Container in index.html"
html = html.replace(target_tag, new_modals + '\n' + target_tag)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html successfully! New length:", len(html))
