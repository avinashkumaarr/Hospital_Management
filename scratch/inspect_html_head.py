with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(0, 30):
    print(f"{i+1}: {lines[i]}", end='')
