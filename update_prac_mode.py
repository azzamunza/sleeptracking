import re

filepath = "C:/Users/Aaron Munro/Documents/GitHub/sleeptracking/index.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Rename "Navigation" to "Sleep Log Day Selector"
html = html.replace('<h3>Navigation</h3>', '<h3>Sleep Log Day Selector</h3>')

# 2. Move "Open Full Screen" button to TWO WEEK SLEEP DIARY header
# Remove it from My Data
html = html.replace('<button class="outline" id="full-screen-btn" onclick="openFullScreenTable()">Open Full Screen</button>', '')

# Add it to TWO WEEK SLEEP DIARY
old_header = '<div class="section-header" onclick="this.parentElement.classList.toggle(\'collapsed\')"><h3>TWO WEEK SLEEP DIARY</h3><span class="collapse-icon">▼</span></div>'
new_header = '<div class="section-header" onclick="this.parentElement.classList.toggle(\'collapsed\')"><h3>TWO WEEK SLEEP DIARY</h3><div style="display:flex; align-items:center; gap:10px;"><button class="outline" id="full-screen-btn" onclick="event.stopPropagation(); openFullScreenTable()" style="margin:0; padding: 5px 10px; font-size: 12px; background: transparent; color: var(--text); border: 1px solid var(--text);">Open Full Screen</button><span class="collapse-icon">▼</span></div></div>'
html = html.replace(old_header, new_header)

# 3. Practitioner Mode Button Activation & Defaults
practitioner_js = """
      isPractitionerMode = true;
      document.querySelectorAll('.read-only-text').forEach(el => el.style.display = '');
      
      // Leave cards visible, but Toggle button should still work
      document.getElementById('toggle-btn').disabled = false;
      document.getElementById('open-invite-btn').style.display = 'none';

      // Set defaults for practitioner
      showingTable = true;
      notesUnderneath = true;
      const notesBtn = document.getElementById('toggle-notes-loc-btn');
      if (notesBtn) notesBtn.textContent = "Notes Pos: ⬓";

      // Enable specific buttons for practitioner
      const toEnable = [
          'full-screen-btn', 
          'toggle-notes-loc-btn', 
          'generic-export-btn', 
          'export-csv', 
          'export-json'
      ];
      toEnable.forEach(id => {
          const el = document.getElementById(id);
          if (el) el.disabled = false;
      });
      // Also enable popup dialog buttons
      document.querySelectorAll('button[onclick="copyGenericModal()"], button[onclick="closeGenericModal()"]').forEach(el => el.disabled = false);

      loadPractitionerData();
"""
pattern = re.compile(r'isPractitionerMode = true;.*?\n      loadPractitionerData\(\);', re.DOTALL)
html = pattern.sub(practitioner_js.strip(), html)

# Also wait! toggleView() switches showingTable.
# We set showingTable = true here, but we also need to explicitly call `toggleView()` or set the styles to show the table if they start out showing Hourly view.
# Actually, `showingTable` is initialized at the top of the script:
# `let showingTable = !!new URLSearchParams(window.location.search).get('invite_id');`
# So showingTable is ALREADY true when page loads in Practitioner mode.
# We just need to make sure the app correctly starts in table view if `showingTable` is true.
# At the bottom of the script, `toggleView()` is NOT called on load. Wait, how is the table shown initially?
# The CSS has `#hourly-view` block, `#table-view` none by default.
# Let's add a check at the end of the script to apply `showingTable` state on load.

# 4. PDF Export Sizing - Override inline scaling
print_css_fix = """
      #table-container { height: auto !important; overflow: visible !important; }
      #table-container table { transform: none !important; width: 100% !important; }
"""
if "#table-container table { transform: none" not in html:
    html = html.replace('@media print {\n', '@media print {\n' + print_css_fix)


with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)
