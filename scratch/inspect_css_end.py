with open('static/css/styles.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("styles.css total lines:", len(lines))
print("\nLast 30 lines:")
for i in range(len(lines)-30, len(lines)):
    print(f"{i+1}: {lines[i]}", end='')
