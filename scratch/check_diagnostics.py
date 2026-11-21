import os, sys, re, json, glob
from html.parser import HTMLParser

print("=== CHECKING REPOSITORY FOR DIAGNOSTICS ===")

# 1. Check HTML
html_path = "index.html"
with open(html_path, "r", encoding="utf-8") as f:
    html_lines = f.readlines()

dup_attr = []
unclosed = []
tag_stack = []
void_tags = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

class StrictHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []
    def handle_starttag(self, tag, attrs):
        attr_names = [a[0] for a in attrs]
        seen = set()
        for a in attr_names:
            if a in seen:
                self.errors.append((f"Duplicate attribute '{a}' on <{tag}>", self.getpos()))
            seen.add(a)

p = StrictHTMLParser()
p.feed("".join(html_lines))
print(f"HTML duplicate attributes: {len(p.errors)}")
for e in p.errors[:10]:
    print(" ", e)

# 2. Check JavaScript files
js_files = ["static/js/api.js", "static/js/app.js"]
for js_path in js_files:
    with open(js_path, "r", encoding="utf-8") as f:
        js_code = f.read()
    # Check for undefined variables, syntax, etc. using node
    import subprocess
    res = subprocess.run(["node", "--check", js_path], capture_output=True, text=True)
    print(f"Node syntax check {js_path}: rc={res.returncode}")
    if res.stderr:
        print(" ", res.stderr.strip()[:300])

# 3. Check Python files with Pyright or basic checks
py_files = sorted(glob.glob("backend/**/*.py", recursive=True) + glob.glob("*.py"))
print(f"Total Python files: {len(py_files)}")

# 4. Check schema.sql
with open("schema.sql", "r", encoding="utf-8") as f:
    sql_lines = f.readlines()
print(f"schema.sql lines: {len(sql_lines)}")
