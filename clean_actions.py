import re

filepath = "C:/Users/Aaron Munro/Documents/GitHub/sleeptracking/index.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# Remove the old actions block completely
pattern = re.compile(r'<!-- Actions -->\s*<div class="card flex-between">\s*<div>\s*<button id="toggle-btn" onclick="toggleView\(\)">.*?</button>\s*</div>\s*</div>', re.DOTALL)
html = pattern.sub('', html)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)
