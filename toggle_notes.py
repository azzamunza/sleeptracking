import sys
import re

file_path = r"C:\Users\Aaron Munro\Documents\GitHub\sleeptracking\index.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Variables
var_old = "let showingTable = !!new URLSearchParams(window.location.search).get('invite_id');"
var_new = "let showingTable = !!new URLSearchParams(window.location.search).get('invite_id');\n    let showingNotes = true;"
html = html.replace(var_old, var_new)

# 2. Toggle button in HTML
btn_old = """    <div class="card flex-between">
      <button id="toggle-btn" onclick="toggleView()">Toggle Table View</button>"""
btn_new = """    <div class="card flex-between">
      <div>
        <button id="toggle-btn" onclick="toggleView()">Toggle Table View</button>
        <button id="toggle-notes-btn" onclick="toggleNotes()" class="outline" style="margin-left: 5px;">Toggle Notes</button>
      </div>"""
html = html.replace(btn_old, btn_new)

# 3. Exempt button from Practitioner Mode lock
qsa_old = "not(#export-pdf):not(#prev-day-btn):not(#next-day-btn):not(#prev-summary-btn):not(#next-summary-btn)');"
qsa_new = "not(#export-pdf):not(#prev-day-btn):not(#next-day-btn):not(#prev-summary-btn):not(#next-summary-btn):not(#toggle-notes-btn)');"
html = html.replace(qsa_old, qsa_new)

# 4. JS Toggle Function
toggle_js = """    function toggleNotes() {
      showingNotes = !showingNotes;
      if (showingTable) renderTable();
    }
    
    function toggleView() {"""
html = html.replace("    function toggleView() {", toggle_js)

# 5. renderTable modifications
render_table_old_start = """        hourOrder.forEach(h => {
          html += `<th>${formatHourLabel(h)}</th>`;
        });
        html += `<th>Notes</th></tr></thead><tbody>`;"""
render_table_new_start = """        hourOrder.forEach(h => {
          html += `<th>${formatHourLabel(h)}</th>`;
        });
        if (showingNotes) html += `<th>Notes</th>`;
        html += `</tr></thead><tbody>`;"""
html = html.replace(render_table_old_start, render_table_new_start)

render_table_old_end = """          }
          html += `<td>${marks}</td>`;
        });
        
        html += `<td class="table-notes">${dayNotes.join('\\n\\n')}</td></tr>`;
      });"""
render_table_new_end = """          }
          html += `<td>${marks}</td>`;
        });
        
        if (showingNotes) {
          html += `<td class="table-notes">${dayNotes.join('\\n\\n')}</td>`;
        }
        html += `</tr>`;
      });"""
html = html.replace(render_table_old_end, render_table_new_end)

# 6. Print CSS Modifications
print_css_old = """    /* Print Styles */
    @media print {
      @page { size: landscape; margin: 10mm; }
      body { background: white !important; margin: 0; padding: 0; color: black !important; }
      #auth-section, .card:not(#table-view), button, input, img { display: none !important; }
      #app { display: block !important; }
      #table-view { display: block !important; box-shadow: none; border: none; padding: 0; margin: 0; background: white !important; color: black !important; }
      #table-view h3 { font-size: 18px; margin-bottom: 5px; color: black !important; }
      table { width: 100%; border-collapse: collapse; font-size: 10px; min-width: auto; background: white !important; color: black !important; }
      th, td { border: 1px solid black !important; padding: 4px; color: black !important; }
      th { background: #eee !important; color: black !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
      .table-notes, .table-type, .table-date { color: black !important; }
      .note-item { border-bottom: 1px solid #aaa !important; }
      div { color: black !important; background: transparent !important; }
    }"""
print_css_new = """    /* Print Styles */
    @media print {
      @page { size: landscape; margin: 10mm; }
      body { background: white !important; margin: 0; padding: 0; color: black !important; }
      #auth-section, .card:not(#table-view), button, input, img { display: none !important; }
      #app { display: block !important; }
      #table-view { display: block !important; box-shadow: none; border: none; padding: 0; margin: 0; background: white !important; color: black !important; }
      #table-view h3 { font-size: 18px; margin-bottom: 5px; color: black !important; }
      table { width: 100% !important; max-width: 100% !important; border-collapse: collapse; font-size: 9px; min-width: 0 !important; background: white !important; color: black !important; table-layout: auto; }
      th, td { border: 1px solid black !important; padding: 2px; color: black !important; word-wrap: break-word; }
      th { background: #eee !important; color: black !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
      .table-notes, .table-type, .table-date { color: black !important; min-width: 0 !important; width: auto !important; white-space: normal !important; }
      .note-item { border-bottom: 1px solid #aaa !important; }
      div { color: black !important; background: transparent !important; }
    }"""
html = html.replace(print_css_old, print_css_new)


with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
