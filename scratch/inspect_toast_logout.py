with open('static/css/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

with open('static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

print("--- CSS for toast ---")
m = re.search(r'(#toast-container[\s\S]*?)(/\*|\Z)', css)
if m:
    print(m.group(1)[:1200])

print("\n--- JS for toast ---")
m = re.search(r'(function\s+toast[\s\S]*?)(function|\Z)', js)
if m:
    print(m.group(1)[:800])

print("\n--- HTML L745-765 (sidebar footer) ---")
lines = html.splitlines()
for i in range(744, 765):
    print(f"{i+1}: {lines[i]}")

print("\n--- HTML L1835-1845 (profile logout) ---")
for i in range(1834, min(len(lines), 1845)):
    print(f"{i+1}: {lines[i]}")
