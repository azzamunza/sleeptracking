import sys
import re

file_path = r"C:\Users\Aaron Munro\Documents\GitHub\sleeptracking\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

invite_ui = """
    <!-- Actions -->
    <div class="card" id="invite-section">
      <h3>Invite Practitioner</h3>
      <div class="flex-between">
         <input type="text" id="invite-name" placeholder="Practitioner Name" style="width: 35%; margin-bottom: 0;">
         <button id="save-invite-btn" onclick="saveInvite()">Save</button>
         <select id="invite-list" style="width: 30%; padding: 8px; border: 1px solid var(--border); border-radius: 4px;" onchange="loadInvite()">
            <option value="">-- Select Invite --</option>
         </select>
         <button id="revoke-invite-btn" class="outline" onclick="revokeInvite()" disabled>Revoke Invite</button>
      </div>
      <div id="invite-link-display" style="margin-top: 10px; font-size: 12px; color: var(--primary); word-break: break-all;"></div>
    </div>
"""
html = html.replace("    <!-- Actions -->", invite_ui + "    <!-- Actions -->")

invite_vars = """
    let saveTimeout = null;
    let allData = []; // Cache for table view/export
    let isPractitionerMode = false;
    let practitionerInviteId = new URLSearchParams(window.location.search).get('invite_id');
"""
html = html.replace("    let saveTimeout = null;\n    let allData = []; // Cache for table view/export", invite_vars)

init_logic = """
    // PWA Service Worker
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('sw.js').catch(console.error);
    }

    // Practitioner Mode Init
    if (practitionerInviteId) {
      document.getElementById('auth-section').style.display = 'none';
      document.getElementById('app').style.display = 'block';
      
      document.getElementById('user-email').textContent = 'Practitioner Mode';
      document.getElementById('logout-btn').style.display = 'none';
      
      // Disable edit controls
      const allInputs = document.querySelectorAll('input, button:not(#toggle-btn):not(#export-csv):not(#export-json):not(#export-pdf)');
      allInputs.forEach(el => el.disabled = true);
      
      // Hide invite section
      document.getElementById('invite-section').style.display = 'none';
      
      isPractitionerMode = true;
      showingTable = true;
      document.getElementById('hourly-view').style.display = 'none';
      document.getElementById('table-view').style.display = 'block';

      loadPractitionerData();
    }

    async function loadPractitionerData() {
      const { data, error } = await supabaseClient.rpc('get_practitioner_data', { p_invite_id: practitionerInviteId });
      if (error) {
        alert("Invalid or expired invite.");
        return;
      }
      allData = data || [];
      renderTable();
    }
"""
html = html.replace("    // PWA Service Worker\n    if ('serviceWorker' in navigator) {\n      navigator.serviceWorker.register('sw.js').catch(console.error);\n    }", init_logic)

auth_logic = """
    supabaseClient.auth.onAuthStateChange((event, session) => {
      if (isPractitionerMode) return;
"""
html = html.replace("    supabaseClient.auth.onAuthStateChange((event, session) => {", auth_logic)

auth_logic_inject = """
        if (event === 'INITIAL_SESSION' || event === 'SIGNED_IN') {
          loadDayData(currentViewingDate);
          fetchAllData(); // for table/export
          loadInvites();
        }
"""
html = html.replace("        if (event === 'INITIAL_SESSION' || event === 'SIGNED_IN') {\n          loadDayData(currentViewingDate);\n          fetchAllData(); // for table/export\n        }", auth_logic_inject)

export_btn_ids = """
    <!-- Actions -->
    <div class="card flex-between">
      <button id="toggle-btn" onclick="toggleView()">Toggle Table View</button>
      <div>
        <button id="export-csv" onclick="exportCSV()" class="outline">Export CSV</button>
        <button id="export-json" onclick="exportJSON()" class="outline">Export JSON</button>
        <button id="export-pdf" onclick="printPDF()" class="outline">Export PDF</button>
      </div>
    </div>
"""
html = html.replace("""    <!-- Actions -->
    <div class="card flex-between">
      <button onclick="toggleView()">Toggle Table View</button>
      <div>
        <button onclick="exportCSV()" class="outline">Export CSV</button>
        <button onclick="exportJSON()" class="outline">Export JSON</button>
        <button onclick="printPDF()" class="outline">Export PDF</button>
      </div>
    </div>""", export_btn_ids)

schedule_save_override = """
    function scheduleSave() {
      if (isPractitionerMode) return;
      if (saveTimeout) clearTimeout(saveTimeout);
      saveTimeout = setTimeout(saveData, 1000);
    }
"""
html = html.replace("    function scheduleSave() {\n      if (saveTimeout) clearTimeout(saveTimeout);\n      saveTimeout = setTimeout(saveData, 1000);\n    }", schedule_save_override)

toggle_override = """
    function toggleMarker(hour, marker, btnElement) {
      if (isPractitionerMode) return;
"""
html = html.replace("    function toggleMarker(hour, marker, btnElement) {", toggle_override)

note_override = """
    function updateNote(hour, text) {
      if (isPractitionerMode) return;
"""
html = html.replace("    function updateNote(hour, text) {", note_override)

invite_funcs = """
    // --- Invite Management ---
    async function loadInvites() {
      if (!currentUser) return;
      const { data, error } = await supabaseClient.from('invites').select('*').order('created_at', { ascending: false });
      if (!error && data) {
        const select = document.getElementById('invite-list');
        select.innerHTML = '<option value="">-- Select Invite --</option>';
        data.forEach(inv => {
          const opt = document.createElement('option');
          opt.value = inv.id;
          opt.textContent = inv.practitioner_name;
          select.appendChild(opt);
        });
      }
    }

    async function saveInvite() {
      if (!currentUser) return;
      const name = document.getElementById('invite-name').value.trim();
      if (!name) { alert("Enter a name"); return; }
      
      const { data, error } = await supabaseClient.from('invites').insert({
        user_id: currentUser.id,
        practitioner_name: name
      }).select().single();
      
      if (error) {
        alert("Error saving invite: " + error.message);
      } else {
        const url = window.location.origin + window.location.pathname + '?invite_id=' + data.id;
        document.getElementById('invite-link-display').textContent = url;
        loadInvites();
      }
    }

    function loadInvite() {
      const select = document.getElementById('invite-list');
      const selectedId = select.value;
      const revokeBtn = document.getElementById('revoke-invite-btn');
      const linkDisplay = document.getElementById('invite-link-display');
      
      if (selectedId) {
        document.getElementById('invite-name').value = select.options[select.selectedIndex].text;
        revokeBtn.disabled = false;
        linkDisplay.textContent = window.location.origin + window.location.pathname + '?invite_id=' + selectedId;
      } else {
        document.getElementById('invite-name').value = '';
        revokeBtn.disabled = true;
        linkDisplay.textContent = '';
      }
    }

    async function revokeInvite() {
      const select = document.getElementById('invite-list');
      const selectedId = select.value;
      if (!selectedId) return;
      
      const { error } = await supabaseClient.from('invites').delete().eq('id', selectedId);
      if (error) {
        alert("Error revoking invite: " + error.message);
      } else {
        document.getElementById('invite-name').value = '';
        document.getElementById('revoke-invite-btn').disabled = true;
        document.getElementById('invite-link-display').textContent = '';
        loadInvites();
      }
    }
"""
html = html.replace("  </script>\n</body>", invite_funcs + "  </script>\n</body>")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
