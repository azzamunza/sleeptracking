import sys

file_path = r"C:\Users\Aaron Munro\Documents\GitHub\sleeptracking\index.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add span for practitioner name in the header
old_header = """    <div class="card flex-between">
      <span id="user-email"></span>
      <div>
        <button id="open-invite-btn" class="outline" onclick="openInviteModal()">Invite Practitioner</button>
        <button id="logout-btn" class="outline">Logout</button>
      </div>
    </div>"""

new_header = """    <div class="card flex-between">
      <span id="user-email"></span>
      <div style="display: flex; align-items: center; gap: 10px;">
        <span id="practitioner-name-display" style="display:none; font-weight: bold; color: var(--primary);"></span>
        <button id="open-invite-btn" class="outline" onclick="openInviteModal()">Invite Practitioner</button>
        <button id="logout-btn" class="outline">Logout</button>
      </div>
    </div>"""

html = html.replace(old_header, new_header)

# 2. Fetch and display practitioner name
old_prac_data = """    async function loadPractitionerData() {
      const { data, error } = await supabaseClient.rpc('get_practitioner_data', { p_invite_id: practitionerInviteId });"""

new_prac_data = """    async function loadPractitionerData() {
      // Fetch the practitioner name
      const { data: nameData } = await supabaseClient.rpc('get_practitioner_name', { p_invite_id: practitionerInviteId });
      if (nameData) {
        document.getElementById('practitioner-name-display').textContent = nameData;
        document.getElementById('practitioner-name-display').style.display = 'inline';
      }

      const { data, error } = await supabaseClient.rpc('get_practitioner_data', { p_invite_id: practitionerInviteId });"""

html = html.replace(old_prac_data, new_prac_data)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
