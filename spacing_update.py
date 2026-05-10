import sys

file_path = r"C:\Users\Aaron Munro\Documents\GitHub\sleeptracking\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# Increase padding/spacing for note-item
old_css = ".note-item { border-bottom: 1px solid #ccc; padding: 4px 0; margin: 0; }"
new_css = ".note-item { border-bottom: 1px solid #ccc; padding: 8px 0; margin-bottom: 4px; line-height: 1.4; }"

html = html.replace(old_css, new_css)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
