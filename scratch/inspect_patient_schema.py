with open('backend/app/schemas/all_schemas.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'class PatientUpdate' in l:
        print(f"Around line {i+1}:")
        for j in range(i, min(len(lines), i+20)):
            print(f"{j+1}: {lines[j]}", end='')
