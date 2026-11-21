with open('static/css/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re
matches = re.findall(r'(\.welcome[^{]*\{[^}]*\})', css)
for m in matches:
    print(m)
