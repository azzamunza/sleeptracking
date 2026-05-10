import re

filepath = "C:/Users/Aaron Munro/Documents/GitHub/sleeptracking/index.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# Add initial view sync
init_js = """
    // Initial calls
    if (showingTable) {
        // Force the initial view sync without toggling the boolean
        document.getElementById('hourly-view').style.display = 'none';
        document.getElementById('table-view').style.display = 'block';
        const navWrapper = document.getElementById('nav-wrapper');
        if (navWrapper) navWrapper.style.display = 'none';
        setTimeout(renderTable, 50);
    }
    setTimeout(updateQuickEntryHeader, 500);
"""

html = html.replace('// Initial calls\n    setTimeout(updateQuickEntryHeader, 500);', init_js.strip())

with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)
