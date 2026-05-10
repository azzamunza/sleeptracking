import sys
import re

file_path = r"C:\Users\Aaron Munro\Documents\GitHub\sleeptracking\index.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

print_regex = re.compile(r'    /\* Print Styles \*/.*?\}', re.DOTALL)
# It's tricky to replace safely if there's nested brackets.
# Let's just find the @media print { ... } block.
# Actually, the diff shows the old block was untouched. Let's fix it safely.

print_css_replacement = """    /* Print Styles */
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
    
# Manual replace
old_print_block = """    /* Print Styles */
    @media print {
      @page { size: landscape; margin: 10mm; }
      body { background: var(--card-bg); margin: 0; padding: 0; color: black; }
      #auth-section, .card:not(#table-view), button, input { display: none !important; }
      #app { display: block !important; }
      #table-view { display: block !important; box-shadow: none; border: none; padding: 0; margin: 0; }
      #table-view h3 { font-size: 18px; margin-bottom: 5px; }
      table { width: 100%; border-collapse: collapse; font-size: 10px; min-width: auto; }
      th, td { border: 1px solid black !important; padding: 4px; color: black; }
      th { background: #eee !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    }"""
html = html.replace(old_print_block, print_css_replacement)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
