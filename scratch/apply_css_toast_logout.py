with open('static/css/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

old_toast_block = '''#toast-container {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  z-index: 2000;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.toast {
  background: var(--navy);
  color: #fff;
  padding: 0.65rem 1.15rem;
  border-radius: var(--radius-md);
  font-size: 0.85rem;
  font-weight: 500;
  box-shadow: var(--shadow-lg);
  display: flex;
  align-items: center;
  gap: 0.65rem;
  animation: slideIn 0.2s ease-out;
}

.toast.danger {
  background: var(--danger);
}

@keyframes slideIn {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}'''

new_toast_block = '''/* Redesigned Toast Notification System */
#toast-container {
  position: fixed;
  top: 1.25rem;
  right: 1.5rem;
  z-index: 99999;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  pointer-events: none;
  max-width: 400px;
  width: calc(100vw - 2.5rem);
}

.toast {
  pointer-events: auto;
  background: var(--surface);
  color: var(--text);
  border: 1px solid var(--border);
  border-left: 4px solid #10b981;
  padding: 0.75rem 0.95rem;
  border-radius: var(--radius-md);
  font-size: 0.85rem;
  font-weight: 500;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.12), 0 8px 10px -6px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  animation: toastIn 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  transition: transform 0.2s ease, opacity 0.2s ease;
  min-height: 44px;
}

.toast.success {
  border-left-color: #10b981;
}

.toast.danger {
  border-left-color: #ef4444;
}

.toast-left {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  min-width: 0;
  flex: 1;
}

.toast-icon-badge {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.82rem;
  font-weight: 800;
  flex-shrink: 0;
}

.toast-icon-badge.success {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.toast-icon-badge.danger {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.toast-body-text {
  font-size: 0.84rem;
  font-weight: 600;
  color: var(--text);
  line-height: 1.4;
  word-break: break-word;
}

.toast-close-btn {
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  font-size: 0.85rem;
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
  flex-shrink: 0;
  line-height: 1;
}

.toast-close-btn:hover {
  background: var(--bg-alt);
  color: var(--text);
}

@keyframes toastIn {
  from {
    opacity: 0;
    transform: translateY(-16px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes toastOut {
  from {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
  to {
    opacity: 0;
    transform: translateY(-12px) scale(0.95);
  }
}

@media (max-width: 600px) {
  #toast-container {
    top: 0.75rem;
    right: 0.75rem;
    left: 0.75rem;
    width: auto;
    max-width: none;
  }
}'''

assert old_toast_block in css, "Could not find old_toast_block in styles.css"
css = css.replace(old_toast_block, new_toast_block)

# Add logout buttons and welcome banner styling
extra_styles = '''

/* --- Visible Red Logout Buttons & Welcome Banner --- */
.sidebar-footer {
  padding: 0.85rem 1rem !important;
  border-top: 1px solid var(--border-light);
  display: flex !important;
  flex-direction: column !important;
  gap: 0.65rem !important;
  background: var(--surface) !important;
}

.sidebar-user-card {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  cursor: pointer;
  padding: 0.35rem 0.45rem;
  border-radius: var(--radius-md);
  transition: background var(--transition-fast);
  width: 100%;
}

.sidebar-user-card:hover {
  background: var(--bg-alt);
}

.sidebar-user-meta {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}

.sidebar-user-meta #sidebar-user-name {
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.sidebar-user-meta #sidebar-user-role {
  font-size: 0.7rem;
  color: var(--text-muted);
}

.btn-logout-red {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 0.5rem !important;
  background: #dc2626 !important;
  color: #ffffff !important;
  border: 1px solid #b91c1c !important;
  padding: 0.55rem 1rem !important;
  border-radius: var(--radius-md) !important;
  font-size: 0.85rem !important;
  font-weight: 700 !important;
  cursor: pointer !important;
  width: 100% !important;
  white-space: nowrap !important;
  transition: all var(--transition-fast) !important;
  box-shadow: 0 1px 3px rgba(220, 38, 38, 0.25) !important;
  box-sizing: border-box !important;
  text-decoration: none !important;
}

.btn-logout-red:hover {
  background: #b91c1c !important;
  border-color: #991b1b !important;
  color: #ffffff !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(220, 38, 38, 0.35) !important;
}

.btn-logout-red:active {
  transform: translateY(0);
}

.btn-logout-red .btn-logout-icon {
  font-size: 0.95rem;
  line-height: 1;
}

.btn-logout-red .btn-logout-label {
  color: #ffffff !important;
  font-weight: 700 !important;
  font-size: 0.85rem !important;
  display: inline-block !important;
  visibility: visible !important;
  opacity: 1 !important;
  letter-spacing: 0.02em;
}

.btn-logout-header {
  display: inline-flex !important;
  align-items: center !important;
  gap: 0.45rem !important;
  background: #dc2626 !important;
  color: #ffffff !important;
  border: 1px solid #b91c1c !important;
  padding: 0.42rem 0.85rem !important;
  border-radius: var(--radius-md) !important;
  font-size: 0.82rem !important;
  font-weight: 700 !important;
  cursor: pointer !important;
  white-space: nowrap !important;
  transition: all var(--transition-fast) !important;
  box-shadow: 0 1px 3px rgba(220, 38, 38, 0.25) !important;
  margin-left: 0.65rem !important;
  text-decoration: none !important;
}

.btn-logout-header:hover {
  background: #b91c1c !important;
  border-color: #991b1b !important;
  color: #ffffff !important;
  transform: translateY(-1px);
  box-shadow: 0 3px 6px rgba(220, 38, 38, 0.35) !important;
}

.btn-logout-header:active {
  transform: translateY(0);
}

.btn-logout-header .btn-logout-icon {
  font-size: 0.9rem;
  line-height: 1;
}

.btn-logout-header .btn-logout-label {
  color: #ffffff !important;
  font-weight: 700 !important;
  font-size: 0.82rem !important;
  display: inline-block !important;
  visibility: visible !important;
  opacity: 1 !important;
}

.welcome-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--surface);
  border: 1px solid var(--border-light);
  border-left: 4px solid var(--primary);
  border-radius: var(--radius-lg);
  padding: 1rem 1.35rem;
  margin-bottom: 1.25rem;
  flex-wrap: wrap;
  gap: 0.85rem;
  box-shadow: var(--shadow-sm);
}

.welcome-banner-title {
  font-family: var(--font-heading);
  font-size: 1.2rem;
  font-weight: 800;
  color: var(--text);
  margin: 0;
  line-height: 1.3;
}

.welcome-banner-sub {
  font-size: 0.82rem;
  color: var(--text-muted);
  margin-top: 2px;
  line-height: 1.4;
}

.welcome-banner-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}
'''

css += extra_styles

with open('static/css/styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Successfully updated static/css/styles.css!")
