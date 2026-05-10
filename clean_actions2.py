import re

filepath = "C:/Users/Aaron Munro/Documents/GitHub/sleeptracking/index.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# Delete the OLD Actions block.
pattern = r'<!-- Actions -->\s*<div class="card flex-between">\s*<div>\s*<button id="toggle-btn" onclick="toggleView\(\)">Toggle Table View</button>\s*<button class="outline" id="toggle-notes-btn" onclick="toggleNotes\(\)" style="margin-left: 5px;">Toggle Notes</button>\s*</div>\s*<div>\s*<button class="outline" id="export-csv" onclick="exportCSV\(\)">Export CSV</button>\s*<button class="outline" id="export-json" onclick="exportJSON\(\)">Export JSON</button>\s*<button class="outline" id="export-pdf" onclick="printPDF\(\)">Export PDF</button>\s*</div>\s*</div>'

new_html = re.sub(pattern, '', html)

if html != new_html:
    print("Successfully removed old Actions card.")
else:
    print("Could not find old Actions card to remove.")

with open(filepath, "w", encoding="utf-8") as f:
    f.write(new_html)
