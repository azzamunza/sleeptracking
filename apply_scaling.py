import re

filepath = "C:/Users/Aaron Munro/Documents/GitHub/sleeptracking/index.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# Fix the button text
html = html.replace("Notes Pos: \"\"", "Notes Pos: ⬓")
html = html.replace("Notes Pos: -", "Notes Pos: ◨")

# Add the scaling implementation to the renderTable override (and the original renderTable via a wrapper if needed)
# Actually, the user asked to render the table in the same way the PDF scales it.
# We can just wrap the `table-container` in a div and apply scale to it when renderTable runs.
# Let's write a scale function and call it at the end of both table renders.

scale_js = """
    function scaleTableToFit() {
        const table = document.querySelector('#table-container table');
        const container = document.getElementById('table-container');
        if (table && container) {
            // reset transform first to measure true width
            table.style.transform = 'none';
            table.style.transformOrigin = 'top left';
            table.style.width = 'max-content'; // force it to take up as much space as it needs
            
            const tableWidth = table.offsetWidth;
            const containerWidth = container.parentElement.offsetWidth - 30; // padding approx
            
            if (tableWidth > containerWidth && containerWidth > 0) {
                const scale = containerWidth / tableWidth;
                table.style.transform = 'scale(' + scale + ')';
                container.style.height = (table.offsetHeight * scale) + 'px';
                container.style.overflow = 'hidden';
            } else {
                table.style.transform = 'none';
                table.style.width = '100%';
                container.style.height = 'auto';
            }
        }
    }
    
    // Add window resize listener
    window.addEventListener('resize', scaleTableToFit);
"""

html = html.replace('// Initial calls', scale_js + '\n    // Initial calls')

# Make sure scaleTableToFit is called after renderTable
html = html.replace('container.innerHTML = html;', 'container.innerHTML = html;\n        setTimeout(scaleTableToFit, 50);')
html = html.replace('origRenderTable();', 'origRenderTable();\n            setTimeout(scaleTableToFit, 50);')

with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)
