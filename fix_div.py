import sys
import re

file_path = r"C:\Users\Aaron Munro\Documents\GitHub\sleeptracking\index.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# Fix the extra </div>
html = html.replace("""    </div>\n\n\n    </div>\n\n\n        <!-- Daily Summary -->""", """    </div>\n\n\n        <!-- Daily Summary -->""")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
