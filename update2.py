import sys
import re

file_path = r"C:\Users\Aaron Munro\Documents\GitHub\sleeptracking\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# Add sorting to loadPractitionerData
load_data_old = """    async function loadPractitionerData() {
      const { data, error } = await supabaseClient.rpc('get_practitioner_data', { p_invite_id: practitionerInviteId });
      if (error) {
        alert("Invalid or expired invite.");
        return;
      }
      allData = data || [];
      renderTable();
    }"""
    
load_data_new = """    async function loadPractitionerData() {
      const { data, error } = await supabaseClient.rpc('get_practitioner_data', { p_invite_id: practitionerInviteId });
      if (error) {
        alert("Invalid or expired invite.");
        return;
      }
      allData = data || [];
      allData.sort((a, b) => a.date_string.localeCompare(b.date_string));
      renderTable();
    }"""
html = html.replace(load_data_old, load_data_new)

# Add card hiding logic
init_old = """      // Hide invite section
      document.getElementById('invite-section').style.display = 'none';
      
      isPractitionerMode = true;
      showingTable = true;
      document.getElementById('hourly-view').style.display = 'none';
      document.getElementById('table-view').style.display = 'block';"""
      
init_new = """      isPractitionerMode = true;
      showingTable = true;
      
      // Hide all cards except the actions card and table view
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
html = html.replace(init_old, init_new)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
