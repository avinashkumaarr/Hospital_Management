with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("--- modal-rx-slip (1830 to 1880) ---")
for i in range(1828, min(1885, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')

print("\n--- modal-reschedule-appointment (1985 to 2030) ---")
for i in range(1985, min(2030, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')
