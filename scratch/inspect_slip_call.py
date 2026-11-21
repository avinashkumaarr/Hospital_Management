with open('static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

for line in js.splitlines():
    if 'openPrescriptionSlipByRecordId' in line:
        print(line)
