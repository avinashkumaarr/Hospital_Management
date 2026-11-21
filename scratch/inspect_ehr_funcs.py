with open('static/js/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'viewPatientEhr' in l or 'startConsultationForPatient' in l:
        print(f"{i+1}: {l.strip()}")
