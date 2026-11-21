import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("HTML Length:", len(html))

# Find all page sections
pages = re.findall(r'<div[^>]*id=["\'](page-[^"\']+)["\']', html)
print("Pages found:", pages)

# Find all modals
modals = re.findall(r'<div[^>]*id=["\'](modal-[^"\']+)["\']', html)
print("Modals found:", modals)

# Check search input in topbar
topbar_search = "search-input" in html or "global-search" in html or "Ctrl+K" in html
print("Global search mentions in HTML:", topbar_search)

# Check v3.0 mentions vs v4.0
v3_count = html.count("v3.0") + html.count("3.0")
v4_count = html.count("v4.0") + html.count("4.0")
print(f"Version occurrences: v3.0={v3_count}, v4.0={v4_count}")

# Check page-patients markup
match_patients = re.search(r'(<div[^>]*id=["\']page-patients["\'].*?)(<div[^>]*id=["\']page-|\Z)', html, re.DOTALL)
if match_patients:
    print("\n--- page-patients section preview (first 500 chars) ---")
    print(match_patients.group(1)[:500])
