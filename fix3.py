import sys

file_path = r"C:\Users\Aaron Munro\Documents\GitHub\sleeptracking\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# Fix 1b: Remove showingTable = true
html = html.replace("      isPractitionerMode = true;\n      showingTable = true;", "      isPractitionerMode = true;")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
