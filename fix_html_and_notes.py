import re

filepath = "C:/Users/Aaron Munro/Documents/GitHub/sleeptracking/index.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# Fix the My Data card. Currently it's:
# <div class="card flex-between section-card">
html = html.replace('<div class="card flex-between section-card">', '<div class="card section-card">')


# The Notes Layout:
# We need to change how the notes are rendered. If notesUnderneath is true, instead of adding them under EACH row, we should add them all at the very bottom of the table.

notes_js = """
    // Override renderTable to support Notes Underneath
    const origRenderTable = renderTable;
    renderTable = function() {
        if (!notesUnderneath) {
            origRenderTable();
            const table = document.querySelector('#table-container table');
            if (tableZoom && table) table.classList.add('table-zoom-fit');
            return;
        }
        
        // Notes underneath layout
        const container = document.getElementById('table-container');
        let html = `<table>
          <thead>
            <tr>
              <th class="table-date">Date</th>
              <th>Day</th>
              <th class="table-type">Type of day</th>`;
        hourOrder.forEach(h => { html += `<th>${formatHourLabel(h)}</th>`; });
        html += `</tr></thead><tbody>`;

        let allNotesForBottom = [];

        allData.forEach(row => {
          const info = formatDisplayDate(row.date_string);
          html += `<tr>
            <td class="table-date">${info.date}</td>
            <td>${info.day}</td>
            <td class="table-type">${row.type_of_day || ''}</td>`;
            
          let dayNotes = [];
          const hours = row.hours || {};
          
          hourOrder.forEach(h => {
            const hData = hours[h];
            const marks = hData && hData.markers ? hData.markers.join(',') : '';
            if (hData && hData.note) {
              dayNotes.push(`${formatHourLabel(h)}:\\n${hData.note}`);
            }
            html += `<td>${marks}</td>`;
          });
          html += `</tr>`;
          
          if (dayNotes.length > 0) {
              allNotesForBottom.push(`<strong>${info.date} (${info.day})</strong><br>` + dayNotes.join('<br><br>').replace(/\\n/g, '<br>'));
          }
        });
        
        if (showingNotes && allNotesForBottom.length > 0) {
            html += `<tr><td colspan="${3 + hourOrder.length}" class="table-notes" style="background:var(--input-bg); border-top:2px solid #aaa; padding: 15px;">
                <div style="font-size: 14px;"><h3>Notes</h3>${allNotesForBottom.join('<br><hr style="border:none;border-top:1px solid #555;margin:10px 0;"><br>')}</div>
            </td></tr>`;
        }
        
        html += `</tbody></table>`;
        container.innerHTML = html;
        
        const table = document.querySelector('#table-container table');
        if (tableZoom && table) table.classList.add('table-zoom-fit');
    };
"""

# Replace the old override with the new override
pattern = re.compile(r'// Override renderTable to support Notes Underneath\s+const origRenderTable.*?};\s+// Initial calls', re.DOTALL)
html = pattern.sub(notes_js.replace('\\n', '\\\\n') + "\n    // Initial calls", html)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)
