with open('static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
m = re.search(r'(async\s+function\s+loadDashboardCharts[\s\S]*?)(async\s+function|\Z)', js)
if m:
    print(m.group(1)[:1200])
