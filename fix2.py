import sys
import re

file_path = r"C:\Users\Aaron Munro\Documents\GitHub\sleeptracking\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# Fix 1a: Change initialization
html = html.replace("let showingTable = false;", "let showingTable = !!new URLSearchParams(window.location.search).get('invite_id');")

# Fix 1b: Remove showingTable = true
html = html.replace("    isPractitionerMode = true;\n    showingTable = true;", "    isPractitionerMode = true;")

# Fix 2: Auth URL check
html = html.replace("if (event === 'SIGNED_IN' && (window.location.hash || window.location.search)) {", "if (event === 'SIGNED_IN' && new URLSearchParams(window.location.search).has('code')) {")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
