with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1815, min(1865, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')
