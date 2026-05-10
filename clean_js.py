import re

filepath = "C:/Users/Aaron Munro/Documents/GitHub/sleeptracking/index.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# Fix the template literals (remove the extra backslashes introduced by python strings)
html = html.replace('\\${info.date}', '${info.date}')
html = html.replace('\\${info.day}', '${info.day}')
html = html.replace('\\${row.type_of_day || \'\'}', '${row.type_of_day || \'\'}')
html = html.replace('\\${formatHourLabel(h)}', '${formatHourLabel(h)}')
html = html.replace('\\${hData.note}', '${hData.note}')
html = html.replace('\\${allNotesForBottom.join(', '${allNotesForBottom.join(')

with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)
