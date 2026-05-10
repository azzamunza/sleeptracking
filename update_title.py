import re

filepath = "C:/Users/Aaron Munro/Documents/GitHub/sleeptracking/index.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# Replace the text inside the specific h3
html = html.replace('<h3>TWO WEEK SLEEP DIARY</h3>', '<h3>TWO WEEK SLEEP DIARY - Aaron Munro</h3>')

with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)
