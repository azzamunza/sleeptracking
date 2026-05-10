import re

filepath = "C:/Users/Aaron Munro/Documents/GitHub/sleeptracking/index.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Revert the messy variable movement
# 2. Move the Practitioner Init block to the bottom of the script
prac_block_pattern = re.compile(r'// Practitioner Mode Init.*?loadPractitionerData\(\);\s+\}', re.DOTALL)
prac_block_match = prac_block_pattern.search(html)
if prac_block_match:
    prac_block = prac_block_match.group(0)
    html = prac_block_pattern.sub('', html)
    
    # Insert before "Initial calls"
    html = html.replace('// Initial calls', prac_block + '\n\n    // Initial calls')

with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)
