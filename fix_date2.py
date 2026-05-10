import sys
import re

file_path = r"C:\Users\Aaron Munro\Documents\GitHub\sleeptracking\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

html = re.sub(r'<td>\$\{info\.date\}</td>\s*<td>\$\{info\.day\}</td>\s*<td>\$\{row\.type_of_day \|\| \'\'\}</td>',
              r'<td class="table-date">${info.date}</td>\n            <td>${info.day}</td>\n            <td class="table-type">${row.type_of_day || \'\'}</td>',
              html)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
