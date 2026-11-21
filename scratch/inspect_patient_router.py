with open('backend/app/routers/patients.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'update_patient' in l:
        print(f"Around line {i+1}:")
        for j in range(max(0, i-5), min(len(lines), i+35)):
            print(f"{j+1}: {lines[j]}", end='')
