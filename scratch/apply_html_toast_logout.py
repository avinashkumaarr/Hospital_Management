with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Sidebar Footer in index.html
old_sidebar_footer = '''      <div class="sidebar-footer">
        <div class="sidebar-user-card" onclick="showPage('page-profile')" title="View Staff Profile" style="cursor:pointer; display:flex; align-items:center; gap:0.6rem; flex:1; min-width:0;">
          <div class="avatar-sm" id="sidebar-avatar-initials" style="width:34px; height:34px; border-radius:var(--radius-full); background:linear-gradient(135deg, var(--primary), var(--teal)); color:#fff; font-weight:700; font-size:0.8rem; display:flex; align-items:center; justify-content:center; flex-shrink:0;">SA</div>
          <div style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap; flex:1;">
            <div style="font-size:0.82rem; font-weight:700; color:var(--text); overflow:hidden; text-overflow:ellipsis; white-space:nowrap;" id="sidebar-user-name">System Administrator</div>
            <div style="font-size:0.7rem; color:var(--text-muted);" id="sidebar-user-role">Administrator</div>
          </div>
        </div>
        <button class="btn-icon" id="btn-sidebar-logout" onclick="logoutUser()" title="Sign Out of MediLink" style="width:34px; height:34px; border-radius:var(--radius-md); color:var(--danger); border-color:rgba(239,68,68,0.2); background:var(--danger-light); flex-shrink:0;">
          🚪
        </button>
      </div>'''

new_sidebar_footer = '''      <div class="sidebar-footer">
        <div class="sidebar-user-card" onclick="showPage('page-profile')" title="View Staff Profile">
          <div class="avatar-sm" id="sidebar-avatar-initials">SA</div>
          <div class="sidebar-user-meta">
            <div id="sidebar-user-name">System Administrator</div>
            <div id="sidebar-user-role">Administrator</div>
          </div>
        </div>
        <button class="btn-logout-red" id="btn-sidebar-logout" onclick="logoutUser()" title="Sign Out of MediLink">
          <span class="btn-logout-icon">🚪</span>
          <span class="btn-logout-label">Logout</span>
        </button>
      </div>'''

assert old_sidebar_footer in html, "Could not find old_sidebar_footer"
html = html.replace(old_sidebar_footer, new_sidebar_footer)

# 2. Add visible red Logout button in Topbar Header
old_header_actions = '''          <!-- Staff Profile Dropdown -->
          <div class="profile-dropdown-wrap" style="position:relative; margin-left:0.5rem;">'''

new_header_actions = '''          <!-- Topbar Logout Button -->
          <button class="btn-logout-header" id="btn-header-logout" onclick="logoutUser()" title="Logout of MediLink">
            <span class="btn-logout-icon">🚪</span>
            <span class="btn-logout-label">Logout</span>
          </button>

          <!-- Staff Profile Dropdown -->
          <div class="profile-dropdown-wrap" style="position:relative; margin-left:0.35rem;">'''

assert old_header_actions in html, "Could not find old_header_actions"
html = html.replace(old_header_actions, new_header_actions)

# 3. Clean welcome-banner inline styles in #page-home
old_welcome_banner = '''          <!-- Welcome Greeting Banner -->
          <div class="welcome-banner" style="display:flex; justify-content:space-between; align-items:center; background:linear-gradient(135deg, rgba(37,99,235,0.08), rgba(13,148,136,0.08)); border:1px solid var(--border); border-radius:var(--radius-lg); padding:1.25rem 1.5rem; margin-bottom:1.5rem; flex-wrap:wrap; gap:1rem;">
            <div>
              <h2 style="font-family:var(--font-heading); font-size:1.35rem; font-weight:800; color:var(--text);">
                Welcome back, <span id="welcome-user-name">System Administrator</span> 👋
              </h2>
              <p style="font-size:0.85rem; color:var(--text-muted); margin-top:2px;">
                Hospital Operations &amp; Unified Clinical Records Network • Active Node: <span id="welcome-facility-node" style="font-weight:600; color:var(--primary);">AIIMS Delhi (Node 01)</span>
              </p>
            </div>
            <div style="display:flex; gap:0.6rem; align-items:center;">
              <button class="btn btn-secondary btn-sm" onclick="showPage('page-encounter')">
                🩺 + New Consultation
              </button>
              <button class="btn btn-primary btn-sm" onclick="showPage('page-register')">
                👥 Enroll Patient
              </button>
            </div>
          </div>'''

new_welcome_banner = '''          <!-- Welcome Greeting Banner -->
          <div class="welcome-banner">
            <div>
              <h2 class="welcome-banner-title">
                Welcome back, <span id="welcome-user-name">System Administrator</span> 👋
              </h2>
              <p class="welcome-banner-sub">
                Hospital Operations &amp; Unified Clinical Records Network • Active Node: <span id="welcome-facility-node" style="font-weight:700; color:var(--primary);">AIIMS Delhi (Node 01)</span>
              </p>
            </div>
            <div class="welcome-banner-actions">
              <button class="btn btn-secondary btn-sm" onclick="showPage('page-encounter')">
                🩺 + New Consultation
              </button>
              <button class="btn btn-primary btn-sm" onclick="showPage('page-register')">
                👥 Enroll Patient
              </button>
            </div>
          </div>'''

assert old_welcome_banner in html, "Could not find old_welcome_banner"
html = html.replace(old_welcome_banner, new_welcome_banner)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Successfully updated index.html!")
