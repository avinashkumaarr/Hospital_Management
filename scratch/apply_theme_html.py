with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add theme initializer in <head>
old_head = '''  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>MediLink Enterprise v4.0 — Hospital Management & Unified Medical Records Network</title>'''

new_head = '''  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>MediLink Enterprise v4.0 — Hospital Management & Unified Medical Records Network</title>
  
  <!-- Immediate Theme Initializer: Prevents flash of wrong theme -->
  <script>
    (function() {
      try {
        var pref = localStorage.getItem('medilink-theme') || localStorage.getItem('medilink_theme') || 'system';
        if (!['system', 'light', 'dark', 'midnight'].includes(pref)) pref = 'system';
        var resolved = pref;
        if (pref === 'system') {
          var isDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
          resolved = isDark ? 'dark' : 'light';
        }
        document.documentElement.setAttribute('data-theme', resolved);
        document.documentElement.setAttribute('data-theme-preference', pref);
      } catch (e) {}
    })();
  </script>'''

assert old_head in html, "Could not find old_head in index.html"
html = html.replace(old_head, new_head)

# 2. Update landing navbar theme button
old_landing_theme = '<button class="btn-icon" onclick="toggleTheme()" title="Toggle Dark/Light Theme">🌓</button>'
new_landing_theme = '''<div class="theme-dropdown-wrap" style="position:relative;">
            <button class="btn-icon" id="landing-theme-toggle" onclick="toggleLandingThemeMenu(event)" title="Interface Theme (System, Light, Dark, Midnight)">
              <span id="landing-theme-btn-icon">💻</span>
            </button>
            <div class="theme-dropdown-menu" id="landing-theme-dropdown-menu" style="display:none;">
              <div class="theme-menu-header">Interface Theme</div>
              <button class="theme-menu-item" data-theme-val="system" onclick="setAppTheme('system'); closeLandingThemeMenu();">
                <span class="theme-menu-icon">💻</span>
                <span class="theme-menu-label">System Default</span>
                <span class="theme-menu-check">✓</span>
              </button>
              <button class="theme-menu-item" data-theme-val="light" onclick="setAppTheme('light'); closeLandingThemeMenu();">
                <span class="theme-menu-icon">☀️</span>
                <span class="theme-menu-label">Light</span>
                <span class="theme-menu-check">✓</span>
              </button>
              <button class="theme-menu-item" data-theme-val="dark" onclick="setAppTheme('dark'); closeLandingThemeMenu();">
                <span class="theme-menu-icon">🌙</span>
                <span class="theme-menu-label">Dark</span>
                <span class="theme-menu-check">✓</span>
              </button>
              <button class="theme-menu-item" data-theme-val="midnight" onclick="setAppTheme('midnight'); closeLandingThemeMenu();">
                <span class="theme-menu-icon">🌌</span>
                <span class="theme-menu-label">Midnight Blue</span>
                <span class="theme-menu-check">✓</span>
              </button>
            </div>
          </div>'''

assert old_landing_theme in html, "Could not find old_landing_theme in index.html"
html = html.replace(old_landing_theme, new_landing_theme, 1)

# 3. Update topbar header theme button
old_topbar_theme = '''          <!-- Theme Toggle Button -->
          <button class="btn-icon" onclick="toggleTheme()" title="Toggle Clinical Night Shift / Light Theme">🌓</button>'''

new_topbar_theme = '''          <!-- Theme Toggle Dropdown Menu (Requirement 4) -->
          <div class="theme-dropdown-wrap" style="position:relative;">
            <button class="btn-icon" id="btn-theme-toggle" onclick="toggleThemeMenu(event)" title="Interface Theme (System, Light, Dark, Midnight)">
              <span id="theme-btn-icon">💻</span>
            </button>
            <div class="theme-dropdown-menu" id="theme-dropdown-menu" style="display:none;">
              <div class="theme-menu-header">Interface Theme</div>
              <button class="theme-menu-item" data-theme-val="system" onclick="setAppTheme('system'); closeThemeMenu();">
                <span class="theme-menu-icon">💻</span>
                <span class="theme-menu-label">System Default</span>
                <span class="theme-menu-check">✓</span>
              </button>
              <button class="theme-menu-item" data-theme-val="light" onclick="setAppTheme('light'); closeThemeMenu();">
                <span class="theme-menu-icon">☀️</span>
                <span class="theme-menu-label">Light</span>
                <span class="theme-menu-check">✓</span>
              </button>
              <button class="theme-menu-item" data-theme-val="dark" onclick="setAppTheme('dark'); closeThemeMenu();">
                <span class="theme-menu-icon">🌙</span>
                <span class="theme-menu-label">Dark</span>
                <span class="theme-menu-check">✓</span>
              </button>
              <button class="theme-menu-item" data-theme-val="midnight" onclick="setAppTheme('midnight'); closeThemeMenu();">
                <span class="theme-menu-icon">🌌</span>
                <span class="theme-menu-label">Midnight Blue</span>
                <span class="theme-menu-check">✓</span>
              </button>
            </div>
          </div>'''

assert old_topbar_theme in html, "Could not find old_topbar_theme in index.html"
html = html.replace(old_topbar_theme, new_topbar_theme)

# 4. Update profile dropdown menu item
old_profile_theme_item = '''              <button class="dropdown-item" onclick="toggleTheme(); closeProfileDropdown();">
                <i data-lucide="moon">🌓</i>
                <span>Toggle Theme</span>
              </button>'''

new_profile_theme_item = '''              <button class="dropdown-item" onclick="openProfileAppearance(); closeProfileDropdown();">
                <i data-lucide="palette">🎨</i>
                <span>Appearance &amp; Theme</span>
              </button>'''

assert old_profile_theme_item in html, "Could not find old_profile_theme_item in index.html"
html = html.replace(old_profile_theme_item, new_profile_theme_item)

# 5. Add Appearance Section in #page-profile (Requirement 3)
old_workstation_card = '''              <!-- Workstation Session Settings -->
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
                  <button class="btn btn-danger" id="btn-profile-logout" onclick="logoutUser()" style="width:100%; justify-content:center;">
                    🚪 Sign Out of Workstation
                  </button>
                </div>
              </div>'''

new_workstation_and_appearance = '''              <!-- Workstation Session Settings -->
              <div class="card">
                <div class="card-header">
                  <div class="card-title">🖥️ Workstation Session</div>
                  <span class="badge badge-success">Active Session</span>
                </div>
                <div style="font-size:0.82rem; color:var(--text-muted); display:flex; flex-direction:column; gap:0.6rem;">
                  <div>Database Core: <strong style="color:var(--text)">Dual Engine (SQLite / MySQL 8.0)</strong></div>
                  <div>Security Protocol: <strong style="color:var(--text)">HMAC-SHA256 Token Auth</strong></div>
                  <div>Appearance Mode: <strong id="profile-current-theme-label" style="color:var(--primary)">System Default</strong></div>
                </div>
                <div style="margin-top:1.25rem; border-top:1px solid var(--border-light); padding-top:1rem;">
                  <button class="btn-logout-red" id="btn-profile-logout" onclick="logoutUser()" style="width:100%; justify-content:center; padding:0.65rem 1rem;">
                    <span class="btn-logout-icon">🚪</span>
                    <span class="btn-logout-label">Logout of Workstation</span>
                  </button>
                </div>
              </div>

              <!-- Appearance & Theme Customization (Requirement 3) -->
              <div class="card" id="settings-appearance-card" style="margin-top:1.5rem; grid-column:1 / -1;">
                <div class="card-header">
                  <div>
                    <div class="card-title">🎨 Appearance &amp; Interface Theme</div>
                    <div style="font-size:0.8rem; color:var(--text-muted); margin-top:2px;">
                      Choose your clinical interface appearance or automatically follow your operating system appearance.
                    </div>
                  </div>
                  <span class="badge badge-info" id="current-theme-badge">System Default</span>
                </div>

                <div class="theme-cards-grid">
                  <!-- Option 1: System Default -->
                  <div class="theme-preview-card" data-theme-opt="system" onclick="setAppTheme('system')">
                    <div class="theme-mini-preview preview-system">
                      <div class="mini-bar"></div>
                      <div class="mini-body">
                        <div class="mini-side"></div>
                        <div class="mini-content">
                          <div class="mini-kpi"></div>
                          <div class="mini-kpi"></div>
                          <div class="mini-chart"></div>
                        </div>
                      </div>
                    </div>
                    <div class="theme-card-info">
                      <div class="theme-card-title">
                        <span class="theme-opt-icon">💻</span>
                        <strong>System Default</strong>
                      </div>
                      <div class="theme-card-desc">Automatically adapts to your operating system appearance in real time.</div>
                    </div>
                    <div class="theme-card-check">✓</div>
                  </div>

                  <!-- Option 2: Light -->
                  <div class="theme-preview-card" data-theme-opt="light" onclick="setAppTheme('light')">
                    <div class="theme-mini-preview preview-light">
                      <div class="mini-bar"></div>
                      <div class="mini-body">
                        <div class="mini-side"></div>
                        <div class="mini-content">
                          <div class="mini-kpi"></div>
                          <div class="mini-kpi"></div>
                          <div class="mini-chart"></div>
                        </div>
                      </div>
                    </div>
                    <div class="theme-card-info">
                      <div class="theme-card-title">
                        <span class="theme-opt-icon">☀️</span>
                        <strong>Clinical Light</strong>
                      </div>
                      <div class="theme-card-desc">Modern white healthcare surface with royal blue and clinical teal accents.</div>
                    </div>
                    <div class="theme-card-check">✓</div>
                  </div>

                  <!-- Option 3: Dark -->
                  <div class="theme-preview-card" data-theme-opt="dark" onclick="setAppTheme('dark')">
                    <div class="theme-mini-preview preview-dark">
                      <div class="mini-bar"></div>
                      <div class="mini-body">
                        <div class="mini-side"></div>
                        <div class="mini-content">
                          <div class="mini-kpi"></div>
                          <div class="mini-kpi"></div>
                          <div class="mini-chart"></div>
                        </div>
                      </div>
                    </div>
                    <div class="theme-card-info">
                      <div class="theme-card-title">
                        <span class="theme-opt-icon">🌙</span>
                        <strong>Slate Dark</strong>
                      </div>
                      <div class="theme-card-desc">Low-glare dark slate background optimized for night shift comfort.</div>
                    </div>
                    <div class="theme-card-check">✓</div>
                  </div>

                  <!-- Option 4: Midnight Blue -->
                  <div class="theme-preview-card" data-theme-opt="midnight" onclick="setAppTheme('midnight')">
                    <div class="theme-mini-preview preview-midnight">
                      <div class="mini-bar"></div>
                      <div class="mini-body">
                        <div class="mini-side"></div>
                        <div class="mini-content">
                          <div class="mini-kpi"></div>
                          <div class="mini-kpi"></div>
                          <div class="mini-chart"></div>
                        </div>
                      </div>
                    </div>
                    <div class="theme-card-info">
                      <div class="theme-card-title">
                        <span class="theme-opt-icon">🌌</span>
                        <strong>Midnight Blue</strong>
                      </div>
                      <div class="theme-card-desc">Deep navy enterprise hospital theme with high-contrast cyan accents.</div>
                    </div>
                    <div class="theme-card-check">✓</div>
                  </div>
                </div>
              </div>'''

assert old_workstation_card in html, "Could not find old_workstation_card in index.html"
html = html.replace(old_workstation_card, new_workstation_and_appearance)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html updated successfully with complete theme markup!")
