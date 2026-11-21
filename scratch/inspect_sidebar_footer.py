with open('static/css/styles.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'sidebar-footer' in l:
        print(f"Around line {i+1}:")
        for j in range(max(0, i-5), min(len(lines), i+25)):
            print(f"{j+1}: {lines[j]}", end='')
