import shutil
import os

files_to_sync = [
    ('index.html', 'Hospital_Management-master/index.html'),
    ('server.py', 'Hospital_Management-master/server.py'),
    ('README.md', 'Hospital_Management-master/README.md'),
    ('backend/app/config.py', 'Hospital_Management-master/backend/app/config.py'),
    ('backend/app/routers/backup.py', 'Hospital_Management-master/backend/app/routers/backup.py'),
    ('backend/app/routers/patients.py', 'Hospital_Management-master/backend/app/routers/patients.py'),
    ('backend/tests/test_api.py', 'Hospital_Management-master/backend/tests/test_api.py'),
    ('static/css/styles.css', 'Hospital_Management-master/static/css/styles.css'),
    ('static/js/app.js', 'Hospital_Management-master/static/js/app.js'),
    ('static/js/api.js', 'Hospital_Management-master/static/js/api.js')
]

for src, dst in files_to_sync:
    if os.path.exists(src):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        print(f"Synced {src} -> {dst}")
print("Sync complete.")
