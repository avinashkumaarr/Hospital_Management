css_additions = '''

/* ==========================================================================
   MEDILINK ENTERPRISE v4.0 — NEW STYLES & ENHANCEMENTS
   ========================================================================== */

/* --- Printable Prescription Slip --- */
@media print {
  body * {
    visibility: hidden !important;
  }
  #modal-rx-slip,
  #modal-rx-slip .modal-content,
  #printable-rx-content,
  #printable-rx-content * {
    visibility: visible !important;
  }
  #modal-rx-slip {
    position: absolute !important;
    left: 0 !important;
    top: 0 !important;
    width: 100% !important;
    height: auto !important;
    background: #ffffff !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
    z-index: 99999 !important;
    display: block !important;
  }
  #modal-rx-slip .modal-header,
  #modal-rx-slip .modal-footer {
    display: none !important;
  }
  #modal-rx-slip .modal-content {
    border: none !important;
    box-shadow: none !important;
    width: 100% !important;
    max-width: 100% !important;
    padding: 2rem !important;
    background: #ffffff !important;
    color: #0f172a !important;
  }
  #printable-rx-content {
    color: #0f172a !important;
  }
}

/* --- Global Search Command Palette (Ctrl+K) --- */
.global-search-modal-card {
  border: 1px solid var(--border-light);
  background: var(--surface);
  animation: modalScaleIn 0.15s cubic-bezier(0.16, 1, 0.3, 1);
}

.palette-chip {
  background: var(--surface);
  border: 1px solid var(--border-light);
  color: var(--text-muted);
  padding: 3px 12px;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.palette-chip:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.palette-chip.active {
  background: var(--primary);
  border-color: var(--primary);
  color: #ffffff;
}

.palette-section-title {
  padding: 0.4rem 1.25rem 0.2rem;
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-dim);
}

.palette-result-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.6rem 1.25rem;
  cursor: pointer;
  transition: background var(--transition-fast);
  border-left: 3px solid transparent;
}

.palette-result-item:hover,
.palette-result-item.active {
  background: var(--bg-alt);
  border-left-color: var(--primary);
}

.palette-item-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-width: 0;
}

.palette-item-icon {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-md);
  background: var(--bg-alt);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  flex-shrink: 0;
}

.palette-item-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.palette-item-title {
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.palette-item-sub {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.palette-item-action {
  font-size: 0.72rem;
  color: var(--text-dim);
  display: flex;
  align-items: center;
  gap: 4px;
}

kbd {
  background: var(--surface);
  border: 1px solid var(--border-light);
  border-radius: 3px;
  box-shadow: 0 1px 1px rgba(0,0,0,0.1);
  font-family: var(--font-mono);
  font-size: 0.7rem;
  padding: 1px 4px;
  color: var(--text-muted);
}

/* --- Table Pagination Controls --- */
.table-pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0.25rem;
  border-top: 1px solid var(--border-light);
  font-size: 0.82rem;
  color: var(--text-muted);
}

.page-btn {
  padding: 4px 10px;
  font-size: 0.8rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-light);
  background: var(--surface);
  color: var(--text);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.page-btn:hover:not(:disabled) {
  border-color: var(--primary);
  color: var(--primary);
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
'''

with open('static/css/styles.css', 'r', encoding='utf-8') as f:
    current_css = f.read()

# Update version in styles.css header
current_css = current_css.replace('MediLink Enterprise v3.0', 'MediLink Enterprise v4.0')
current_css = current_css.replace('v3.0.0', 'v4.0.0')

new_css = current_css + css_additions

with open('static/css/styles.css', 'w', encoding='utf-8') as f:
    f.write(new_css)

print("Updated static/css/styles.css successfully! New length:", len(new_css))
