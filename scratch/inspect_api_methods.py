with open('static/js/api.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
methods = re.findall(r'(\w+)\s*:\s*(?:async\s*)?\([^)]*\)\s*=>', js)
print("api.js methods found:", methods)
