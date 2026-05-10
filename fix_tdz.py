import sys

file_path = r"C:\Users\Aaron Munro\Documents\GitHub\sleeptracking\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# Remove the late declaration
html = html.replace("let showingTable = false;\n    function toggleView() {", "function toggleView() {")

# Add the declaration to the top variables block
vars_old = """    let allData = []; // Cache for table view/export
    let isPractitionerMode = false;
    let practitionerInviteId = new URLSearchParams(window.location.search).get('invite_id');"""

vars_new = """    let allData = []; // Cache for table view/export
    let isPractitionerMode = false;
    let practitionerInviteId = new URLSearchParams(window.location.search).get('invite_id');
    let showingTable = false;"""

html = html.replace(vars_old, vars_new)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
