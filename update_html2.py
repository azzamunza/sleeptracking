import re
from bs4 import BeautifulSoup

filepath = "C:/Users/Aaron Munro/Documents/GitHub/sleeptracking/index.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# Re-do My Data grid
toggle_btn = soup.find(id="toggle-btn")
if toggle_btn and "Toggle Table View" in toggle_btn.text:
    my_data_card = toggle_btn.find_parent("div", class_="card")
    if my_data_card and "my-data-grid" not in str(my_data_card):
        # Rebuild layout
        grid = soup.new_tag("div", attrs={"class": "my-data-grid"})
        col1 = soup.new_tag("div", attrs={"style": "display:flex; flex-direction:column; gap:5px;"})
        col2 = soup.new_tag("div", attrs={"style": "display:flex; flex-direction:column; gap:5px;"})
        col3 = soup.new_tag("div", attrs={"style": "display:flex; flex-direction:column; gap:5px;"})
        
        # Col 1
        toggle_view_btn = my_data_card.find("button", id="toggle-btn")
        if toggle_view_btn: col1.append(toggle_view_btn.extract())
        
        zoom_btn = soup.new_tag("button", attrs={"id": "toggle-zoom-btn", "class": "outline", "onclick": "toggleTableZoom()"})
        zoom_btn.string = "Zoom to Fit: Off"
        col1.append(zoom_btn)

        # Col 2
        toggle_notes_btn = my_data_card.find("button", id="toggle-notes-btn")
        if toggle_notes_btn: col2.append(toggle_notes_btn.extract())
        notes_loc_btn = soup.new_tag("button", attrs={"id": "toggle-notes-loc-btn", "class": "outline", "onclick": "toggleNotesLocation()"})
        notes_loc_btn.string = "Notes Layout: Side"
        col2.append(notes_loc_btn)
        
        # Col 3
        exp_csv = my_data_card.find("button", id="export-csv")
        exp_json = my_data_card.find("button", id="export-json")
        exp_pdf = my_data_card.find("button", id="export-pdf")
        
        if exp_csv:
            exp_csv["onclick"] = "openExportDialog('csv')"
            col3.append(exp_csv.extract())
        if exp_json:
            exp_json["onclick"] = "openExportDialog('json')"
            col3.append(exp_json.extract())
        if exp_pdf: col3.append(exp_pdf.extract())
        
        grid.append(col1)
        grid.append(col2)
        grid.append(col3)
        
        my_data_card.clear()
        my_data_card.append(grid)
        
        # Wrap section
        my_data_card["class"] = my_data_card.get("class", []) + ["section-card"]
        
        content_div = soup.new_tag("div", attrs={"class": "section-content"})
        for child in list(my_data_card.children):
            content_div.append(child)
            
        header_div = soup.new_tag("div", attrs={"class": "section-header", "onclick": "this.parentElement.classList.toggle('collapsed')"})
        h3 = soup.new_tag("h3")
        h3.string = "My Data"
        header_div.append(h3)
        
        icon = soup.new_tag("span", attrs={"class": "collapse-icon"})
        icon.string = "▼"
        header_div.append(icon)
        
        my_data_card.append(header_div)
        my_data_card.append(content_div)

# Fix Legend width wrapper issue
# The legend text lost its &nbsp; due to soup parsing
legend = soup.find("div", string=lambda s: s and "TWO WEEK SLEEP DIARY" in s)
if not legend:
    legend = soup.find("h3", string="TWO WEEK SLEEP DIARY")
if legend:
    legend_div = legend.find_next_sibling("div")
    if legend_div and "Coffee" in legend_div.text:
        # Re-set inner HTML manually
        legend_div.clear()
        legend_div.append(BeautifulSoup("<strong>C</strong> - Coffee &nbsp;|&nbsp; <strong>M</strong> - Medicine &nbsp;|&nbsp; <strong>A</strong> - Alcohol &nbsp;|&nbsp; <strong>E</strong> - Exercise &nbsp;|&nbsp; <strong>B</strong> - Go to bed &nbsp;|&nbsp; <strong>Z</strong> - Asleep", "html.parser"))

with open(filepath, "w", encoding="utf-8") as f:
    f.write(str(soup))
