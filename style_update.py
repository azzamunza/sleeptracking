import sys
import re

file_path = r"C:\Users\Aaron Munro\Documents\GitHub\sleeptracking\index.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Title and Fonts
html = html.replace("<title>Sleep Tracker</title>", '<title>The Aaron Munro Diary of Sheep Counting</title>\n  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap" rel="stylesheet">')

# 2. CSS Variables
old_vars = """    :root {
      --bg: #f0f2f5;
      --card-bg: #ffffff;
      --text: #333;
      --primary: #4285f4;
      --border: #ccc;
    }"""
new_vars = """    :root {
      --bg: #111b33;
      --card-bg: #1e2d4a;
      --text: #fdf5d3;
      --primary: #7ba5d6;
      --border: #3b4f73;
      --input-bg: #0d1527;
    }"""
html = html.replace(old_vars, new_vars)

# 3. Font Family
html = html.replace("font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;", "font-family: 'Nunito', -apple-system, BlinkMacSystemFont, sans-serif;")

# 4. Button and Input Radius updates for friendly UI
html = html.replace("border-radius: 6px;", "border-radius: 20px; font-weight: 700; letter-spacing: 0.5px;")
html = html.replace("border-radius: 4px;", "border-radius: 12px;")
html = html.replace("box-shadow: 0 1px 3px rgba(0,0,0,0.1);", "box-shadow: 0 4px 12px rgba(0,0,0,0.3); border: 1px solid var(--border);")
html = html.replace("background: white;", "background: var(--card-bg);")
html = html.replace("background: #f9f9f9;", "background: #162444;")

# Replace specific CSS colors
html = html.replace("background: #e0e0e0;", "background: #3b4f73;")
html = html.replace("color: #999;", "color: #8aa1c4;")
html = html.replace("color: #333;", "color: var(--text);")
html = html.replace("color: #aaa;", "color: #8aa1c4;")
html = html.replace("border-bottom: 1px solid #ccc;", "border-bottom: 1px solid var(--border);")
html = html.replace("border-bottom: 1px solid #eee;", "border-bottom: 1px solid var(--border);")
html = html.replace("background: #f5f5f5;", "background: transparent;")
html = html.replace("border-color: transparent;", "border-color: #3b4f73;")

# Update inputs to use the new input background
input_css = """    input[type="text"], input[type="date"] {
      width: 100%; padding: 8px; margin-bottom: 10px; border: 1px solid var(--border); border-radius: 12px; box-sizing: border-box;
      background: var(--input-bg); color: var(--text);
    }
    select { background: var(--input-bg); color: var(--text); }"""
html = re.sub(r'input\[type="text"\], input\[type="date"\] \{.*?(?=    \.flex-between)', input_css + "\n", html, flags=re.DOTALL)

# 5. Auth Section Update
old_auth = """  <div class="card" id="auth-section">
    <h2>Sleep Tracker Login</h2>
    <button id="login-btn">Sign in with Google</button>
    <button onclick="clearCache()" style="background: #3b4f73; color: var(--text);">Clear Cache</button>
  </div>"""
new_auth = """  <div class="card" id="auth-section" style="max-width: 500px; margin: 40px auto; text-align: center; padding: 30px;">
    <img src="images/login-banner.png" alt="The Aaron Munro Diary of Sheep Counting" style="width: 100%; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
    <h2 style="margin-bottom: 25px; font-weight: 900; letter-spacing: 1px;">Welcome to the Diary</h2>
    <button id="login-btn" style="font-size: 16px; padding: 12px 30px;">Sign in with Google</button>
    <br><br>
    <button onclick="clearCache()" style="background: transparent; border: 1px solid var(--border); color: #8aa1c4; padding: 8px 20px; font-size: 12px;">Clear Cache</button>
  </div>"""
html = html.replace(old_auth, new_auth)

# 6. App Header Banner
old_app = """  <div id="app">
    <div class="card flex-between">"""
new_app = """  <div id="app">
    <img src="images/header-banner.png" alt="The Aaron Munro Diary of Sheep Counting" style="width: 100%; border-radius: 12px; margin-bottom: 15px; display: block; box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
    <div class="card flex-between">"""
html = html.replace(old_app, new_app)

# 7. Modal Styling tweaks
html = html.replace("background:rgba(0,0,0,0.5);", "background:rgba(10, 15, 30, 0.85);")
html = html.replace("color:#333; font-size:24px;", "color:var(--text); font-size:24px;")

# 8. Print overrides to ensure text is visible on white paper
print_css = """    /* Print Styles */
    @media print {
      @page { size: landscape; margin: 10mm; }
      body { background: white !important; margin: 0; padding: 0; color: black !important; }
      #auth-section, .card:not(#table-view), button, input, img { display: none !important; }
      #app { display: block !important; }
      #table-view { display: block !important; box-shadow: none; border: none; padding: 0; margin: 0; background: white !important; color: black !important; }
      #table-view h3 { font-size: 18px; margin-bottom: 5px; color: black !important; }
      table { width: 100%; border-collapse: collapse; font-size: 10px; min-width: auto; background: white !important; color: black !important; }
      th, td { border: 1px solid black !important; padding: 4px; color: black !important; }
      th { background: #eee !important; color: black !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
      .table-notes, .table-type, .table-date { color: black !important; }
      .note-item { border-bottom: 1px solid #aaa !important; }
      div { color: black !important; background: transparent !important; }
    }"""
html = re.sub(r'/\* Print Styles \*/.*?\}', print_css, html, flags=re.DOTALL)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
