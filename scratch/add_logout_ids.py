with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add IDs to logout buttons
html = html.replace(
    '<button class="btn-icon" onclick="logoutUser()" title="Sign Out of MediLink"',
    '<button class="btn-icon" id="btn-sidebar-logout" onclick="logoutUser()" title="Sign Out of MediLink"'
)

html = html.replace(
    '<button class="dropdown-item dropdown-item-danger" onclick="logoutUser(); closeProfileDropdown();">',
    '<button class="dropdown-item dropdown-item-danger" id="btn-dropdown-logout" onclick="logoutUser(); closeProfileDropdown();">'
)

html = html.replace(
    '<button class="btn btn-danger" onclick="logoutUser()" style="width:100%; justify-content:center;">',
    '<button class="btn btn-danger" id="btn-profile-logout" onclick="logoutUser()" style="width:100%; justify-content:center;">'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('Hospital_Management-master/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Added logout IDs to index.html!")
