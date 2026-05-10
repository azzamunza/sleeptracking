const window = { location: { origin: '', pathname: '', search: '' }, supabase: { createClient: () => ({ auth: { onAuthStateChange: (cb) => { global.authCb = cb; }, signInWithOAuth: () => {}, signOut: () => {} }, rpc: () => ({}), from: () => ({ select: () => ({ eq: () => ({ order: () => ({}), maybeSingle: () => ({}) }) }) }) }) }, URL: { createObjectURL: () => {} }, print: () => {} }; document = { getElementById: () => ({ style: {}, classList: { contains: () => false }, querySelector: () => null }), querySelectorAll: () => [], createElement: () => ({ style: {}, classList: { add: () => {}, remove: () => {} } }) }; navigator = { serviceWorker: { register: () => Promise.resolve() } }; alert = () => {}; const Blob = function() {}; 

    async function clearCache() {
      if ('caches' in window) {
        const names = await caches.keys();
        for (let name of names) { await caches.delete(name); }
        alert("Cache cleared!");
        window.location.reload(true);
      }
    }
    // --- Supabase Setup ---
    const SUPABASE_URL = "https://nrwckhyegdkcbfbiitxz.supabase.co";
    const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5yd2NraHllZ2RrY2JmYmlpdHh6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzIxMzYxMzcsImV4cCI6MjA4NzcxMjEzN30.j_4uCVEG2CoNv9n8tGJaPwZNqSuEqZUZUxxVLdGZcEo";
    
    const supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
      auth: { flowType: 'pkce', detectSessionInUrl: true, persistSession: true }
    });

    let currentUser = null;
    let currentViewingDate = getDiaryDateStr(new Date()); 
    let todayData = { hours: {}, type_of_day: "" };

    let saveTimeout = null;
    let allData = []; // Cache for table view/export
    let isPractitionerMode = false;
    let practitionerInviteId = new URLSearchParams(window.location.search).get('invite_id');
    let showingTable = !!new URLSearchParams(window.location.search).get('invite_id');



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
      const allInputs = document.querySelectorAll('input, button:not(#toggle-btn):not(#export-csv):not(#export-json):not(#export-pdf):not(#prev-day-btn):not(#next-day-btn):not(#prev-summary-btn):not(#next-summary-btn)');
      allInputs.forEach(el => el.disabled = true);
      
      isPractitionerMode = true;
      document.querySelectorAll('.read-only-text').forEach(el => el.style.display = '');
      
      // Leave cards visible, but Toggle button should still work
      document.getElementById('toggle-btn').disabled = false;
      document.getElementById('open-invite-btn').style.display = 'none';

      loadPractitionerData();
    }

    async function loadPractitionerData() {
      // Fetch the practitioner name
      const { data: nameData } = await supabaseClient.rpc('get_practitioner_name', { p_invite_id: practitionerInviteId });
      if (nameData) {
        document.getElementById('practitioner-name-display').textContent = nameData;
        document.getElementById('practitioner-name-display').style.display = 'inline';
      }

      const { data, error } = await supabaseClient.rpc('get_practitioner_data', { p_invite_id: practitionerInviteId });
      if (error) {
        alert("Invalid or expired invite.");
        return;
      }
      allData = data || [];
      allData.sort((a, b) => a.date_string.localeCompare(b.date_string));
      loadDayData(currentViewingDate);
      renderTable();
      currentSummaryDate = currentViewingDate;
      renderSummary();
    }


    // --- Helpers ---
    // A diary day spans from 12:00 PM (Noon) to 11:59 AM the next day.
    function getWordedDate(dateStr, prefix = '') {
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
    }

    function getDiaryDateStr(dateObj) {
      const d = new Date(dateObj);
      if (d.getHours() < 12) {
        d.setDate(d.getDate() - 1); // Belongs to previous day's diary entry
      }
      return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
    }

    function formatDisplayDate(dateStr) {
      const d = new Date(dateStr + 'T12:00:00'); // set to noon to avoid timezone shift
      const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
      return { 
        date: dateStr, 
        day: days[d.getDay()] 
      };
    }

    const hourOrder = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11];
    function formatHourLabel(h) {
      if (h === 0) return 'Midnight';
      if (h === 12) return 'Noon';
      return h < 12 ? `${h} AM` : `${h === 12 ? 12 : h - 12} PM`;
    }

    // --- Auth Logic ---

    supabaseClient.auth.onAuthStateChange((event, session) => {
      if (isPractitionerMode) return;

      if (session) {
        currentUser = session.user;
        document.getElementById('auth-section').style.display = 'none';
        document.getElementById('app').style.display = 'block';
        document.getElementById('user-email').textContent = session.user.email;
        
        // Load data on initial session or sign in

        if (event === 'INITIAL_SESSION' || event === 'SIGNED_IN') {
          loadDayData(currentViewingDate);
          fetchAllData(); // for table/export
          loadInvites();
        }

        
        // Clear any auth tokens from the URL for a cleaner address bar
        if (event === 'SIGNED_IN' && new URLSearchParams(window.location.search).has('code')) {
          history.replaceState({}, document.title, window.location.pathname);
        }
      } else {
        currentUser = null;
        document.getElementById('auth-section').style.display = 'block';
        document.getElementById('app').style.display = 'none';
      }
    });

    document.getElementById('login-btn').onclick = async () => {
      // Use origin + pathname to avoid appending queries or hashes to the redirect
      const redirectUrl = window.location.origin + window.location.pathname;
      const { error } = await supabaseClient.auth.signInWithOAuth({ 
        provider: 'google', 
        options: { redirectTo: redirectUrl } 
      });
      if (error) alert("Login error: " + error.message);
    };
    
    document.getElementById('logout-btn').onclick = async () => {
      await supabaseClient.auth.signOut();
    };

    // --- UI Logic ---
    function renderHours() {
      const container = document.getElementById('hours-container');
      container.innerHTML = '';
      
      const markers = ['C', 'M', 'A', 'E', 'B', 'Z'];
      const markerLabels = {
        'C': 'Coffee (C)',
        'M': 'Meds (M)',
        'A': 'Alcohol (A)',
        'E': 'Exercise (E)',
        'B': 'Bed (B)',
        'Z': 'Asleep (Z)'
      };

      hourOrder.forEach(h => {
        const row = document.createElement('div');
        row.className = 'hour-row';
        
        const topRow = document.createElement('div');
        topRow.style.display = 'flex';
        topRow.style.alignItems = 'center';
        topRow.style.gap = '10px';
        
        const label = document.createElement('div');
        label.className = 'hour-header';
        label.textContent = formatHourLabel(h);
        
        const toggles = document.createElement('div');
        toggles.className = 'toggles';
        
        const hourData = todayData.hours[h] || { markers: [], note: '' };
        
        markers.forEach(m => {
          const btn = document.createElement('button');
          btn.className = 'toggle-btn' + (hourData.markers.includes(m) ? ' active' : '');
          btn.textContent = markerLabels[m];
          btn.onclick = () => toggleMarker(h, m, btn);
          if (isPractitionerMode) btn.disabled = true;
          toggles.appendChild(btn);
        });

        const noteInput = document.createElement('input');
        noteInput.type = 'text';
        noteInput.placeholder = 'Add note...';
        noteInput.value = hourData.note || '';
        noteInput.style.margin = '0';
        noteInput.style.flexGrow = '1';
        noteInput.oninput = (e) => updateNote(h, e.target.value);
        if (isPractitionerMode) noteInput.disabled = true;

        topRow.appendChild(label);
        topRow.appendChild(toggles);
        
        row.appendChild(topRow);
        row.appendChild(noteInput);
        
        container.appendChild(row);
      });
    }

    let currentSummaryDate = currentViewingDate;
    function updateHeader() {
      document.getElementById('current-date-display').textContent = getWordedDate(currentViewingDate);
      const dayNameEl = document.getElementById('current-day-name');
      if(dayNameEl) dayNameEl.style.display = 'none';
      
      document.getElementById('type-of-day').value = todayData.type_of_day || '';
      
      const now = new Date();
      document.getElementById('current-hour-display').textContent = `Current: ${formatHourLabel(now.getHours())} - ${getWordedDate(getDiaryDateStr(now))}`;
    }

    document.getElementById('prev-day-btn').onclick = () => { changeDay(-1); };
    document.getElementById('next-day-btn').onclick = () => { changeDay(1); };
    
    document.getElementById('type-of-day').oninput = (e) => {
      todayData.type_of_day = e.target.value;
      scheduleSave();
    };

    function changeDay(offset) {
      const d = new Date(currentViewingDate + 'T12:00:00');
      d.setDate(d.getDate() + offset);
      currentViewingDate = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
      loadDayData(currentViewingDate);
    }

    // --- Data Management ---
    async function loadDayData(dateStr) {
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
      const { data, error } = await supabaseClient
        .from('sleep_days')
        .select('*')
        .eq('user_id', currentUser.id)
        .eq('date_string', dateStr)
        .maybeSingle();
      
      if (data) {
        todayData = { hours: data.hours || {}, type_of_day: data.type_of_day || "" };
      }
      updateHeader();
      renderHours();
    }


    function scheduleSave() {
      if (isPractitionerMode) return;
      if (saveTimeout) clearTimeout(saveTimeout);
      saveTimeout = setTimeout(saveData, 1000);
    }


    async function saveData() {
      if (!currentUser) return;
      const payload = {
        user_id: currentUser.id,
        date_string: currentViewingDate,
        type_of_day: todayData.type_of_day,
        hours: todayData.hours
      };
      
      const { error } = await supabaseClient
        .from('sleep_days')
        .upsert(payload, { onConflict: 'user_id,date_string' });
        
      if (error) console.error("Error saving:", error);
      else fetchAllData(); // refresh cache in background
    }


    function toggleMarker(hour, marker, btnElement) {
      if (isPractitionerMode) return;

      if (!todayData.hours[hour]) todayData.hours[hour] = { markers: [], note: '' };
      const arr = todayData.hours[hour].markers;
      const idx = arr.indexOf(marker);
      
      if (idx > -1) {
        arr.splice(idx, 1);
        btnElement.classList.remove('active');
      } else {
        arr.push(marker);
        btnElement.classList.add('active');
      }
      scheduleSave();
    }


    function updateNote(hour, text) {
      if (isPractitionerMode) return;

      if (!todayData.hours[hour]) todayData.hours[hour] = { markers: [], note: '' };
      todayData.hours[hour].note = text;
      scheduleSave();
    }

    function quickLog(marker) {
      const now = new Date();
      const currentHour = now.getHours();
      const targetDiaryDate = getDiaryDateStr(now);
      
      if (targetDiaryDate !== currentViewingDate) {
        // Switch to the correct day before logging
        currentViewingDate = targetDiaryDate;
        loadDayData(currentViewingDate).then(() => {
          doQuickLog(currentHour, marker);
        });
      } else {
        doQuickLog(currentHour, marker);
      }
    }

    function doQuickLog(hour, marker) {
      if (!todayData.hours[hour]) todayData.hours[hour] = { markers: [], note: '' };
      if (!todayData.hours[hour].markers.includes(marker)) {
        todayData.hours[hour].markers.push(marker);
        scheduleSave();
        renderHours(); // re-render to show active toggle
      }
      alert(`Logged ${marker} for ${formatHourLabel(hour)}`);
    }

    // --- Table & Export ---
    async function fetchAllData() {
      if (!currentUser) return;
      const { data, error } = await supabaseClient
        .from('sleep_days')
        .select('*')
        .eq('user_id', currentUser.id)
        .order('date_string', { ascending: true });
      if (!error && data) {
        allData = data;
        renderTable();
        currentSummaryDate = currentViewingDate;
        renderSummary();
      }
    }

    function toggleView() {
      showingTable = !showingTable;
      document.getElementById('hourly-view').style.display = showingTable ? 'none' : 'block';
      document.getElementById('table-view').style.display = showingTable ? 'block' : 'none';
      const navWrapper = document.getElementById('nav-wrapper');
      if (navWrapper) navWrapper.style.display = showingTable ? 'none' : 'block';
      if (showingTable) renderTable();
    }


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

    function renderTable() {
      const container = document.getElementById('table-container');
      let html = `<table>
        <thead>
          <tr>
            <th class="table-date">Date</th>
            <th>Day</th>
            <th class="table-type">Type of day</th>`;
      hourOrder.forEach(h => {
        html += `<th>${formatHourLabel(h)}</th>`;
      });
      html += `<th>Notes</th></tr></thead><tbody>`;

      allData.forEach(row => {
        const info = formatDisplayDate(row.date_string);
        html += `<tr>
          <td class="table-date">${info.date}</td>
            <td>${info.day}</td>
            <td class="table-type">${row.type_of_day || ''}</td>`;
          
        let dayNotes = [];
        const hours = row.hours || {};
        
        hourOrder.forEach(h => {
          const hData = hours[h];
          const marks = hData && hData.markers ? hData.markers.join(',') : '';
          if (hData && hData.note) {
            dayNotes.push(`${formatHourLabel(h)}:
${hData.note}`);
          }
          html += `<td>${marks}</td>`;
        });
        
        html += `<td class="table-notes">${dayNotes.join('\n\n')}</td></tr>`;
      });
      html += `</tbody></table>`;
      container.innerHTML = html;
    }

    function exportCSV() {
      let csv = "Date,Day,Type of Day,";
      hourOrder.forEach(h => { csv += `"${formatHourLabel(h)}",`; });
      csv += "Notes\n";

      allData.forEach(row => {
        const info = formatDisplayDate(row.date_string);
        let rowStr = `"${info.date}","${info.day}","${row.type_of_day || ''}",`;
        let dayNotes = [];
        
        hourOrder.forEach(h => {
          const hData = (row.hours || {})[h];
          rowStr += `"${(hData && hData.markers) ? hData.markers.join(' ') : ''}",`;
          if (hData && hData.note) {
            dayNotes.push(`${formatHourLabel(h)}:
${hData.note}`);
          }
        });
        rowStr += `"${dayNotes.join('\n\n')}"\n`;
        csv += rowStr;
      });

      const blob = new Blob([csv], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'sleep_data.csv';
      a.click();
    }

    function exportJSON() {
      const blob = new Blob([JSON.stringify(allData, null, 2)], { type: 'application/json' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'sleep_data.json';
      a.click();
    }

    function printPDF() {
      const wasTableHidden = !showingTable;
      if (wasTableHidden) {
        toggleView(); // temporarily render table
      }
      window.print();
      if (wasTableHidden) {
        toggleView(); // restore original view
      }
    }

    // --- Invite Management ---
    function openInviteModal() {
      document.getElementById('invite-modal').style.display = 'flex';
      loadInvites();
    }
    function closeInviteModal() {
      document.getElementById('invite-modal').style.display = 'none';
    }

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
  


try {
  global.authCb('SIGNED_IN', { user: { email: 'test@test.com' } });
  console.log('SUCCESS');
} catch (e) {
  console.error('RUNTIME ERROR:', e);
}
