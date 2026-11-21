with open('static/css/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

print("CSS length:", len(css))
print("Print rules in CSS:", "@media print" in css)
print("Modal rules in CSS:", ".modal-backdrop" in css)
print("Global search in CSS:", "global-search" in css)

if "@media print" in css:
    idx = css.find("@media print")
    print("\nPrint CSS block:\n", css[idx:idx+400])
