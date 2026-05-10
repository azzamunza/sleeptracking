import re
from bs4 import BeautifulSoup

filepath = "C:/Users/Aaron Munro/Documents/GitHub/sleeptracking/index.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# 1. Fix My Data Header Column Issue
# The previous card was <div class="card flex-between section-card">
my_data_card = soup.find("div", class_="card flex-between section-card")
if my_data_card:
    my_data_card["class"] = ["card", "section-card"] # Remove flex-between

# 2. Add headers/collapsibles to Navigation and Hourly Log
# Navigation Card
nav_card = soup.find("div", id="nav-wrapper")
if nav_card:
    inner_card = nav_card.find("div", class_="card")
    if inner_card:
        inner_card["class"] = inner_card.get("class", []) + ["section-card"]
        
        # Build header
        header_div = soup.new_tag("div", attrs={"class": "section-header", "onclick": "this.parentElement.classList.toggle('collapsed')"})
        h3 = soup.new_tag("h3")
        h3.string = "Navigation"
        header_div.append(h3)
        icon = soup.new_tag("span", attrs={"class": "collapse-icon"})
        icon.string = "▼"
        header_div.append(icon)
        
        # Build content
        content_div = soup.new_tag("div", attrs={"class": "section-content"})
        for child in list(inner_card.children):
            content_div.append(child)
            
        inner_card.clear()
        inner_card.append(header_div)
        inner_card.append(content_div)

# Hourly Log Card
hourly_view = soup.find("div", id="hourly-view")
if hourly_view:
    hourly_view["class"] = hourly_view.get("class", []) + ["section-card"]
    
    # Build header
    header_div = soup.new_tag("div", attrs={"class": "section-header", "onclick": "this.parentElement.classList.toggle('collapsed')"})
    h3 = soup.new_tag("h3")
    h3.string = "Hourly Log"
    header_div.append(h3)
    icon = soup.new_tag("span", attrs={"class": "collapse-icon"})
    icon.string = "▼"
    header_div.append(icon)
    
    # Build content
    content_div = soup.new_tag("div", attrs={"class": "section-content"})
    # Find the old h3 and spans
    old_h3 = hourly_view.find("h3")
    if old_h3: old_h3.decompose()
    
    for child in list(hourly_view.children):
        content_div.append(child)
        
    hourly_view.clear()
    hourly_view.append(header_div)
    hourly_view.append(content_div)

# 3. Fix Legend Wrapping
# We need to make sure the legend doesn't wrap and has enough space.
legend_div = soup.find("div", string=lambda s: s and "Coffee" in s and "|" in s)
if not legend_div:
    # Try finding via strong
    strong = soup.find("strong", string="C")
    if strong:
        legend_div = strong.find_parent("div")

if legend_div:
    legend_div["style"] = "font-size: 11px; margin-bottom: 10px; background: #162444; padding: 10px; border: 1px solid #aaa; text-align: center; white-space: nowrap; overflow-x: auto;"

# 4. Notes Section Separate from Table
# Add a container for notes underneath the table
table_view = soup.find("div", id="table-view")
if table_view:
    notes_section = soup.new_tag("div", attrs={"id": "table-notes-bottom", "style": "margin-top: 15px; display: none;"})
    table_view.append(notes_section)

# Convert to string to apply JS regex fixes
new_html = str(soup)

# 5. Fix JS Crash (remove reference to deleted element)
new_html = new_html.replace("document.getElementById('current-hour-display').textContent = `Current: ${formatHourLabel(now.getHours())} - ${getWordedDate(getDiaryDateStr(now))}`;", "// Time display moved to header")

# 6. Fix Notes JS to use the new div
notes_js_fix = """
    // Override renderTable to support Notes Underneath
    const origRenderTable = renderTable;
    renderTable = function() {
        if (!notesUnderneath) {
            origRenderTable();
            document.getElementById('table-notes-bottom').style.display = 'none';
            const table = document.querySelector('#table-container table');
            if (tableZoom && table) table.classList.add('table-zoom-fit');
            return;
        }
        
        // Notes underneath layout
        const container = document.getElementById('table-container');
        const notesContainer = document.getElementById('table-notes-bottom');
        
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
            <td class="table-date">\${info.date}</td>
            <td>\${info.day}</td>
            <td class="table-type">\${row.type_of_day || ''}</td>`;
            
          let dayNotes = [];
          const hours = row.hours || {};
          
          hourOrder.forEach(h => {
            const hData = hours[h];
            const marks = hData && hData.markers ? hData.markers.join(',') : '';
            if (hData && hData.note) {
              dayNotes.push(`<strong>\${formatHourLabel(h)}</strong>:\\n\${hData.note}`);
            }
            html += `<td>\${marks}</td>`;
          });
          html += `</tr>`;
          
          if (dayNotes.length > 0) {
              allNotesForBottom.push(`<h3>\${info.date} (\${info.day})</h3>` + dayNotes.join('<br><br>').replace(/\\\\n/g, '<br>'));
          }
        });
        
        html += `</tbody></table>`;
        container.innerHTML = html;
        
        if (showingNotes && allNotesForBottom.length > 0) {
            notesContainer.style.display = 'block';
            notesContainer.innerHTML = `<div class="card"><div style="padding: 10px;"><h2>Diary Notes</h2><hr style="border:none;border-top:1px solid #555;margin:10px 0;">\${allNotesForBottom.join('<br><hr style="border:none;border-top:1px solid #555;margin:10px 0;"><br>')}</div></div>`;
        } else {
            notesContainer.style.display = 'none';
        }
        
        const table = document.querySelector('#table-container table');
        if (tableZoom && table) table.classList.add('table-zoom-fit');
    };
"""

# The above code used double slashes and templates, need to be careful.
# I'll use a simpler replacement for the notes JS.
pattern = re.compile(r'// Override renderTable to support Notes Underneath.*?// Initial calls', re.DOTALL)
new_html = pattern.sub(notes_js_fix + "\n    // Initial calls", new_html)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(new_html)
