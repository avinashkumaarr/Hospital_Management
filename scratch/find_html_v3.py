with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '3.0' in l:
        print(f"Line {i+1}: {repr(l)}")
