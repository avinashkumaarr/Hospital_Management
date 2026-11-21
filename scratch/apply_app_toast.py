with open('static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_toast = '''function toast(message, isDanger = false) {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const t = document.createElement('div');
  t.className = `toast ${isDanger ? 'danger' : ''}`;
  t.innerHTML = `<span>${isDanger ? '⚠️' : '✅'}</span> <span>${escapeHtml(message)}</span>`;
  container.appendChild(t);
  setTimeout(() => {
    t.style.opacity = '0';
    t.style.transform = 'translateY(8px)';
    setTimeout(() => t.remove(), 250);
  }, 3500);
}'''

new_toast = '''function toast(message, isDanger = false) {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const t = document.createElement('div');
  t.className = `toast ${isDanger ? 'danger' : 'success'}`;
  
  const iconBadge = isDanger
    ? `<div class="toast-icon-badge danger"><span>⚠</span></div>`
    : `<div class="toast-icon-badge success"><span>✓</span></div>`;

  t.innerHTML = `
    <div class="toast-left">
      ${iconBadge}
      <div class="toast-body-text">${escapeHtml(message)}</div>
    </div>
    <button type="button" class="toast-close-btn" onclick="dismissToast(this.closest('.toast'))" title="Close notification">✕</button>
  `;

  container.appendChild(t);

  const timeoutId = setTimeout(() => {
    dismissToast(t);
  }, 4000);

  t._dismissTimeout = timeoutId;
}

function dismissToast(toastEl) {
  if (!toastEl || toastEl.classList.contains('dismissing')) return;
  toastEl.classList.add('dismissing');
  if (toastEl._dismissTimeout) clearTimeout(toastEl._dismissTimeout);
  toastEl.style.animation = 'toastOut 0.25s cubic-bezier(0.16, 1, 0.3, 1) forwards';
  setTimeout(() => {
    if (toastEl.parentElement) toastEl.remove();
  }, 260);
}'''

assert old_toast in js, "Could not find old_toast in app.js"
js = js.replace(old_toast, new_toast)

with open('static/js/app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Successfully updated static/js/app.js!")
