const { getWordedDate, getDiaryDateStr } = require('./test_syntax.js'); // wait, let's just copy the helpers

const code = `
    function getWordedDate(dateStr, prefix = '') {
      const d = new Date(dateStr + 'T12:00:00');
      const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
      const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 
'October', 'November', 'December'];
      
      const dayName = days[d.getDay()];
      const dateNum = d.getDate();
      const monthName = months[d.getMonth()];
      const year = d.getFullYear();
      
      let suffix = 'th';
      if (dateNum === 1 || dateNum === 21 || dateNum === 31) suffix = 'st';
      else if (dateNum === 2 || dateNum === 22) suffix = 'nd';
      else if (dateNum === 3 || dateNum === 23) suffix = 'rd';
      
      return \`\${prefix}\${dayName} \${dateNum}\${suffix} \${monthName} \${year}\`;
    }

    function getDiaryDateStr(dateObj) {
      const d = new Date(dateObj);
      if (d.getHours() < 12) {
        d.setDate(d.getDate() - 1); // Belongs to previous day's diary entry
      }
      return \`\${d.getFullYear()}-\${String(d.getMonth() + 1).padStart(2, '0')}-\${String(d.getDate()).padStart(2, '0')}\`;
    }

    const now = new Date();
    const timeStr = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    console.log("Quick Entry - " + getWordedDate(getDiaryDateStr(now)) + " " + timeStr);
`;
require('fs').writeFileSync('C:/Users/Aaron Munro/Documents/GitHub/sleeptracking/test_date.js', code);
