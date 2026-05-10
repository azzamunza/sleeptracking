import sys

file_path = r"C:\Users\Aaron Munro\Documents\GitHub\sleeptracking\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update CSS
css_old = ".table-notes { text-align: left; min-width: 250px; hyphens: none; word-wrap: break-word; vertical-align: top; }"
css_new = ".table-notes { text-align: left; min-width: 250px; hyphens: none; word-wrap: break-word; vertical-align: top; white-space: pre-wrap; }"
html = html.replace(css_old, css_new)

# 2. Update renderTable notes format
rt_old = """          if (hData && hData.note) {
            dayNotes.push(`${formatHourLabel(h)}: ${hData.note}`);
          }
          html += `<td>${marks}</td>`;
        });
        
        html += `<td class="table-notes">${dayNotes.join('\\n')}</td></tr>`;"""
rt_new = """          if (hData && hData.note) {
            dayNotes.push(`${formatHourLabel(h)}:\n${hData.note}`);
          }
          html += `<td>${marks}</td>`;
        });
        
        html += `<td class="table-notes">${dayNotes.join('\\n\\n')}</td></tr>`;"""
html = html.replace(rt_old, rt_new)

# 3. Update exportCSV notes format
csv_old = """          if (hData && hData.note) {
            dayNotes.push(`${formatHourLabel(h)}: ${hData.note}`);
          }
        });
        rowStr += `"${dayNotes.join(' | ')}"\\n`;"""
csv_new = """          if (hData && hData.note) {
            dayNotes.push(`${formatHourLabel(h)}:\n${hData.note}`);
          }
        });
        rowStr += `"${dayNotes.join('\\n\\n')}"\\n`;"""
html = html.replace(csv_old, csv_new)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
