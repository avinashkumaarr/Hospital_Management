import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Search for any tag with id starting with page-
all_pages = re.findall(r'<([a-zA-Z0-9]+)[^>]*id=["\'](page-[^"\']+)["\']', html)
print("All page tags and IDs:", all_pages)

# Check all elements with modal in id
all_modals = re.findall(r'<([a-zA-Z0-9]+)[^>]*id=["\']([^"\']*modal[^"\']*)["\']', html)
print("All modal IDs:", all_modals)

# Find topbar / search
match_topbar = re.search(r'(<header.*?header>)', html, re.DOTALL)
if match_topbar:
    print("\nTopbar found length:", len(match_topbar.group(1)))
    # print search related lines in topbar
    for line in match_topbar.group(1).splitlines():
        if 'search' in line.lower() or 'ctrl' in line.lower() or 'input' in line.lower():
            print("Topbar search line:", line.strip())

# Find modal-rx-slip
match_rx = re.search(r'(<div[^>]*id=["\']modal-rx-slip["\'].*?</div>\s*</div>)', html, re.DOTALL)
if match_rx:
    print("\nmodal-rx-slip preview:\n", match_rx.group(1)[:400])

# Find modal-reschedule-appointment
match_resched = re.search(r'(<div[^>]*id=["\']modal-reschedule-appointment["\'].*?</div>\s*</div>)', html, re.DOTALL)
if match_resched:
    print("\nmodal-reschedule-appointment preview:\n", match_resched.group(1)[:400])
