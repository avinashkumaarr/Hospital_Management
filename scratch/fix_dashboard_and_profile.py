import re

print("--- Step 1: Updating static/css/styles.css ---")
with open("static/css/styles.css", "r", encoding="utf-8") as f:
    css = f.read()

# Fix layout flex rules for #view-app and #app-container
old_app_view_rule = """#view-app.active {
  display: flex;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}"""

new_app_view_rule = """#view-app.active,
#app-container {
  display: flex !important;
  flex: 1 1 auto;
  width: 100vw !important;
  height: 100vh !important;
  max-width: 100vw;
  max-height: 100vh;
  overflow: hidden !important;
  position: relative;
}"""

if old_app_view_rule in css:
    css = css.replace(old_app_view_rule, new_app_view_rule)

# Ensure .app-main has min-width: 0 and flex: 1 1 0%
old_app_main_rule = """.app-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: var(--bg);
}"""

new_app_main_rule = """.app-main {
  flex: 1 1 0%;
  min-width: 0;
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: var(--bg);
}"""

if old_app_main_rule in css:
    css = css.replace(old_app_main_rule, new_app_main_rule)

# Add profile dropdown and profile page styles if not present
profile_css = """
/* ==========================================================================
   STAFF PROFILE DROPDOWN & PROFILE PAGE STYLES
   ========================================================================== */

.profile-dropdown-wrap {
  position: relative;
}

.profile-trigger-btn {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  background: var(--bg-alt);
  border: 1px solid var(--border);
  padding: 4px 10px 4px 6px;
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: var(--transition);
}

.profile-trigger-btn:hover {
  background: var(--surface);
  border-color: var(--primary);
  box-shadow: var(--shadow-sm);
}

.avatar-pill {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--primary), var(--teal));
  color: #fff;
  font-weight: 700;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.profile-meta-text {
  display: flex;
  flex-direction: column;
  text-align: left;
  line-height: 1.2;
}

.profile-name-line {
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--text);
  max-width: 140px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.profile-role-line {
  font-size: 0.68rem;
  color: var(--text-muted);
}

.dropdown-chevron {
  font-size: 0.75rem;
  color: var(--text-dim);
  margin-left: 2px;
}

/* Profile Dropdown Menu */
.profile-dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 260px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  z-index: 1000;
  padding: 0.5rem;
  animation: fadeInDown 0.15s ease-out;
}

.dropdown-user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
}

.dropdown-avatar {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--primary), var(--teal));
  color: #fff;
  font-weight: 800;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.dropdown-meta {
  min-width: 0;
  flex: 1;
}

.dropdown-meta strong {
  display: block;
  font-size: 0.88rem;
  color: var(--text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dropdown-divider {
  height: 1px;
  background: var(--border-light);
  margin: 0.35rem 0;
}

.dropdown-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.55rem 0.75rem;
  border-radius: var(--radius-md);
  background: transparent;
  border: none;
  color: var(--text);
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  text-align: left;
  transition: var(--transition);
}

.dropdown-item:hover {
  background: var(--bg-alt);
  color: var(--primary);
}

.dropdown-item i {
  width: 16px;
  height: 16px;
  color: var(--text-muted);
}

.dropdown-item:hover i {
  color: var(--primary);
}

.dropdown-item-danger {
  color: var(--danger);
}

.dropdown-item-danger:hover {
  background: var(--danger-light);
  color: var(--danger);
}

.dropdown-item-danger i {
  color: var(--danger);
}

/* Profile Page Layout */
.profile-header-banner {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  border-radius: var(--radius-xl);
  padding: 2rem;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 1.75rem;
  margin-bottom: 2rem;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-md);
}

.profile-header-banner::after {
  content: '';
  position: absolute;
  right: -40px;
  top: -40px;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(37, 99, 235, 0.25) 0%, transparent 70%);
  pointer-events: none;
}

.profile-avatar-lg {
  width: 80px;
  height: 80px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--primary), var(--teal));
  color: #fff;
  font-family: var(--font-heading);
  font-size: 2rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 4px solid rgba(255, 255, 255, 0.15);
  box-shadow: var(--shadow-lg);
  flex-shrink: 0;
}

.profile-meta-lg h2 {
  font-family: var(--font-heading);
  font-size: 1.6rem;
  font-weight: 800;
  margin-bottom: 0.35rem;
}

.profile-tags-row {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  flex-wrap: wrap;
  margin-top: 0.5rem;
}

.profile-grid-layout {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 1.5rem;
}

@media (max-width: 900px) {
  .profile-grid-layout {
    grid-template-columns: 1fr;
  }
}
"""

if ".profile-dropdown-wrap" not in css:
    css += "\n" + profile_css

with open("static/css/styles.css", "w", encoding="utf-8") as f:
    f.write(css)
print("static/css/styles.css updated successfully.")
