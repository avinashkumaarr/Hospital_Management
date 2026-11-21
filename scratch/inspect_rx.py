with open('static/js/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'modal-rx-slip' in l:
        print(f"Around line {i+1}:")
        for j in range(max(0, i-10), min(len(lines), i+25)):
            print(f"{j+1}: {lines[j]}", end='')
