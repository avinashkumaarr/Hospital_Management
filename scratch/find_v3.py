import os

def search_v3(dir_path):
    for root, dirs, files in os.walk(dir_path):
        if any(skip in root for skip in ['.git', '__pycache__', '.pytest_cache', 'scratch']):
            continue
        for f in files:
            if f.endswith(('.html', '.js', '.py', '.md', '.css', '.sql')):
                path = os.path.join(root, f)
                try:
                    with open(path, 'r', encoding='utf-8') as fl:
                        content = fl.read()
                        if 'v3.0' in content or '3.0' in content:
                            c = content.count('v3.0') + content.count('3.0')
                            print(f"{path}: {c} matches")
                except Exception as e:
                    pass

search_v3('.')
