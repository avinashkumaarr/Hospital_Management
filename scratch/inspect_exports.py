import os

routes_dir = 'backend/app/routers'
for f in os.listdir(routes_dir):
    if f.endswith('.py'):
        with open(os.path.join(routes_dir, f), 'r', encoding='utf-8') as fl:
            txt = fl.read()
            if 'csv' in txt.lower() or 'export' in txt.lower():
                print(f"Export mentions in {f}")
