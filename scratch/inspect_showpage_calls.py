with open('static/js/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(422, 460):
    print(f"{i+1}: {lines[i]}", end='')
