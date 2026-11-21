import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

print("--- Check handleGlobalSearch in HTML & JS ---")
for line in html.splitlines():
    if 'handleGlobalSearch' in line or 'global-search' in line:
        print("HTML:", line.strip())

print("\n--- Check loadPatientDirectory in JS ---")
m = re.search(r'(function\s+loadPatientDirectory[\s\S]*?)(function|\Z)', js)
if m:
    print(m.group(1)[:1200])

print("\n--- Check modal-rx-slip in JS ---")
for line in js.splitlines():
    if 'modal-rx-slip' in line or 'printable-rx' in line or 'rx-slip' in line:
        print("JS:", line.strip())

print("\n--- Check confirmRescheduleAppointment in JS ---")
m = re.search(r'(function\s+confirmRescheduleAppointment[\s\S]*?)(function|\Z)', js)
if m:
    print(m.group(1)[:800])

print("\n--- Check modal-reschedule-appointment in JS ---")
for line in js.splitlines():
    if 'modal-reschedule-appointment' in line or 'reschedule' in line.lower():
        print("JS:", line.strip())
