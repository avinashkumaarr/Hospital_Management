with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'global-search-box' in l:
        print(f"Around line {i+1}:")
        for j in range(max(0, i-2), min(i+6, len(lines))):
            print(f"{j+1}: {repr(lines[j])}")
