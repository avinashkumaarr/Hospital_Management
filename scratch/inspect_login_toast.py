with open('static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
print("--- Login handlers in app.js ---")
for line in js.splitlines():
    if 'switchview' in line.lower() and ('app' in line.lower() or 'home' in line.lower()):
        print("switchView:", line.strip())
    if 'quicklogin' in line.lower() or 'handlelogin' in line.lower() or 'performlogin' in line.lower():
        print("login func:", line.strip())

m = re.search(r'(async\s+function\s+performLogin[\s\S]*?)(function|\Z)', js)
if m:
    print("\nperformLogin:\n", m.group(1)[:800])

m = re.search(r'(async\s+function\s+quickLogin[\s\S]*?)(function|\Z)', js)
if m:
    print("\nquickLogin:\n", m.group(1)[:800])
