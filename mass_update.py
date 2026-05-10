import sys
import re
from datetime import datetime

file_path = r"C:\Users\Aaron Munro\Documents\GitHub\sleeptracking\index.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# 2. Clear Cache Button
clear_cache_btn = """    <button id="login-btn">Sign in with Google</button>
    <button onclick="clearCache()" style="background: #e0e0e0; color: #333;">Clear Cache</button>"""
html = html.replace('    <button id="login-btn">Sign in with Google</button>', clear_cache_btn)

clear_cache_script = """    async function clearCache() {
      if ('caches' in window) {
        const names = await caches.keys();
        for (let name of names) { await caches.delete(name); }
        alert("Cache cleared!");
        window.location.reload(true);
      }
    }
    // --- Supabase Setup ---"""
html = html.replace("    // --- Supabase Setup ---", clear_cache_script)

# 3. Invite Practitioner Modal
invite_btn = """      <div>
        <button id="open-invite-btn" class="outline" onclick="openInviteModal()">Invite Practitioner</button>
        <button id="logout-btn" class="outline">Logout</button>
      </div>"""
html = html.replace('      <button id="logout-btn" class="outline">Logout</button>', invite_btn)

invite_modal = """  <!-- Invite Modal -->
  <div id="invite-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:1000; align-items:center; justify-content:center;">
    <div class="card" style="width: 90%; max-width: 500px; max-height: 90vh; overflow-y: auto;">
      <div class="flex-between" style="margin-bottom: 15px;">
        <h3>Invite Practitioner</h3>
        <button onclick="closeInviteModal()" style="background:transparent; color:#333; font-size:24px; padding:0; margin:0; line-height:1;">&times;</button>
      </div>
      <div style="display: flex; flex-direction: column; gap: 10px;">
         <input type="text" id="invite-name" placeholder="Practitioner Name" style="margin:0;">
         <button id="save-invite-btn" onclick="saveInvite()">Save</button>
         <select id="invite-list" style="padding: 8px; border: 1px solid var(--border); border-radius: 4px;" onchange="loadInvite()">
            <option value="">-- Select Invite --</option>
         </select>
         <button id="revoke-invite-btn" class="outline" onclick="revokeInvite()" disabled>Revoke Invite</button>
      </div>
      <div id="invite-link-display" style="margin-top: 10px; font-size: 12px; color: var(--primary); word-break: break-all;"></div>
    </div>
  </div>
  
  <div id="app">"""
html = html.replace('  <div id="app">', invite_modal)

# Remove old invite section
old_invite_section_regex = re.compile(r'<!-- Actions -->\s*<div class="card" id="invite-section">.*?</div>\s*<!-- Actions -->', re.DOTALL)
html = old_invite_section_regex.sub('<!-- Actions -->', html)

modal_functions = """    function openInviteModal() {
      document.getElementById('invite-modal').style.display = 'flex';
      loadInvites();
    }
    function closeInviteModal() {
      document.getElementById('invite-modal').style.display = 'none';
    }
"""
html = html.replace('    // --- Invite Management ---', '    // --- Invite Management ---\n' + modal_functions)


# 4. Move Navigation & Type of Day
nav_section_regex = re.compile(r'<!-- Navigation & Type of Day -->\s*<div class="card".*?</label>\s*<input type="text" id="type-of-day"[^>]*>\s*</div>', re.DOTALL)
nav_match = nav_section_regex.search(html)
if nav_match:
    nav_html = nav_match.group(0)
    html = html.replace(nav_html, '')
    # Insert before Hourly Log
    html = html.replace('<!-- Hourly Log View -->', f'<div id="nav-wrapper">\n{nav_html}\n</div>\n    <!-- Hourly Log View -->')

# 1. & 6. Key Legend updates
# Remove old Key Legend
old_legend_regex = re.compile(r'<!-- Key / Legend -->\s*<div class="card">.*?</div>', re.DOTALL)
html = old_legend_regex.sub('', html)

# Replace table legend
table_legend_regex = re.compile(r'<div style="display: grid; grid-template-columns: repeat\(6, 1fr\).*?</div>', re.DOTALL)
single_line_legend = '<div style="font-size: 11px; margin-bottom: 10px; background: #f9f9f9; padding: 8px; border: 1px solid #aaa; text-align: center;"><strong>C</strong> - Coffee &nbsp;|&nbsp; <strong>M</strong> - Medicine &nbsp;|&nbsp; <strong>A</strong> - Alcohol &nbsp;|&nbsp; <strong>E</strong> - Exercise &nbsp;|&nbsp; <strong>B</strong> - Go to bed &nbsp;|&nbsp; <strong>Z</strong> - Asleep</div>'
html = table_legend_regex.sub(single_line_legend, html)


# 7. Daily Summary
summary_html = """    <!-- Daily Summary -->
    <div class="card" id="daily-summary">
      <div class="flex-between" style="margin-bottom: 10px;">
        <button onclick="changeSummaryDay(-1)">&larr; Prev</button>
        <h3 id="summary-date-display" style="margin: 0; text-align: center; font-size: 16px;"></h3>
        <button onclick="changeSummaryDay(1)">Next &rarr;</button>
      </div>
      <div id="summary-content" style="font-size: 14px; white-space: pre-wrap; line-height: 1.5;"></div>
    </div>
"""
# Insert after Quick Entry
html = html.replace('<!-- Actions -->', summary_html + '\n    <!-- Actions -->')

# 8. & 9. Practitioner mode and Styles
# CSS for disabled buttons and toggles
css_additions = """
    button:disabled { background: #e0e0e0; color: #999; cursor: not-allowed; opacity: 1; border: none; }
    button.outline:disabled { background: transparent; border: 1px solid #ccc; color: #ccc; }
    
    .toggle-btn { 
      padding: 6px 10px; background: transparent; color: var(--primary); border: 1px solid var(--primary); border-radius: 4px; cursor: pointer; font-size: 12px; font-weight: bold;
    }
    .toggle-btn.active { background: var(--primary); color: white; }
    .toggle-btn:disabled { background: #f5f5f5; border: 1px solid #ddd; color: #aaa; }
"""
html = html.replace('    .toggle-btn { \n      padding: 6px 10px; background: #e0e0e0; color: #333; border: none; border-radius: 4px; cursor: pointer; font-size: 12px; font-weight: bold;\n    }\n    .toggle-btn.active { background: var(--primary); color: white; }', css_additions)


# Practitioner Mode Init JS fix
prac_init_old = """      // Hide all cards except the actions card and table view
      const cards = document.querySelectorAll('.card');
      cards.forEach(c => {
        if (!c.classList.contains('flex-between') || c.id === 'auth-section') {
           if (c.id !== 'table-view' && !c.querySelector('#export-csv')) {
              c.style.display = 'none';
           }
        }
      });
      
      document.getElementById('table-view').style.display = 'block';
      document.getElementById('toggle-btn').disabled = true;"""
      
prac_init_new = """      // Leave cards visible, but Toggle button should still work
      document.getElementById('toggle-btn').disabled = false;
      document.getElementById('open-invite-btn').style.display = 'none';"""
html = html.replace(prac_init_old, prac_init_new)


# Worded date format JS
date_format_js = """    function getWordedDate(dateStr, prefix = '') {
      const d = new Date(dateStr + 'T12:00:00');
      const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
      const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
      
      const dayName = days[d.getDay()];
      const dateNum = d.getDate();
      const monthName = months[d.getMonth()];
      const year = d.getFullYear();
      
      let suffix = 'th';
      if (dateNum === 1 || dateNum === 21 || dateNum === 31) suffix = 'st';
      else if (dateNum === 2 || dateNum === 22) suffix = 'nd';
      else if (dateNum === 3 || dateNum === 23) suffix = 'rd';
      
      return `${prefix}${dayName} ${dateNum}${suffix} ${monthName} ${year}`;
    }"""
html = html.replace("    function getDiaryDateStr(dateObj) {", date_format_js + "\n\n    function getDiaryDateStr(dateObj) {")


# Update updateHeader for dates
header_update_old = """    function updateHeader() {
      const info = formatDisplayDate(currentViewingDate);
      document.getElementById('current-date-display').textContent = info.date;
      document.getElementById('current-day-name').textContent = info.day;
      document.getElementById('type-of-day').value = todayData.type_of_day || '';
      
      // Update quick entry label
      const now = new Date();
      document.getElementById('current-hour-display').textContent = `Current: ${formatHourLabel(now.getHours())}`;
    }"""
header_update_new = """    let currentSummaryDate = currentViewingDate;
    function updateHeader() {
      document.getElementById('current-date-display').textContent = getWordedDate(currentViewingDate);
      const dayNameEl = document.getElementById('current-day-name');
      if(dayNameEl) dayNameEl.style.display = 'none';
      
      document.getElementById('type-of-day').value = todayData.type_of_day || '';
      
      const now = new Date();
      document.getElementById('current-hour-display').textContent = `Current: ${formatHourLabel(now.getHours())} - ${getWordedDate(getDiaryDateStr(now))}`;
    }"""
html = html.replace(header_update_old, header_update_new)


# Toggling Table View (hiding nav_wrapper)
toggle_old = """    function toggleView() {
      showingTable = !showingTable;
      document.getElementById('hourly-view').style.display = showingTable ? 'none' : 'block';
      document.getElementById('table-view').style.display = showingTable ? 'block' : 'none';
      if (showingTable) renderTable();
    }"""
toggle_new = """    function toggleView() {
      showingTable = !showingTable;
      document.getElementById('hourly-view').style.display = showingTable ? 'none' : 'block';
      document.getElementById('table-view').style.display = showingTable ? 'block' : 'none';
      const navWrapper = document.getElementById('nav-wrapper');
      if (navWrapper) navWrapper.style.display = showingTable ? 'none' : 'block';
      if (showingTable) renderTable();
    }"""
html = html.replace(toggle_old, toggle_new)


# Summary Logic
summary_logic = """
    function changeSummaryDay(offset) {
      const d = new Date(currentSummaryDate + 'T12:00:00');
      d.setDate(d.getDate() + offset);
      currentSummaryDate = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
      renderSummary();
    }

    function renderSummary() {
      document.getElementById('summary-date-display').textContent = getWordedDate(currentSummaryDate, 'The night of ');
      const contentEl = document.getElementById('summary-content');
      
      const row = allData.find(r => r.date_string === currentSummaryDate);
      if (!row || !row.hours || Object.keys(row.hours).length === 0) {
        contentEl.innerHTML = '<em>No data recorded for this night.</em>';
        return;
      }

      let html = '';
      const markerLabels = { 'C': 'C - Coffee, cola or tea', 'M': 'M - Medicine', 'A': 'A - Alcohol', 'E': 'E - Exercise', 'B': 'B - Go to bed', 'Z': 'Z - Asleep' };
      
      hourOrder.forEach(h => {
        const hData = row.hours[h];
        if (!hData || (hData.markers.length === 0 && !hData.note)) return;
        
        html += `<strong>${formatHourLabel(h)}</strong><br>`;
        if (hData.markers && hData.markers.length > 0) {
           hData.markers.forEach(m => {
             html += `${markerLabels[m]}<br>`;
           });
        }
        if (hData.note) {
           html += `Note: ${hData.note}<br>`;
        }
        html += `<br>`;
      });
      contentEl.innerHTML = html;
    }
"""
html = html.replace("    function renderTable() {", summary_logic + "\n    function renderTable() {")

# Render summary after fetchAllData
fetch_old = """      if (!error && data) {
        allData = data;
        renderTable();
      }"""
fetch_new = """      if (!error && data) {
        allData = data;
        renderTable();
        currentSummaryDate = currentViewingDate;
        renderSummary();
      }"""
html = html.replace(fetch_old, fetch_new)
prac_data_old = """      allData = data || [];
      allData.sort((a, b) => a.date_string.localeCompare(b.date_string));
      renderTable();"""
prac_data_new = """      allData = data || [];
      allData.sort((a, b) => a.date_string.localeCompare(b.date_string));
      renderTable();
      currentSummaryDate = currentViewingDate;
      renderSummary();"""
html = html.replace(prac_data_old, prac_data_new)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
