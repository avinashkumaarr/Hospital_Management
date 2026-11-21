import re
from bs4 import BeautifulSoup

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
html_ids = set(tag.get('id') for tag in soup.find_all(True) if tag.get('id'))

with open('static/js/app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

with open('static/js/api.js', 'r', encoding='utf-8') as f:
    api_js = f.read()

# 1. Missing DOM IDs accessed in app.js
get_elem_ids = set(re.findall(r'document\.getElementById\([\'"]([a-zA-Z0-9_\-]+)[\'"]\)', app_js))
query_ids = set(re.findall(r'querySelector\([\'"]#([a-zA-Z0-9_\-]+)[\'"]\)', app_js))
accessed_ids = get_elem_ids | query_ids
missing_ids = accessed_ids - html_ids
print(f'Total DOM IDs accessed in app.js: {len(accessed_ids)}')
print(f'Missing IDs in index.html: {len(missing_ids)}')
for m in sorted(missing_ids):
    print(f'  Missing ID: #{m}')

# 2. Check onclick handlers in index.html vs defined functions in JS
onclick_handlers = set(re.findall(r'on[a-z]+\s*=\s*[\'"]([a-zA-Z0-9_]+)\(', html))
defined_funcs = set(re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', app_js + api_js))
defined_funcs |= set(re.findall(r'([a-zA-Z0-9_]+)\s*=\s*(?:function|\([^)]*\)\s*=>)', app_js + api_js))
defined_funcs |= set(re.findall(r'window\.([a-zA-Z0-9_]+)\s*=', app_js + api_js))

missing_handlers = onclick_handlers - defined_funcs
print(f'\nTotal onclick handlers in index.html: {len(onclick_handlers)}')
print(f'Missing JS functions for onclick: {len(missing_handlers)}')
for h in sorted(missing_handlers):
    print(f'  Missing function: {h}()')

# 3. Check duplicate function definitions in app.js
func_matches = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', app_js)
func_counts = {}
for fn in func_matches:
    func_counts[fn] = func_counts.get(fn, 0) + 1
dup_funcs = {k: v for k, v in func_counts.items() if v > 1}
print(f'\nDuplicate function declarations in app.js: {len(dup_funcs)}')
for k, v in dup_funcs.items():
    print(f'  Function {k}() declared {v} times')
