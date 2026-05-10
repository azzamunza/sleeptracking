import sys

file_path = r"C:\Users\Aaron Munro\Documents\GitHub\sleeptracking\index.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# Fix the renderTable headers logic for showingNotes
render_table_old_start = """      hourOrder.forEach(h => {
        html += `<th>${formatHourLabel(h)}</th>`;
      });
      html += `<th>Notes</th></tr></thead><tbody>`;"""

render_table_new_start = """      hourOrder.forEach(h => {
        html += `<th>${formatHourLabel(h)}</th>`;
      });
      if (showingNotes) html += `<th>Notes</th>`;
      html += `</tr></thead><tbody>`;"""

html = html.replace(render_table_old_start, render_table_new_start)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
