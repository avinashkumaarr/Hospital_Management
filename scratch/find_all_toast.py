with open('static/css/styles.css', 'r', encoding='utf-8') as f:
    css_lines = f.readlines()

for i, l in enumerate(css_lines):
    if 'toast' in l.lower():
        print(f"CSS L{i+1}: {l.strip()}")

with open('index.html', 'r', encoding='utf-8') as f:
    html_lines = f.readlines()

for i, l in enumerate(html_lines):
    if 'toast' in l.lower():
        print(f"HTML L{i+1}: {l.strip()}")
