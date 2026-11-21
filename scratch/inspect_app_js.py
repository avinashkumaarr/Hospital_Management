import re

with open('static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

print("JS Length:", len(js))

# Look for functions of interest
funcs_to_check = [
    'handleGlobalSearch',
    'openGlobalSearch',
    'openEditPatientModal',
    'savePatientEdit',
    'openReschedule',
    'confirmRescheduleAppointment',
    'printRx',
    'openRxSlip',
    'loadPatientDirectory',
    'loadPatients',
    'renderPatients',
    'beforeunload',
    'dirty',
    'unsaved'
]

for func in funcs_to_check:
    matches = re.findall(rf'function\s+{func}\b|window\.{func}\b|{func}\s*[:=]\s*function|async\s+function\s+{func}\b', js)
    count = js.count(func)
    print(f"{func}: defined={bool(matches)} (total mentions: {count})")
