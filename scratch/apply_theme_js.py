import re

with open('static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Replace toggleTheme() and initTheme()
old_theme_block = '''function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme') || 'light';
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('medilink_theme', next);
  toast(`Switched to ${next === 'dark' ? 'Night Shift Clinical' : 'Clinical Light'} mode`);
}

function initTheme() {
  const saved = localStorage.getItem('medilink_theme') || 'light';
  document.documentElement.setAttribute('data-theme', saved);
}'''

new_theme_block = '''// ==========================================================================
// THEME CUSTOMIZATION SYSTEM (Requirement: 4 Theme Options + Real OS Auto-detect)
// Options: 'system', 'light', 'dark', 'midnight'
// ==========================================================================

const THEME_STORAGE_KEY = 'medilink-theme';
const LEGACY_THEME_STORAGE_KEY = 'medilink_theme';
const THEME_OPTIONS = ['system', 'light', 'dark', 'midnight'];
const THEME_META = {
  system: { name: 'System Default', icon: '💻', desc: 'Automatically follows operating system appearance' },
  light: { name: 'Clinical Light', icon: '☀️', desc: 'Modern white healthcare dashboard with blue and teal accents' },
  dark: { name: 'Slate Dark', icon: '🌙', desc: 'Elegant dark slate dashboard with comfortable contrast' },
  midnight: { name: 'Midnight Blue', icon: '🌌', desc: 'Premium deep navy hospital dashboard' }
};

const systemThemeMediaQuery = (typeof window !== 'undefined' && window.matchMedia) 
  ? window.matchMedia('(prefers-color-scheme: dark)') 
  : null;

let isSystemListenerActive = false;

function handleSystemThemeChange(e) {
  const pref = getStoredThemePreference();
  if (pref === 'system') {
    const resolved = e.matches ? 'dark' : 'light';
    applyThemeToDOM('system', resolved);
    console.log(`[MediLink Theme] System OS appearance changed -> resolved to: ${resolved}`);
  }
}

function ensureSystemListener(enable) {
  if (!systemThemeMediaQuery) return;
  try {
    if (enable && !isSystemListenerActive) {
      if (typeof systemThemeMediaQuery.addEventListener === 'function') {
        systemThemeMediaQuery.addEventListener('change', handleSystemThemeChange);
      } else if (typeof systemThemeMediaQuery.addListener === 'function') {
        systemThemeMediaQuery.addListener(handleSystemThemeChange);
      }
      isSystemListenerActive = true;
    } else if (!enable && isSystemListenerActive) {
      if (typeof systemThemeMediaQuery.removeEventListener === 'function') {
        systemThemeMediaQuery.removeEventListener('change', handleSystemThemeChange);
      } else if (typeof systemThemeMediaQuery.removeListener === 'function') {
        systemThemeMediaQuery.removeListener(handleSystemThemeChange);
      }
      isSystemListenerActive = false;
    }
  } catch (err) {
    console.warn('Theme listener management warning:', err);
  }
}

function getStoredThemePreference() {
  try {
    const stored = localStorage.getItem(THEME_STORAGE_KEY) || localStorage.getItem(LEGACY_THEME_STORAGE_KEY);
    if (stored && THEME_OPTIONS.includes(stored)) {
      return stored;
    }
  } catch (e) {}
  return 'system'; // System Default is the default for users who haven't selected a theme
}

function resolveEffectiveTheme(pref) {
  if (pref === 'system') {
    const isDark = systemThemeMediaQuery && systemThemeMediaQuery.matches;
    return isDark ? 'dark' : 'light';
  }
  return pref;
}

function updateDashboardChartsTheme(resolvedTheme) {
  if (typeof window === 'undefined' || !window.Chart) return;
  const isDark = resolvedTheme === 'dark' || resolvedTheme === 'midnight';
  const textColor = isDark ? '#94a3b8' : '#64748b';
  const gridColor = resolvedTheme === 'midnight' 
    ? 'rgba(30, 53, 103, 0.45)' 
    : (isDark ? 'rgba(51, 65, 85, 0.4)' : 'rgba(226, 232, 240, 0.7)');

  window.Chart.defaults.color = textColor;
  window.Chart.defaults.borderColor = gridColor;

  if (typeof appState !== 'undefined' && appState.charts) {
    if (appState.charts.deptVolume) {
      try {
        if (appState.charts.deptVolume.options && appState.charts.deptVolume.options.plugins && appState.charts.deptVolume.options.plugins.legend) {
          appState.charts.deptVolume.options.plugins.legend.labels.color = textColor;
        }
        appState.charts.deptVolume.update();
      } catch (e) {}
    }
    if (appState.charts.hospitalVolume) {
      try {
        if (appState.charts.hospitalVolume.options && appState.charts.hospitalVolume.options.scales) {
          const scales = appState.charts.hospitalVolume.options.scales;
          if (scales.x) {
            if (scales.x.ticks) scales.x.ticks.color = textColor;
            if (scales.x.grid) scales.x.grid.color = gridColor;
          }
          if (scales.y) {
            if (scales.y.ticks) scales.y.ticks.color = textColor;
            if (scales.y.grid) scales.y.grid.color = gridColor;
          }
        }
        appState.charts.hospitalVolume.update();
      } catch (e) {}
    }
  }
}

function applyThemeToDOM(pref, resolved) {
  document.documentElement.setAttribute('data-theme', resolved);
  document.documentElement.setAttribute('data-theme-preference', pref);

  // Update theme icons in topbar and landing bar buttons
  const meta = THEME_META[pref] || THEME_META.system;
  const themeIcon = meta.icon;
  const topbarIconEl = document.getElementById('theme-btn-icon');
  if (topbarIconEl) topbarIconEl.textContent = themeIcon;
  const landingIconEl = document.getElementById('landing-theme-btn-icon');
  if (landingIconEl) landingIconEl.textContent = themeIcon;

  // Update badges and labels in profile and appearance settings
  const profileLabel = document.getElementById('profile-current-theme-label');
  if (profileLabel) {
    profileLabel.textContent = pref === 'system' 
      ? `System Default (${resolved === 'dark' ? 'Dark' : 'Light'})`
      : meta.name;
  }
  const currentBadge = document.getElementById('current-theme-badge');
  if (currentBadge) {
    currentBadge.textContent = pref === 'system'
      ? `System Default (${resolved === 'dark' ? 'Dark' : 'Light'})`
      : meta.name;
  }

  // Update active checkmarks in topbar dropdown menu & landing dropdown menu
  document.querySelectorAll('.theme-menu-item').forEach(item => {
    const itemVal = item.getAttribute('data-theme-val');
    if (itemVal === pref) {
      item.classList.add('active');
    } else {
      item.classList.remove('active');
    }
  });

  // Update active state on Appearance Settings preview cards
  document.querySelectorAll('.theme-preview-card').forEach(card => {
    const cardOpt = card.getAttribute('data-theme-opt');
    if (cardOpt === pref) {
      card.classList.add('active');
    } else {
      card.classList.remove('active');
    }
  });

  // Update Chart.js colors
  updateDashboardChartsTheme(resolved);
}

function setAppTheme(themeVal, notify = true) {
  if (!THEME_OPTIONS.includes(themeVal)) themeVal = 'system';
  try {
    localStorage.setItem(THEME_STORAGE_KEY, themeVal);
    localStorage.setItem(LEGACY_THEME_STORAGE_KEY, themeVal);
  } catch (e) {}

  const resolved = resolveEffectiveTheme(themeVal);
  ensureSystemListener(themeVal === 'system');
  applyThemeToDOM(themeVal, resolved);

  if (notify && typeof toast === 'function') {
    const meta = THEME_META[themeVal] || THEME_META.system;
    const note = themeVal === 'system' 
      ? `Theme set to System Default (${resolved === 'dark' ? 'Dark Mode' : 'Light Mode'})` 
      : `Theme switched to ${meta.name}`;
    toast(note);
  }
}

function initTheme() {
  const pref = getStoredThemePreference();
  const resolved = resolveEffectiveTheme(pref);
  ensureSystemListener(pref === 'system');
  applyThemeToDOM(pref, resolved);
}

function toggleTheme() {
  const currentPref = getStoredThemePreference();
  const nextIdx = (THEME_OPTIONS.indexOf(currentPref) + 1) % THEME_OPTIONS.length;
  setAppTheme(THEME_OPTIONS[nextIdx], true);
}

function toggleThemeMenu(event) {
  if (event) event.stopPropagation();
  const menu = document.getElementById('theme-dropdown-menu');
  if (!menu) return;
  const isShown = menu.style.display === 'block';
  closeAllThemeMenus();
  if (!isShown) menu.style.display = 'block';
}

function closeThemeMenu() {
  const menu = document.getElementById('theme-dropdown-menu');
  if (menu) menu.style.display = 'none';
}

function toggleLandingThemeMenu(event) {
  if (event) event.stopPropagation();
  const menu = document.getElementById('landing-theme-dropdown-menu');
  if (!menu) return;
  const isShown = menu.style.display === 'block';
  closeAllThemeMenus();
  if (!isShown) menu.style.display = 'block';
}

function closeLandingThemeMenu() {
  const menu = document.getElementById('landing-theme-dropdown-menu');
  if (menu) menu.style.display = 'none';
}

function closeAllThemeMenus() {
  closeThemeMenu();
  closeLandingThemeMenu();
}

function openProfileAppearance() {
  showPage('page-profile');
  setTimeout(() => {
    const el = document.getElementById('settings-appearance-card');
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }, 120);
}'''

assert old_theme_block in js, "Could not find old_theme_block in static/js/app.js"
js = js.replace(old_theme_block, new_theme_block)

# 2. Update global click-outside and escape listeners
old_click_listener = '''// Global click-outside listener to close dropdowns
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
});'''

new_click_listener = '''// Global click-outside listener to close dropdowns
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
  const themeWrap = document.getElementById('theme-dropdown-menu');
  const themeBtn = document.getElementById('btn-theme-toggle');
  if (themeWrap && themeBtn && !themeWrap.contains(e.target) && !themeBtn.contains(e.target)) {
    closeThemeMenu();
  }
  const landingThemeWrap = document.getElementById('landing-theme-dropdown-menu');
  const landingThemeBtn = document.getElementById('landing-theme-toggle');
  if (landingThemeWrap && landingThemeBtn && !landingThemeWrap.contains(e.target) && !landingThemeBtn.contains(e.target)) {
    closeLandingThemeMenu();
  }
});

// Escape key closes dropdowns
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeProfileDropdown();
    closeAllThemeMenus();
    const notifDropdown = document.getElementById('notifications-dropdown');
    if (notifDropdown) notifDropdown.style.display = 'none';
  }
});'''

assert old_click_listener in js, "Could not find old_click_listener in static/js/app.js"
js = js.replace(old_click_listener, new_click_listener)

# 3. Update loadUserProfile to refresh theme labels
old_user_profile_start = '''async function loadUserProfile() {
  try {
    const me = await window.api.getMe();
    appState.currentUser = me;'''

new_user_profile_start = '''async function loadUserProfile() {
  try {
    // Refresh theme status on profile card
    const pref = getStoredThemePreference();
    applyThemeToDOM(pref, resolveEffectiveTheme(pref));

    const me = await window.api.getMe();
    appState.currentUser = me;'''

assert old_user_profile_start in js, "Could not find old_user_profile_start in static/js/app.js"
js = js.replace(old_user_profile_start, new_user_profile_start)

with open('static/js/app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("static/js/app.js updated successfully with complete theme system logic!")
