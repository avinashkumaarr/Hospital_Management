with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for i in range(len(lines)-40, len(lines)):
    print(f"{i+1}: {lines[i]}", end='')
