import sys

file_path = r"C:\Users\Aaron Munro\Documents\GitHub\sleeptracking\index.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add IDs to summary buttons
summary_old = """      <div class="flex-between" style="margin-bottom: 10px;">
        <button onclick="changeSummaryDay(-1)">&larr; Prev</button>
        <h3 id="summary-date-display" style="margin: 0; text-align: center; font-size: 16px;"></h3>
        <button onclick="changeSummaryDay(1)">Next &rarr;</button>
      </div>"""
summary_new = """      <div class="flex-between" style="margin-bottom: 10px;">
        <button id="prev-summary-btn" onclick="changeSummaryDay(-1)">&larr; Prev</button>
        <h3 id="summary-date-display" style="margin: 0; text-align: center; font-size: 16px;"></h3>
        <button id="next-summary-btn" onclick="changeSummaryDay(1)">Next &rarr;</button>
      </div>"""
html = html.replace(summary_old, summary_new)

# 2. Exclude navigation buttons from being disabled
qsa_old = "const allInputs = document.querySelectorAll('input, button:not(#toggle-btn):not(#export-csv):not(#export-json):not(#export-pdf)');"
qsa_new = "const allInputs = document.querySelectorAll('input, button:not(#toggle-btn):not(#export-csv):not(#export-json):not(#export-pdf):not(#prev-day-btn):not(#next-day-btn):not(#prev-summary-btn):not(#next-summary-btn)');"
html = html.replace(qsa_old, qsa_new)

# 3. Patch loadDayData for practitioner mode
load_day_old = """    async function loadDayData(dateStr) {
      todayData = { hours: {}, type_of_day: "" };
      updateHeader();
      renderHours(); // reset UI immediately

      if (!currentUser) return;
      const { data, error } = await supabaseClient"""
load_day_new = """    async function loadDayData(dateStr) {
      todayData = { hours: {}, type_of_day: "" };
      
      if (isPractitionerMode) {
        const row = allData.find(r => r.date_string === dateStr);
        if (row) todayData = { hours: row.hours || {}, type_of_day: row.type_of_day || "" };
        updateHeader();
        renderHours();
        return;
      }
      
      updateHeader();
      renderHours(); // reset UI immediately

      if (!currentUser) return;
      const { data, error } = await supabaseClient"""
html = html.replace(load_day_old, load_day_new)

# 4. Patch loadPractitionerData to initialize the day view
prac_data_old = """      allData.sort((a, b) => a.date_string.localeCompare(b.date_string));
      renderTable();
      currentSummaryDate = currentViewingDate;
      renderSummary();"""
prac_data_new = """      allData.sort((a, b) => a.date_string.localeCompare(b.date_string));
      loadDayData(currentViewingDate);
      renderTable();
      currentSummaryDate = currentViewingDate;
      renderSummary();"""
html = html.replace(prac_data_old, prac_data_new)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
