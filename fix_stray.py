import sys
import re

file_path = r"C:\Users\Aaron Munro\Documents\GitHub\sleeptracking\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# Fix 1: Remove stray legend pieces below Quick Entry
stray1 = """    
        <div><strong>M</strong> - Medicine</div>
        <div><strong>A</strong> - Alcohol</div>
        <div><strong>E</strong> - Exercise</div>
        <div><strong>B</strong> - Go to bed</div>
        <div><strong>Z</strong> - Asleep</div>
      </div>"""
html = html.replace(stray1, "")

# Fix 2: Remove stray legend pieces below TWO WEEK SLEEP DIARY
stray2 = """        <div><strong>M</strong> - Medicine</div>
        <div><strong>A</strong> - Alcohol</div>
        <div><strong>E</strong> - Exercise</div>
        <div><strong>B</strong> - Go to bed</div>
        <div><strong>Z</strong> - Asleep</div>
      </div>"""
html = html.replace(stray2, "")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
