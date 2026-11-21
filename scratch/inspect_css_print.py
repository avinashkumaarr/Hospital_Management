with open('static/css/styles.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1895, min(len(lines), 1960)):
    print(f"{i+1}: {lines[i]}", end='')
