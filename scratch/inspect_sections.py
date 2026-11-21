with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("--- Version strings in index.html ---")
for i, l in enumerate(lines):
    if '3.0' in l or 'Enterprise' in l:
        print(f"{i+1}: {l.strip()[:100]}")

print("\n--- page-patients section ---")
in_patients = False
patients_lines = []
for i, l in enumerate(lines):
    if 'id="page-patients"' in l:
        in_patients = True
    if in_patients:
        patients_lines.append(f"{i+1}: {l}")
        if '</section>' in l:
            break
print(''.join(patients_lines[:35]))
print(f"... ({len(patients_lines)} total lines in page-patients)")

print("\n--- Modals at bottom of index.html ---")
for i, l in enumerate(lines):
    if 'class="modal-backdrop"' in l:
        print(f"{i+1}: {l.strip()}")
