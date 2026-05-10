import re

filepath = "C:/Users/Aaron Munro/Documents/GitHub/sleeptracking/index.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# Fix potential broken unicode characters from previous edits
# U+25BC is ▼ (Down pointing triangle)
# U+2715 is ✕ (Multiplication X) - usually used for close
# But user mentioned "x" corner close button. The modal uses × (U+00D7)
html = html.replace('-', '▼')

# Double check the notesUnderneath initialization. 
# It should be initialized with 'let' and accessible.
if 'let notesUnderneath = true;' not in html and 'let notesUnderneath = false;' not in html:
    # If it's missing or different, ensure it's there
    html = html.replace('let showingTable =', 'let notesUnderneath = false;\n    let showingTable =')

# The user wants Practitioner mode to DEFAULT to Diary mode and Notes below table.
# Diary mode = showingTable = true
# Notes below table = notesUnderneath = true

# Re-verify the PDF print styles
print_styles = """
    @media print {
      #table-container { height: auto !important; overflow: visible !important; }
      #table-container table { transform: none !important; width: 100% !important; margin: 0 !important; }
      #table-view .section-header { display: block !important; }
      #table-view .collapse-icon { display: none !important; }
      #table-view .section-content { display: block !important; border: none !important; }
      .section-card.collapsed .section-content { display: block !important; }
      body { background: white !important; color: black !important; }
      .card { border: none !important; box-shadow: none !important; }
      /* Hide navigation and buttons when printing */
      #nav-wrapper, #quick-entry-btns, #toggle-btn, #toggle-notes-btn, #toggle-notes-loc-btn, #export-csv, #export-json, #export-pdf, #full-screen-btn, #logout-btn, #open-invite-btn {
        display: none !important;
      }
    }
"""

# Find the existing @media print block and replace it for a clean version
pattern = re.compile(r'@media print \{.*?\}', re.DOTALL)
html = pattern.sub(print_styles.strip(), html)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)
