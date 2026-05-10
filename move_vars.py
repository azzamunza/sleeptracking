import re

filepath = "C:/Users/Aaron Munro/Documents/GitHub/sleeptracking/index.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# Move state variables to the top of the script block
script_start = html.find('<script>') + 8
state_vars = """
    let currentUser = null;
    let currentViewingDate = getDiaryDateStr(new Date()); 
    let todayData = { hours: {}, type_of_day: "" };
    let saveTimeout = null;
    let allData = []; 
    let isPractitionerMode = false;
    let practitionerInviteId = new URLSearchParams(window.location.search).get('invite_id');
    let showingTable = !!practitionerInviteId;
    let showingNotes = true;
    let notesUnderneath = false;
"""

# Remove old declarations
html = re.sub(r'let currentUser = null;.*?let notesUnderneath = false;', '', html, flags=re.DOTALL)

# Insert at top
html = html[:script_start] + state_vars + html[script_start:]

with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)
