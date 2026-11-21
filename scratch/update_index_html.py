import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add Staff Profile to sidebar nav under Overview
old_sidebar_overview = """        <div class="nav-section-title">Overview</div>
        <button class="nav-link active" data-page="page-home" onclick="showPage('page-home')">
          <span class="nav-icon"><i data-lucide="layout-dashboard">📊</i></span>
          <span>Command Center</span>
        </button>"""

new_sidebar_overview = """        <div class="nav-section-title">Overview</div>
        <button class="nav-link active" data-page="page-home" onclick="showPage('page-home')">
          <span class="nav-icon"><i data-lucide="layout-dashboard">📊</i></span>
          <span>Command Center</span>
        </button>
        <button class="nav-link" data-page="page-profile" onclick="showPage('page-profile')">
          <span class="nav-icon"><i data-lucide="user">👤</i></span>
          <span>Staff Profile</span>
        </button>"""

if 'data-page="page-profile"' not in html:
    html = html.replace(old_sidebar_overview, new_sidebar_overview)

# 2. Update sidebar footer to have user summary chip + Sign Out button
old_sidebar_footer = """      <div class="sidebar-footer">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <div style="font-size:0.75rem; color:var(--text-muted);">
            <div><strong>MediLink v3.0</strong> Enterprise</div>
            <div style="color:var(--success); font-weight:600">● Relational Core Active</div>
          </div>
          <button class="btn-icon" onclick="switchView('landing')" title="View Public Homepage" style="font-size:0.85rem; width:28px; height:28px;">
            🏠
          </button>
        </div>
      </div>"""

new_sidebar_footer = """      <div class="sidebar-footer">
        <div class="sidebar-user-card" onclick="showPage('page-profile')" title="View Staff Profile" style="cursor:pointer; display:flex; align-items:center; gap:0.6rem; flex:1; min-width:0;">
          <div class="avatar-sm" id="sidebar-avatar-initials" style="width:34px; height:34px; border-radius:var(--radius-full); background:linear-gradient(135deg, var(--primary), var(--teal)); color:#fff; font-weight:700; font-size:0.8rem; display:flex; align-items:center; justify-content:center; flex-shrink:0;">SA</div>
          <div style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap; flex:1;">
            <div style="font-size:0.82rem; font-weight:700; color:var(--text); overflow:hidden; text-overflow:ellipsis; white-space:nowrap;" id="sidebar-user-name">System Administrator</div>
            <div style="font-size:0.7rem; color:var(--text-muted);" id="sidebar-user-role">Administrator</div>
          </div>
        </div>
        <button class="btn-icon" onclick="logoutUser()" title="Sign Out of MediLink" style="width:34px; height:34px; border-radius:var(--radius-md); color:var(--danger); border-color:rgba(239,68,68,0.2); background:var(--danger-light); flex-shrink:0;">
          🚪
        </button>
      </div>"""

if old_sidebar_footer in html:
    html = html.replace(old_sidebar_footer, new_sidebar_footer)

# 3. Replace header avatar & button with Profile Dropdown
old_header_avatar = """          <!-- Staff Profile Avatar & Logout Button -->
          <div style="display:flex; align-items:center; gap:0.6rem; margin-left:0.5rem; padding-left:0.5rem; border-left:1px solid var(--border);">
            <div style="width:32px; height:32px; border-radius:var(--radius-full); background:var(--primary-light); color:var(--primary); font-weight:700; font-size:0.82rem; display:flex; align-items:center; justify-content:center;" id="header-avatar-initials">
              SA
            </div>
            <button class="btn btn-secondary btn-sm" onclick="logoutUser()" title="Sign Out of Workspace" style="font-size:0.75rem; padding:4px 10px;">
              Sign Out
            </button>
          </div>"""

new_header_dropdown = """          <!-- Staff Profile Dropdown -->
          <div class="profile-dropdown-wrap" style="position:relative; margin-left:0.5rem;">
            <button class="profile-trigger-btn" id="header-profile-btn" onclick="toggleProfileDropdown(event)" title="Staff Account Menu">
              <div class="avatar-pill" id="header-avatar-initials">SA</div>
              <div class="profile-meta-text">
                <div class="profile-name-line" id="header-user-name">System Administrator</div>
                <div class="profile-role-line" id="header-user-role">Administrator</div>
              </div>
              <span class="dropdown-chevron">▾</span>
            </button>

            <!-- Dropdown Menu -->
            <div class="profile-dropdown-menu" id="header-profile-menu" style="display:none;">
              <div class="dropdown-user-info">
                <div class="dropdown-avatar" id="dropdown-avatar-initials">SA</div>
                <div class="dropdown-meta">
                  <strong id="dropdown-user-name">System Administrator</strong>
                  <span class="badge badge-primary" id="dropdown-user-role" style="display:inline-block; margin-top:2px; font-size:0.7rem;">Administrator</span>
                  <div style="font-size:0.75rem; color:var(--text-muted); margin-top:2px;" id="dropdown-user-facility">AIIMS Delhi</div>
                </div>
              </div>
              <div class="dropdown-divider"></div>
              <button class="dropdown-item" onclick="openProfilePage();">
                <i data-lucide="user">👤</i>
                <span>My Profile</span>
              </button>
              <button class="dropdown-item" onclick="openProfileSecurity();">
                <i data-lucide="key">🔒</i>
                <span>Account Security</span>
              </button>
              <button class="dropdown-item" onclick="toggleTheme(); closeProfileDropdown();">
                <i data-lucide="moon">🌓</i>
                <span>Toggle Theme</span>
              </button>
              <div class="dropdown-divider"></div>
              <button class="dropdown-item dropdown-item-danger" onclick="logoutUser(); closeProfileDropdown();">
                <i data-lucide="log-out">🚪</i>
                <span>Sign Out</span>
              </button>
            </div>
          </div>"""

if old_header_avatar in html:
    html = html.replace(old_header_avatar, new_header_dropdown)

# 4. Add page-profile section in content-viewport
profile_page_section = """        <!-- ==============================================================
             PAGE 16: STAFF PROFILE & SETTINGS
             ============================================================== -->
        <section id="page-profile" class="page">
          <!-- Profile Hero Banner -->
          <div class="profile-header-banner">
            <div class="profile-avatar-lg" id="profile-hero-avatar">SA</div>
            <div class="profile-meta-lg">
              <h2 id="profile-hero-name">System Administrator</h2>
              <div style="color:#94a3b8; font-size:0.9rem;" id="profile-hero-dept">Hospital Administration • Clinical Operations</div>
              <div class="profile-tags-row">
                <span class="badge badge-primary" id="profile-hero-role">Administrator</span>
                <span class="badge badge-info" id="profile-hero-facility">AIIMS Delhi (Node 01)</span>
                <span class="badge badge-success">● Active &amp; Authorized</span>
              </div>
            </div>
          </div>

          <div class="profile-grid-layout">
            <!-- Left Column: Personal & Contact Information -->
            <div class="card">
              <div class="card-header">
                <div class="card-title">👤 Staff Credentials &amp; Profile</div>
                <span class="badge badge-primary">Institutional EMR</span>
              </div>
              <form onsubmit="handleProfileUpdate(event)">
                <div class="form-row">
                  <div class="form-group">
                    <label class="form-label">Full Name *</label>
                    <input type="text" id="prof-fullname-input" class="form-control" required />
                  </div>
                  <div class="form-group">
                    <label class="form-label">Username (Immutable)</label>
                    <input type="text" id="prof-username-input" class="form-control" readonly disabled style="background:var(--bg-alt); cursor:not-allowed;" />
                  </div>
                </div>

                <div class="form-row">
                  <div class="form-group">
                    <label class="form-label">Institutional Role</label>
                    <input type="text" id="prof-role-input" class="form-control" readonly disabled style="background:var(--bg-alt); cursor:not-allowed;" />
                  </div>
                  <div class="form-group">
                    <label class="form-label">Assigned Facility Node</label>
                    <input type="text" id="prof-facility-input" class="form-control" readonly disabled style="background:var(--bg-alt); cursor:not-allowed;" />
                  </div>
                </div>

                <div class="form-row">
                  <div class="form-group">
                    <label class="form-label">Clinical Department</label>
                    <input type="text" id="prof-dept-input" class="form-control" readonly disabled style="background:var(--bg-alt); cursor:not-allowed;" />
                  </div>
                  <div class="form-group">
                    <label class="form-label">Account Status</label>
                    <input type="text" id="prof-status-input" class="form-control" value="Active / Verified" readonly disabled style="background:var(--bg-alt); cursor:not-allowed;" />
                  </div>
                </div>

                <div class="form-row">
                  <div class="form-group">
                    <label class="form-label">Workstation Email</label>
                    <input type="email" id="prof-email-input" class="form-control" placeholder="staff@medilink.hospital" />
                  </div>
                  <div class="form-group">
                    <label class="form-label">Direct Contact Phone</label>
                    <input type="text" id="prof-phone-input" class="form-control" placeholder="+91 98765 43210" />
                  </div>
                </div>

                <div style="display:flex; justify-content:flex-end; gap:0.5rem; margin-top:1.25rem;">
                  <button type="submit" class="btn btn-primary">💾 Save Profile Changes</button>
                </div>
              </form>
            </div>

            <!-- Right Column: Security & Preferences -->
            <div style="display:flex; flex-direction:column; gap:1.5rem;">
              <!-- Change Password Card -->
              <div class="card">
                <div class="card-header">
                  <div class="card-title">🔒 Account Security &amp; Password</div>
                  <span class="badge badge-warning">PBKDF2 SHA-256</span>
                </div>
                <form onsubmit="handleChangePassword(event)">
                  <div class="form-group">
                    <label class="form-label">Current Password *</label>
                    <input type="password" id="pw-current-input" class="form-control" required placeholder="Enter current password" />
                  </div>
                  <div class="form-group">
                    <label class="form-label">New Password * (Min. 6 chars)</label>
                    <input type="password" id="pw-new-input" class="form-control" required minlength="6" placeholder="Enter new password" />
                  </div>
                  <div class="form-group">
                    <label class="form-label">Confirm New Password *</label>
                    <input type="password" id="pw-confirm-input" class="form-control" required minlength="6" placeholder="Re-enter new password" />
                  </div>
                  <button type="submit" class="btn btn-secondary" style="width:100%; justify-content:center;">
                    🔑 Update Password
                  </button>
                </form>
              </div>

              <!-- Workstation Session Settings -->
              <div class="card">
                <div class="card-header">
                  <div class="card-title">🖥️ Workstation Session</div>
                  <span class="badge badge-success">Active Session</span>
                </div>
                <div style="font-size:0.82rem; color:var(--text-muted); display:flex; flex-direction:column; gap:0.6rem;">
                  <div>Interface Theme: <button class="btn btn-secondary btn-sm" onclick="toggleTheme()" style="margin-left:8px;">Toggle Theme 🌓</button></div>
                  <div>Database Core: <strong style="color:var(--text)">Dual Engine (SQLite / MySQL 8.0)</strong></div>
                  <div>Security Protocol: <strong style="color:var(--text)">HMAC-SHA256 Token Auth</strong></div>
                </div>
                <div style="margin-top:1.25rem; border-top:1px solid var(--border-light); padding-top:1rem;">
                  <button class="btn btn-danger" onclick="logoutUser()" style="width:100%; justify-content:center;">
                    🚪 Sign Out of Workstation
                  </button>
                </div>
              </div>
            </div>
          </div>
        </section>
"""

if 'id="page-profile"' not in html:
    # Insert right before </section>\n\n      </div>\n    </main>
    html = re.sub(
        r'(</section>\s*</div>\s*</main>)',
        r'</section>\n\n' + profile_page_section + r'\n      </div>\n    </main>',
        html
    )

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html updated successfully with Profile and Dropdown.")
