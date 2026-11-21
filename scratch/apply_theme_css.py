css_theme_additions = '''

/* ==========================================================================
   THEME PALETTES & THEME CUSTOMIZATION SYSTEM (FOUR OPTIONS)
   ========================================================================== */

/* Explicit Light Theme (Clinical Light) */
[data-theme="light"] {
  --primary: #2563eb;
  --primary-hover: #1d4ed8;
  --primary-light: #eff6ff;
  --primary-rgb: 37, 99, 235;

  --navy: #0f172a;
  --navy-light: #1e293b;

  --teal: #0d9488;
  --teal-hover: #0f766e;
  --teal-light: #f0fdfa;
  --teal-rgb: 13, 148, 136;

  --accent: #f59e0b;
  --accent-light: #fef3c7;

  --bg: #f8fafc;
  --bg-alt: #f1f5f9;
  --surface: #ffffff;
  --surface-hover: #f8fafc;
  --card: #ffffff;
  --card-alt: #f8fafc;
  --border: #e2e8f0;
  --border-light: #edf2f7;
  --border-focus: #2563eb;

  --text: #0f172a;
  --text-muted: #64748b;
  --text-dim: #94a3b8;

  --success: #10b981;
  --success-light: #ecfdf5;
  --warning: #f59e0b;
  --warning-light: #fffbeb;
  --danger: #ef4444;
  --danger-light: #fef2f2;
  --info: #0284c7;
  --info-light: #f0f9ff;
}

/* Midnight Blue Theme (Deep Navy Enterprise Hospital) */
[data-theme="midnight"] {
  --primary: #38bdf8;
  --primary-hover: #0284c7;
  --primary-light: rgba(56, 189, 248, 0.15);
  --primary-rgb: 56, 189, 248;

  --navy: #f0f6fc;
  --navy-light: #cbd5e1;

  --teal: #2dd4bf;
  --teal-hover: #14b8a6;
  --teal-light: rgba(45, 212, 191, 0.15);

  --bg: #060b18;
  --bg-alt: #0b152d;
  --surface: #0e1b38;
  --surface-hover: #15274f;
  --card: #0e1b38;
  --card-alt: #091226;
  --border: #1e3567;
  --border-light: #16284e;
  --border-focus: #38bdf8;

  --text: #f0f6fc;
  --text-muted: #94a3b8;
  --text-dim: #64748b;

  --success: #10b981;
  --success-light: rgba(16, 185, 129, 0.15);
  --warning: #f59e0b;
  --warning-light: rgba(245, 158, 11, 0.15);
  --danger: #f87171;
  --danger-light: rgba(239, 68, 68, 0.15);
  --info: #38bdf8;
  --info-light: rgba(56, 189, 248, 0.15);

  --shadow-xs: 0 1px 2px rgba(2, 6, 23, 0.5);
  --shadow-sm: 0 2px 4px rgba(2, 6, 23, 0.55);
  --shadow-md: 0 4px 8px rgba(2, 6, 23, 0.65);
  --shadow-lg: 0 12px 20px rgba(2, 6, 23, 0.75);
  --shadow-xl: 0 20px 30px rgba(2, 6, 23, 0.85);
}

/* Theme Cards Grid & Interactive Previews */
.theme-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.25rem;
  margin-top: 1rem;
}

.theme-preview-card {
  border: 2px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.15rem;
  background: var(--surface);
  cursor: pointer;
  transition: all var(--transition-fast);
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.theme-preview-card:hover {
  border-color: var(--primary);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.theme-preview-card.active {
  border-color: var(--primary);
  background: var(--card-alt);
  box-shadow: 0 0 0 1px var(--primary), var(--shadow-md);
}

.theme-card-check {
  position: absolute;
  top: 0.85rem;
  right: 0.85rem;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--primary);
  color: #fff;
  font-size: 0.8rem;
  font-weight: 800;
  display: none;
  align-items: center;
  justify-content: center;
}

.theme-preview-card.active .theme-card-check {
  display: flex;
}

/* Miniature Dashboards */
.theme-mini-preview {
  height: 84px;
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid rgba(0,0,0,0.12);
  display: flex;
  flex-direction: column;
}

.theme-mini-preview .mini-bar {
  height: 14px;
  border-bottom: 1px solid rgba(0,0,0,0.12);
}

.theme-mini-preview .mini-body {
  flex: 1;
  display: flex;
}

.theme-mini-preview .mini-side {
  width: 26px;
  border-right: 1px solid rgba(0,0,0,0.12);
}

.theme-mini-preview .mini-content {
  flex: 1;
  padding: 5px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4px;
}

.theme-mini-preview .mini-kpi {
  height: 16px;
  border-radius: 3px;
}

.theme-mini-preview .mini-chart {
  grid-column: 1 / -1;
  height: 34px;
  border-radius: 3px;
}

/* Palette variations in mini previews */
.preview-light { background: #f8fafc; }
.preview-light .mini-bar { background: #ffffff; border-color: #e2e8f0; }
.preview-light .mini-side { background: #ffffff; border-color: #e2e8f0; }
.preview-light .mini-kpi { background: #ffffff; border: 1px solid #e2e8f0; }
.preview-light .mini-chart { background: #eff6ff; border: 1px solid #bfdbfe; }

.preview-dark { background: #0b1120; }
.preview-dark .mini-bar { background: #1e293b; border-color: #334155; }
.preview-dark .mini-side { background: #1e293b; border-color: #334155; }
.preview-dark .mini-kpi { background: #1e293b; border: 1px solid #334155; }
.preview-dark .mini-chart { background: #172554; border: 1px solid #1e40af; }

.preview-midnight { background: #060b18; }
.preview-midnight .mini-bar { background: #0e1b38; border-color: #1e3567; }
.preview-midnight .mini-side { background: #0e1b38; border-color: #1e3567; }
.preview-midnight .mini-kpi { background: #0e1b38; border: 1px solid #1e3567; }
.preview-midnight .mini-chart { background: #082f49; border: 1px solid #0369a1; }

.preview-system {
  background: linear-gradient(135deg, #f8fafc 50%, #0b1120 50%);
}
.preview-system .mini-bar { background: linear-gradient(135deg, #ffffff 50%, #1e293b 50%); border-color: #475569; }
.preview-system .mini-side { background: linear-gradient(135deg, #ffffff 50%, #1e293b 50%); border-color: #475569; }
.preview-system .mini-kpi { background: linear-gradient(135deg, #ffffff 50%, #1e293b 50%); border: 1px solid #475569; }
.preview-system .mini-chart { background: linear-gradient(135deg, #eff6ff 50%, #172554 50%); border: 1px solid #475569; }

.theme-card-info {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.theme-card-title {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  font-size: 0.95rem;
  color: var(--text);
}

.theme-card-desc {
  font-size: 0.78rem;
  color: var(--text-muted);
  line-height: 1.4;
}

/* Theme Dropdown Popover in Topbar and Navbar */
.theme-dropdown-menu {
  position: absolute;
  right: 0;
  top: 44px;
  width: 220px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  padding: 0.5rem;
  z-index: 1000;
  animation: modalScaleIn 0.15s cubic-bezier(0.16, 1, 0.3, 1);
}

.theme-menu-header {
  padding: 0.4rem 0.65rem 0.3rem;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-dim);
}

.theme-menu-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.55rem 0.65rem;
  border: none;
  background: transparent;
  color: var(--text);
  font-size: 0.85rem;
  font-weight: 600;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
  text-align: left;
}

.theme-menu-item:hover {
  background: var(--bg-alt);
  color: var(--primary);
}

.theme-menu-item.active {
  background: var(--primary-light);
  color: var(--primary);
}

.theme-menu-icon {
  font-size: 1rem;
  line-height: 1;
}

.theme-menu-label {
  flex: 1;
}

.theme-menu-check {
  font-size: 0.85rem;
  font-weight: 800;
  color: var(--primary);
  display: none;
}

.theme-menu-item.active .theme-menu-check {
  display: inline-block;
}

/* Smooth Theme Transitions */
html {
  transition: background-color 0.2s ease, color 0.2s ease;
}

@media (prefers-reduced-motion: reduce) {
  html, * {
    transition: none !important;
  }
}
'''

with open('static/css/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

css += css_theme_additions

with open('static/css/styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("styles.css updated successfully with four theme palettes & customization styles!")
