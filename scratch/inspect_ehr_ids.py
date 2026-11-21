with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_search = False
for i, l in enumerate(lines):
    if 'id="page-search"' in l:
        in_search = True
    if in_search:
        if 'id=' in l or '<h' in l:
            print(f"{i+1}: {l.strip()[:100]}")
        if '</section>' in l:
            break
