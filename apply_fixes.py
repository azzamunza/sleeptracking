import re

filepath = "C:/Users/Aaron Munro/Documents/GitHub/sleeptracking/index.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Fix ${marks} bug
html = html.replace('<td>\${marks}</td>', '<td>${marks}</td>')

# 2. Add Open Full Screen button logic
full_screen_js = """
    function openFullScreenTable() {
        const tableHTML = document.getElementById('table-view').innerHTML;
        const printStyles = document.querySelector('style').innerHTML;
        const newWindow = window.open('', '_blank');
        newWindow.document.write(`
            <html><head><title>Sleep Diary - Full Screen</title>
            <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap" rel="stylesheet">
            <style>
                ${printStyles}
                body { background: var(--bg); color: var(--text); padding: 20px; }
                h3 { color: var(--text) !important; }
                /* Scale container to fit window */
                #scale-container {
                    width: 100%;
                    overflow: hidden;
                    transform-origin: top left;
                }
                table { background: var(--card-bg) !important; color: var(--text) !important; }
                th, td { border: 1px solid #555 !important; color: var(--text) !important; }
                th { background: #162444 !important; }
                .table-notes, .table-type, .table-date { white-space: pre-wrap !important; color: var(--text) !important; }
                @media print {
                   body { background: white !important; color: black !important; padding: 0; }
                   h3 { color: black !important; }
                   table { background: white !important; color: black !important; }
                   th, td { border: 1px solid black !important; color: black !important; }
                   th { background: #eee !important; color: black !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
                   .table-notes, .table-type, .table-date { color: black !important; }
                }
            </style>
            </head><body>
            <div id="scale-container">
            ${tableHTML}
            </div>
            <script>
                function scaleToFit() {
                    const container = document.getElementById('scale-container');
                    const table = container.querySelector('table');
                    if (table) {
                        const tableWidth = table.offsetWidth;
                        const windowWidth = window.innerWidth - 40; // padding
                        if (tableWidth > windowWidth) {
                            const scale = windowWidth / tableWidth;
                            container.style.transform = 'scale(' + scale + ')';
                            container.style.height = (table.offsetHeight * scale) + 'px';
                        } else {
                            container.style.transform = 'none';
                            container.style.height = 'auto';
                        }
                    }
                }
                window.onload = scaleToFit;
                window.onresize = scaleToFit;
            </script>
            </body></html>
        `);
        newWindow.document.close();
    }
"""
html = html.replace('// --- New Mod Functions ---', full_screen_js + '\n    // --- New Mod Functions ---')

# 3. Modify Toggle buttons in My Data
# Change 'Toggle Table View' -> 'Diary' (or toggle depending on state, we'll just set it to "Diary / Log")
html = html.replace('<button id="toggle-btn" onclick="toggleView()">Toggle Table View</button>', '<button id="toggle-btn" onclick="toggleView()">Diary / Log</button>')

# Remove Zoom to Fit button
html = re.sub(r'<button class="outline" id="toggle-zoom-btn" onclick="toggleTableZoom\(\)">.*?</button>', '', html)

# Change Notes Layout button to use unicode
html = html.replace('<button class="outline" id="toggle-notes-loc-btn" onclick="toggleNotesLocation()">Notes Layout: Side</button>', '<button class="outline" id="toggle-notes-loc-btn" onclick="toggleNotesLocation()">Notes Pos: ◨</button>')

# Add Full Screen Button to the Export section (Col 1 since zoom was removed)
html = html.replace('<div style="display:flex; flex-direction:column; gap:5px;"><button id="toggle-btn" onclick="toggleView()">Diary / Log</button></div>', '<div style="display:flex; flex-direction:column; gap:5px;"><button id="toggle-btn" onclick="toggleView()">Diary / Log</button><button class="outline" id="full-screen-btn" onclick="openFullScreenTable()">Open Full Screen</button></div>')

# Update the JS for Notes Pos toggle
notes_loc_js = """
    function toggleNotesLocation() {
        notesUnderneath = !notesUnderneath;
        const btn = document.getElementById('toggle-notes-loc-btn');
        if (btn) btn.textContent = notesUnderneath ? "Notes Pos: ⬓" : "Notes Pos: ◨";
        if (showingTable) renderTable();
    }
"""
pattern = re.compile(r'function toggleNotesLocation\(\) \{.*?\n    \}', re.DOTALL)
html = pattern.sub(notes_loc_js.strip(), html)


# 4. Remove the old table-zoom-fit CSS and references as requested
html = re.sub(r'/\* Table zoom to fit \*/.*?\.table-zoom-fit th, \.table-zoom-fit td \{ word-wrap: break-word; overflow: hidden; \}', '', html, flags=re.DOTALL)
html = re.sub(r'// Zoom Toggle.*?\n    \}', '', html, flags=re.DOTALL)

# Clean up JS override to not use tableZoom
override_js = """
    // Override renderTable to support Notes Underneath
    const origRenderTable = renderTable;
    renderTable = function() {
        if (!notesUnderneath) {
            origRenderTable();
            document.getElementById('table-notes-bottom').style.display = 'none';
            return;
        }
"""
pattern = re.compile(r'// Override renderTable to support Notes Underneath\s+const origRenderTable = renderTable;\s+renderTable = function\(\) \{\s+if \(!notesUnderneath\) \{\s+origRenderTable\(\);\s+document\.getElementById\(\'table-notes-bottom\'\)\.style\.display = \'none\';\s+const table = document\.querySelector\(\'#table-container table\'\);\s+if \(tableZoom && table\) table\.classList\.add\(\'table-zoom-fit\'\);\s+return;\s+\}')
html = pattern.sub(override_js.strip(), html)

html = re.sub(r'const table = document\.querySelector\(\'#table-container table\'\);\s+if \(tableZoom && table\) table\.classList\.add\(\'table-zoom-fit\'\);', '', html)


# 5. Fix Legend on Two Lines
legend_html = """
<div style="font-size: 11px; margin-bottom: 10px; background: #162444; padding: 10px; border: 1px solid #aaa; text-align: center; white-space: nowrap; overflow-x: auto; display: flex; flex-direction: column; gap: 5px;">
    <div><strong>C</strong> - Coffee &nbsp;|&nbsp; <strong>M</strong> - Medicine &nbsp;|&nbsp; <strong>A</strong> - Alcohol</div>
    <div><strong>E</strong> - Exercise &nbsp;|&nbsp; <strong>B</strong> - Go to bed &nbsp;|&nbsp; <strong>Z</strong> - Asleep</div>
</div>
"""
# Find the existing legend and replace it.
pattern = re.compile(r'<div style="font-size: 11px; margin-bottom: 10px; background: #162444; padding: 10px; border: 1px solid #aaa; \ntext-align: center; white-space: nowrap; overflow-x: auto;"><strong>C</strong> - Coffee \| <strong>M</strong> - \nMedicine \| <strong>A</strong> - Alcohol \| <strong>E</strong> - Exercise \| <strong>B</strong> - Go to bed \| \n<strong>Z</strong> - Asleep</div>', re.DOTALL)
# wait, powershell output showed weird encoding issues. I will search for a simpler substring.
import bs4
soup = bs4.BeautifulSoup(html, "html.parser")
legend_div = soup.find("div", string=lambda s: s and "Coffee" in s and "Asleep" in s)
if legend_div:
    new_legend = bs4.BeautifulSoup(legend_html, "html.parser").div
    legend_div.replace_with(new_legend)
else:
    # Try finding it based on child strong tags
    strong = soup.find("strong", string="C")
    if strong:
        parent = strong.parent
        if "Coffee" in str(parent):
            new_legend = bs4.BeautifulSoup(legend_html, "html.parser").div
            parent.replace_with(new_legend)

# Add "TWO WEEK SLEEP DIARY" as a proper header. It's currently an h3 directly in #table-view
table_view = soup.find("div", id="table-view")
if table_view:
    table_view["class"] = table_view.get("class", []) + ["section-card"]
    
    h3 = table_view.find("h3", string="TWO WEEK SLEEP DIARY")
    if h3:
        header_div = soup.new_tag("div", attrs={"class": "section-header", "onclick": "this.parentElement.classList.toggle('collapsed')"})
        header_div.append(h3.extract())
        icon = soup.new_tag("span", attrs={"class": "collapse-icon"})
        icon.string = "▼"
        header_div.append(icon)
        
        # wrap the rest in section-content
        content_div = soup.new_tag("div", attrs={"class": "section-content"})
        for child in list(table_view.children):
            content_div.append(child)
            
        table_view.clear()
        table_view.append(header_div)
        table_view.append(content_div)


with open(filepath, "w", encoding="utf-8") as f:
    f.write(str(soup))
