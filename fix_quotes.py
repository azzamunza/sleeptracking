import sys
file_path = r"C:\Users\Aaron Munro\Documents\GitHub\sleeptracking\index.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()
html = html.replace("\\'\\'", "''")
with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
