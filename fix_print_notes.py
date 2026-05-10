import re

filepath = "C:/Users/Aaron Munro/Documents/GitHub/sleeptracking/index.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# Fix the print styles to ensure notes are visible
# Specifically, allow .card inside #table-view to be visible, or just allow #table-notes-bottom
print_fix = """
      #table-view .card { display: block !important; border: 1px solid black !important; background: white !important; color: black !important; }
      #table-notes-bottom { display: block !important; }
"""

# We also need to make sure that if notes are toggled OFF (showingNotes = false), 
# the print style doesn't force them back on. 
# But the JS handles display: none/block for #table-notes-bottom based on showingNotes.
# However, CSS !important would override the inline style.
# So we should use a selector that respects the inline display.

better_print_fix = """
      #table-view .card { border: 1px solid black !important; background: white !important; color: black !important; }
      /* Ensure the notes container is visible if it doesn't have display: none inline */
      #table-notes-bottom:not([style*="display: none"]) { display: block !important; }
"""

# Replace the restrictive card selector
html = html.replace('.card:not(#table-view)', '.card:not(#table-view):not(.section-content .card)')

# Or simpler:
html = html.replace('#auth-section, .card:not(#table-view), button, input, img { display: none !important; }', 
                    '#auth-section, .card:not(#table-view):not(#table-notes-bottom .card), button, input, img { display: none !important; }')

# And add the specific visibility for notes
if '#table-notes-bottom' not in html[html.find('@media print'):]:
    html = html.replace('@media print {\n', '@media print {\n' + better_print_fix)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)
