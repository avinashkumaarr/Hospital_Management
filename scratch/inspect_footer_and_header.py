with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("--- Header right section (around line 815) ---")
for i in range(810, 835):
    print(f"{i+1}: {lines[i]}", end='')

print("\n--- Sidebar footer section (around line 750) ---")
for i in range(745, 765):
    print(f"{i+1}: {lines[i]}", end='')
