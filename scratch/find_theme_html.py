with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'toggleTheme' in l or 'theme' in l.lower() and ('button' in l.lower() or 'dropdown' in l.lower() or 'preference' in l.lower()):
        print(f"L{i+1}: {l.strip()[:100]}")
