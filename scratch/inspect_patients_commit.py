with open('backend/app/routers/patients.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(270, min(290, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')
