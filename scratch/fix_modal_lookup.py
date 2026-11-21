with open('static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_func = '''async function openEditPatientModal(aadhaar) {
  let patient = (appState.patients || []).find(p => p.aadhaar_number === aadhaar);
  if (!patient) {
    try {
      patient = await window.api.getPatient(aadhaar);
    } catch (e) {
      toast('Failed to load patient: ' + e.message, true);
      return;
    }
  }'''

new_func = '''async function openEditPatientModal(aadhaar) {
  const clean = String(aadhaar).replace(/\s+/g, '');
  let patient = (appState.patients || []).find(p => String(p.aadhaar_number).replace(/\s+/g, '') === clean);
  if (!patient) {
    try {
      patient = await window.api.getPatient(clean);
    } catch (e) {
      toast('Failed to load patient: ' + e.message, true);
      return;
    }
  }'''

assert old_func in js, "Could not find old_func in app.js"
js = js.replace(old_func, new_func)

with open('static/js/app.js', 'w', encoding='utf-8') as f:
    f.write(js)

with open('Hospital_Management-master/static/js/app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated openEditPatientModal in both files successfully!")
