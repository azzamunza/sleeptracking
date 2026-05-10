import sys
import re

file_path = r"C:\Users\Aaron Munro\Documents\GitHub\sleeptracking\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. CSS Updates
css_old = ".table-notes { text-align: left; max-width: 200px; white-space: pre-wrap; }"
css_new = """    .table-date { min-width: 90px; white-space: nowrap; }
    .table-type { min-width: 250px; hyphens: none; word-wrap: break-word; text-align: left; }
    .table-notes { text-align: left; min-width: 250px; hyphens: none; word-wrap: break-word; vertical-align: top; }
    .note-item { border-bottom: 1px solid #ccc; padding: 4px 0; margin: 0; }
    .note-item:last-child { border-bottom: none; }"""
html = html.replace(css_old, css_new)

# 2. renderTable Header Updates
header_old = """            <tr>
              <th>Date</th>
              <th>Day</th>
              <th>Type</th>`;"""
header_new = """            <tr>
              <th class="table-date">Date</th>
              <th>Day</th>
              <th class="table-type">Type of day</th>`;"""
html = html.replace(header_old, header_new)

# 3. renderTable Row Updates
row_old = """          html += `<tr>
            <td>${info.date}</td>
            <td>${info.day}</td>
            <td>${row.type_of_day || ''}</td>`;"""
row_new = """          html += `<tr>
            <td class="table-date">${info.date}</td>
            <td>${info.day}</td>
            <td class="table-type">${row.type_of_day || ''}</td>`;"""
html = html.replace(row_old, row_new)

# 4. Notes Array Construction
notes_old = """            if (hData && hData.note) {
              dayNotes.push(`${formatHourLabel(h)}: ${hData.note}`);
            }
            html += `<td>${marks}</td>`;
          });
          
          html += `<td class="table-notes">${dayNotes.join('\\n')}</td></tr>`;"""
notes_new = """            if (hData && hData.note) {
              dayNotes.push(`<div class="note-item"><strong>${formatHourLabel(h)}:</strong> ${hData.note}</div>`);
            }
            html += `<td>${marks}</td>`;
          });
          
          html += `<td class="table-notes">${dayNotes.join('')}</td></tr>`;"""
html = html.replace(notes_old, notes_new)


with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
