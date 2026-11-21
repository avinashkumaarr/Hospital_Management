with open('static/css/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

with open('static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

print("--- CSS root variables ---")
m = re.search(r'(:root\s*\{[\s\S]*?\})', css)
if m:
    print(m.group(1)[:1200])

print("\n--- CSS data-theme=dark ---")
m = re.search(r'(\[data-theme=["\']dark["\']\]\s*\{[\s\S]*?\})', css)
if m:
    print(m.group(1)[:1200])

print("\n--- JS theme functions ---")
for line in js.splitlines():
    if 'theme' in line.lower() and ('function' in line or 'toggle' in line or 'init' in line):
        print(line)

print("\n--- HTML theme buttons ---")
for line in html.splitlines():
    if 'toggleTheme' in line or 'theme' in line.lower() and ('button' in line.lower() or 'dropdown' in line.lower()):
        print(line.strip())
