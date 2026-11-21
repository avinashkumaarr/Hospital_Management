with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_prof = False
for i, l in enumerate(lines):
    if 'id="page-profile"' in l:
        in_prof = True
    if in_prof:
        if 'id=' in l or '<h' in l:
            print(f"{i+1}: {l.strip()[:100]}")
        if '</section>' in l:
            break
