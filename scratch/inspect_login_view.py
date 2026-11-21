with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_login = False
for i, l in enumerate(lines):
    if 'id="view-login"' in l:
        in_login = True
    if in_login:
        print(f"{i+1}: {l}", end='')
        if 'id="view-app"' in l:
            break
