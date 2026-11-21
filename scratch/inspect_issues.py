with open('static/css/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

with open('static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("--- Toast in CSS ---")
for line in css.splitlines():
    if 'toast' in line.lower():
        print("CSS:", line)

print("\n--- Toast in JS ---")
for line in js.splitlines():
    if 'function toast' in line or 'showtoast' in line.lower():
        print("JS function:", line)
    if 'welcome' in line.lower() and 'toast' in line.lower():
        print("JS welcome toast:", line)

print("\n--- Logout buttons in HTML ---")
for i, line in enumerate(html.splitlines()):
    if 'logout' in line.lower():
        print(f"HTML L{i+1}:", line.strip()[:100])
