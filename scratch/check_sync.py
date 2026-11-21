import os
import filecmp

root_files = ['index.html', 'server.py', 'README.md', 'pyrefly.toml', '.vscode/settings.json']

for rf in root_files:
    inner = os.path.join('Hospital_Management-master', rf)
    if os.path.exists(inner):
        same = filecmp.cmp(rf, inner, shallow=False)
        print(f"{rf}: {'Identical' if same else 'Different'}")
