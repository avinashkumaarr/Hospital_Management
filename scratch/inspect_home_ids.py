with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_home = False
for i, l in enumerate(lines):
    if 'id="page-home"' in l:
        in_home = True
    if in_home:
        if 'id=' in l:
            print(f"{i+1}: {l.strip()[:100]}")
        if '</section>' in l:
            break
