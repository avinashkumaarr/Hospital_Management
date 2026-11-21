with open('backend/app/routers/backup.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '3.0' in l or 'version' in l:
        print(f"{i+1}: {l.strip()}")
