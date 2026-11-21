with open('static/js/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'function loadPatientDirectory' in l:
        print(f"loadPatientDirectory at line {i+1}")
        for j in range(i, min(i+70, len(lines))):
            print(f"{j+1}: {lines[j]}", end='')
        break
