with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

replacements = {
    '<span class="nav-icon">📊</span>': '<span class="nav-icon"><i data-lucide="layout-dashboard">📊</i></span>',
    '<span class="nav-icon">👥</span>': '<span class="nav-icon"><i data-lucide="users">👥</i></span>',
    '<span class="nav-icon">🔍</span>': '<span class="nav-icon"><i data-lucide="search">🔍</i></span>',
    '<span class="nav-icon">➕</span>': '<span class="nav-icon"><i data-lucide="user-plus">➕</i></span>',
    '<span class="nav-icon">🩺</span>': '<span class="nav-icon"><i data-lucide="stethoscope">🩺</i></span>',
    '<span class="nav-icon">📅</span>': '<span class="nav-icon"><i data-lucide="calendar">📅</i></span>',
    '<span class="nav-icon">👨‍⚕️</span>': '<span class="nav-icon"><i data-lucide="user-check">👨‍⚕️</i></span>',
    '<span class="nav-icon">🛏️</span>': '<span class="nav-icon"><i data-lucide="bed">🛏️</i></span>',
    '<span class="nav-icon">🎫</span>': '<span class="nav-icon"><i data-lucide="ticket">🎫</i></span>',
    '<span class="nav-icon">🧪</span>': '<span class="nav-icon"><i data-lucide="flask-conical">🧪</i></span>',
    '<span class="nav-icon">🚑</span>': '<span class="nav-icon"><i data-lucide="ambulance">🚑</i></span>',
    '<span class="nav-icon">📈</span>': '<span class="nav-icon"><i data-lucide="trending-up">📈</i></span>',
    '<span class="nav-icon">🛡️</span>': '<span class="nav-icon"><i data-lucide="shield">🛡️</i></span>',
    '<span class="nav-icon">💾</span>': '<span class="nav-icon"><i data-lucide="database">💾</i></span>',
    '<span class="nav-icon">⚙️</span>': '<span class="nav-icon"><i data-lucide="hard-drive">⚙️</i></span>'
}

count = 0
for k, v in replacements.items():
    if k in text:
        text = text.replace(k, v)
        count += 1

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print(f"Replaced {count} sidebar icons successfully.")
