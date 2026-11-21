with open('static/js/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'function showPage' in l:
        print(f"showPage at line {i+1}:")
        for j in range(i, min(i+40, len(lines))):
            print(f"{j+1}: {lines[j]}", end='')
        break
