with open("static/js/app.js", "r", encoding="utf-8") as f:
    js = f.read()

# 1. Update switchView to guard protected app view and ensure default page is shown
old_switch_view = """function switchView(viewName) {
  document.querySelectorAll('.app-view').forEach(v => v.classList.remove('active'));
  const target = document.getElementById(`view-${viewName}`);
  if (target) {
    target.classList.add('active');
  }
  if (window.lucide && typeof window.lucide.createIcons === 'function') {
    window.lucide.createIcons();
  }
  window.scrollTo(0, 0);
}"""

new_switch_view = """function switchView(viewName) {
  if (viewName === 'app') {
    const token = window.api ? window.api.getToken() : null;
    if (!token) {
      toast('Please sign in to access the hospital command center.', true);
      switchView('login');
      return;
    }
  }

  document.querySelectorAll('.app-view').forEach(v => v.classList.remove('active'));
  const target = document.getElementById(`view-${viewName}`);
  if (target) {
    target.classList.add('active');
  }

  if (viewName === 'app') {
    const pageToLoad = appState.activePage || 'page-home';
    showPage(pageToLoad);
  }

  if (window.lucide && typeof window.lucide.createIcons === 'function') {
    window.lucide.createIcons();
  }
  window.scrollTo(0, 0);
}"""

if old_switch_view in js:
    js = js.replace(old_switch_view, new_switch_view)

# 2. Update performLogin to explicitly show page-home
old_perform_login = """async function performLogin(username, password) {
  try {
    const authData = await window.api.login(username, password);
    appState.currentUser = authData;
    updateUserInterface(authData);
    switchView('app');
    loadDashboard();
    toast(`Authenticated as ${authData.role} (${authData.full_name})`);
  } catch (err) {
    toast(`Authentication error: ${err.message}`, true);
  }
}"""

new_perform_login = """async function performLogin(username, password) {
  try {
    const authData = await window.api.login(username, password);
    appState.currentUser = authData;
    updateUserInterface(authData);
    switchView('app');
    showPage('page-home');
    loadDashboard();
    toast(`Welcome, ${authData.full_name} (${authData.role})`);
  } catch (err) {
    toast(`Authentication error: ${err.message}`, true);
  }
}"""

if old_perform_login in js:
    js = js.replace(old_perform_login, new_perform_login)

# 3. Update updateUserInterface to update all header, sidebar, and dropdown fields
old_update_ui = """function updateUserInterface(authData) {
  const label = document.getElementById('user-role-label');
  const nameLabel = document.getElementById('user-name-label');
  const welcomeName = document.getElementById('welcome-user-name');
  const avatarInitials = document.getElementById('header-avatar-initials');

  if (label) label.textContent = authData.role;
  if (nameLabel) nameLabel.textContent = authData.full_name;
  if (welcomeName) welcomeName.textContent = authData.full_name;

  if (avatarInitials && authData.full_name) {
    const parts = authData.full_name.split(' ');
    const initials = parts.length > 1 ? parts[0][0] + parts[1][0] : parts[0].slice(0, 2);
    avatarInitials.textContent = initials.toUpperCase();
  }

  const roleSelect = document.getElementById('active-role-select');
  if (roleSelect && authData.username) {
    roleSelect.value = authData.username;
  }

  applyRolePermissions(authData.role);
}"""

new_update_ui = """function updateUserInterface(authData) {
  if (!authData) return;
  const setTxt = (id, txt) => {
    const el = document.getElementById(id);
    if (el) el.textContent = txt;
  };

  setTxt('user-role-label', authData.role);
  setTxt('user-name-label', authData.full_name);
  setTxt('welcome-user-name', authData.full_name);
  setTxt('header-user-name', authData.full_name);
  setTxt('header-user-role', authData.role);
  setTxt('sidebar-user-name', authData.full_name);
  setTxt('sidebar-user-role', authData.role);
  setTxt('dropdown-user-name', authData.full_name);
  setTxt('dropdown-user-role', authData.role);
  setTxt('dropdown-user-facility', authData.hospital_name || 'AIIMS Delhi');

  const initials = authData.full_name
    ? authData.full_name.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()
    : 'SA';

  setTxt('header-avatar-initials', initials);
  setTxt('sidebar-avatar-initials', initials);
  setTxt('dropdown-avatar-initials', initials);

  const roleSelect = document.getElementById('active-role-select');
  if (roleSelect && authData.username) {
    roleSelect.value = authData.username;
  }

  applyRolePermissions(authData.role);
}"""

if old_update_ui in js:
    js = js.replace(old_update_ui, new_update_ui)

# 4. Update logoutUser
old_logout = """function logoutUser() {
  if (window.api) {
    window.api.setToken(null);
  }
  appState.currentUser = null;
  toast('Signed out of MediLink workspace');
  switchView('landing');
}"""

new_logout = """async function logoutUser() {
  try {
    if (window.api) {
      await window.api.logout();
    }
  } catch (e) {
    console.warn('Logout notice:', e);
  }
  if (window.api) {
    window.api.setToken(null);
  }
  appState.currentUser = null;
  closeProfileDropdown();
  
  const welcomeName = document.getElementById('welcome-user-name');
  if (welcomeName) welcomeName.textContent = 'Staff Member';
  
  toast('Signed out of MediLink workspace successfully');
  switchView('landing');
}"""

if old_logout in js:
    js = js.replace(old_logout, new_logout)

# 5. Add dropdown and profile methods if not present
dropdown_and_profile_methods = """
// ==========================================================================
// PROFILE DROPDOWN & PROFILE PAGE CONTROLLER (Tasks 3, 4, 5)
// ==========================================================================

function toggleProfileDropdown(e) {
  if (e) e.stopPropagation();
  const menu = document.getElementById('header-profile-menu');
  if (menu) {
    const isVisible = menu.style.display === 'block';
    menu.style.display = isVisible ? 'none' : 'block';
  }
}

function closeProfileDropdown() {
  const menu = document.getElementById('header-profile-menu');
  if (menu) menu.style.display = 'none';
}

function openProfilePage() {
  closeProfileDropdown();
  showPage('page-profile');
}

function openProfileSecurity() {
  closeProfileDropdown();
  showPage('page-profile');
  setTimeout(() => {
    const pwInput = document.getElementById('pw-current-input');
    if (pwInput) pwInput.focus();
  }, 100);
}

// Global click-outside listener to close dropdowns
document.addEventListener('click', (e) => {
  const profileWrap = document.querySelector('.profile-dropdown-wrap');
  if (profileWrap && !profileWrap.contains(e.target)) {
    closeProfileDropdown();
  }
  const notifDropdown = document.getElementById('notifications-dropdown');
  const notifBtn = document.getElementById('btn-notifications');
  if (notifDropdown && notifBtn && !notifDropdown.contains(e.target) && !notifBtn.contains(e.target)) {
    notifDropdown.style.display = 'none';
  }
});

// Escape key closes dropdowns
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeProfileDropdown();
    const notifDropdown = document.getElementById('notifications-dropdown');
    if (notifDropdown) notifDropdown.style.display = 'none';
  }
});

async function loadUserProfile() {
  try {
    const me = await window.api.getMe();
    appState.currentUser = me;
    
    const setVal = (id, val) => {
      const el = document.getElementById(id);
      if (el) el.value = val || '';
    };
    const setTxt = (id, txt) => {
      const el = document.getElementById(id);
      if (el) el.textContent = txt || '';
    };

    setTxt('profile-hero-name', me.full_name);
    setTxt('profile-hero-role', me.role);
    setTxt('profile-hero-dept', `${me.department || 'Clinical Medicine'} • Hospital Network Node`);
    setTxt('profile-hero-facility', me.hospital_name || 'AIIMS New Delhi');
    
    const initials = me.full_name ? me.full_name.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase() : 'SA';
    setTxt('profile-hero-avatar', initials);

    setVal('prof-fullname-input', me.full_name);
    setVal('prof-username-input', me.username);
    setVal('prof-role-input', me.role);
    setVal('prof-facility-input', me.hospital_name || 'AIIMS New Delhi');
    setVal('prof-dept-input', me.department || 'Clinical Medicine');
    setVal('prof-email-input', me.email);
    setVal('prof-phone-input', me.phone);
  } catch (err) {
    console.error('Failed to load user profile:', err);
    toast(`Could not load profile: ${err.message}`, true);
  }
}

async function handleProfileUpdate(e) {
  if (e) e.preventDefault();
  const fullName = document.getElementById('prof-fullname-input')?.value;
  const email = document.getElementById('prof-email-input')?.value;
  const phone = document.getElementById('prof-phone-input')?.value;

  try {
    const updated = await window.api.updateProfile({
      full_name: fullName,
      email: email,
      phone: phone
    });
    appState.currentUser = updated;
    updateUserInterface(updated);
    loadUserProfile();
    toast('Profile updated successfully!');
  } catch (err) {
    toast(`Failed to update profile: ${err.message}`, true);
  }
}

async function handleChangePassword(e) {
  if (e) e.preventDefault();
  const currentPw = document.getElementById('pw-current-input')?.value;
  const newPw = document.getElementById('pw-new-input')?.value;
  const confirmPw = document.getElementById('pw-confirm-input')?.value;

  if (newPw !== confirmPw) {
    toast('New passwords do not match!', true);
    return;
  }
  if (newPw.length < 6) {
    toast('New password must be at least 6 characters!', true);
    return;
  }

  try {
    await window.api.changePassword(currentPw, newPw);
    toast('Password changed successfully! Please keep your new password safe.');
    const elCurrent = document.getElementById('pw-current-input');
    const elNew = document.getElementById('pw-new-input');
    const elConfirm = document.getElementById('pw-confirm-input');
    if (elCurrent) elCurrent.value = '';
    if (elNew) elNew.value = '';
    if (elConfirm) elConfirm.value = '';
  } catch (err) {
    toast(`Password update failed: ${err.message}`, true);
  }
}
"""

if "function toggleProfileDropdown" not in js:
    # Insert right before showPage
    js = js.replace("// ==========================================================================\n// NAVIGATION & THEME", dropdown_and_profile_methods + "\n// ==========================================================================\n// NAVIGATION & THEME")

# 6. Update pageTitles in showPage to include page-profile
old_page_titles = """    'page-sql': 'SQL DBMS Query Workbench',
    'page-backup': 'Database Engine & Health'
  };"""

new_page_titles = """    'page-sql': 'SQL DBMS Query Workbench',
    'page-backup': 'Database Engine & Health',
    'page-profile': 'Staff Profile & Settings'
  };"""

if old_page_titles in js:
    js = js.replace(old_page_titles, new_page_titles)

# 7. In showPage, call loadUserProfile if page-profile is activated
old_show_page_triggers = """  if (pageId === 'page-sql') loadSqlWorkbench();
  if (pageId === 'page-backup') loadBackupStatus();"""

new_show_page_triggers = """  if (pageId === 'page-sql') loadSqlWorkbench();
  if (pageId === 'page-backup') loadBackupStatus();
  if (pageId === 'page-profile') loadUserProfile();"""

if old_show_page_triggers in js:
    js = js.replace(old_show_page_triggers, new_show_page_triggers)

# 8. Update DOMContentLoaded for clean session restoration (Task 6)
old_dom_loaded = """window.addEventListener('DOMContentLoaded', async () => {
  initTheme();
  await initAuth();
  
  const hash = window.location.hash;
  if (hash === '#app' && window.api && window.api.getToken()) {
    switchView('app');
    loadDashboard();
  } else if (hash === '#login') {
    switchView('login');
  } else {
    switchView('landing');
  }

  loadNotifications();
  if (window.lucide && typeof window.lucide.createIcons === 'function') {
    window.lucide.createIcons();
  }

  // Keyboard shortcut Ctrl+K for global search
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      const input = document.getElementById('global-search-input');
      if (input) input.focus();
    }
  });
});"""

new_dom_loaded = """window.addEventListener('DOMContentLoaded', async () => {
  initTheme();
  
  const savedToken = window.api ? window.api.getToken() : null;
  if (savedToken) {
    try {
      const me = await window.api.getMe();
      appState.currentUser = me;
      updateUserInterface(me);
      await initRoleSelector();
      switchView('app');
      showPage(appState.activePage || 'page-home');
    } catch (e) {
      console.warn('Session expired or invalid:', e);
      window.api.setToken(null);
      switchView('landing');
      toast('Previous session expired. Please sign in.');
    }
  } else {
    await initRoleSelector();
    const hash = window.location.hash;
    if (hash === '#login') {
      switchView('login');
    } else {
      switchView('landing');
    }
  }

  loadNotifications();
  if (window.lucide && typeof window.lucide.createIcons === 'function') {
    window.lucide.createIcons();
  }

  // Keyboard shortcut Ctrl+K for global search
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      const input = document.getElementById('global-search-input');
      if (input) input.focus();
    }
  });
});"""

if old_dom_loaded in js:
    js = js.replace(old_dom_loaded, new_dom_loaded)

# Also define initRoleSelector if not present
if "async function initRoleSelector" not in js:
    role_selector_fn = """
async function initRoleSelector() {
  try {
    const roles = await window.api.getRoles();
    const roleSelect = document.getElementById('active-role-select');
    if (roleSelect && roles) {
      roleSelect.innerHTML = roles.map(r => 
        `<option value="${r.username}">${r.role} (${r.username})</option>`
      ).join('');
    }
  } catch (err) {
    console.warn('Role selector init error:', err);
  }
}
"""
    js = js.replace("async function initAuth() {", role_selector_fn + "\nasync function initAuth() {")

with open("static/js/app.js", "w", encoding="utf-8") as f:
    f.write(js)

print("static/js/app.js updated successfully.")
