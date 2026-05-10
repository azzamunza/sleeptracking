import sys

file_path = r"C:\Users\Aaron Munro\Documents\GitHub\sleeptracking\index.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update CSS for .toggle-btn:disabled
old_css = ".toggle-btn:disabled { background: #f5f5f5; border: 1px solid #ddd; color: #aaa; }"
new_css = ".toggle-btn:disabled { background: #e0e0e0; border-color: transparent; color: #999; cursor: not-allowed; }\n    .toggle-btn.active:disabled { background: #555; border-color: #555; color: white; }"
html = html.replace(old_css, new_css)

# 2. Add Read Only Mode texts
old_h3_hourly = "<h3>Hourly Log</h3>"
new_h3_hourly = """<h3>Hourly Log <span class="read-only-text" style="display:none; font-size: 12px; font-weight: normal; color: #777; margin-left: 10px; font-style: italic;">read only mode</span></h3>"""
html = html.replace(old_h3_hourly, new_h3_hourly)

old_type = """      <input type="text" id="type-of-day" placeholder="e.g. Work">
    </div>"""
new_type = """      <input type="text" id="type-of-day" placeholder="e.g. Work">
      <div class="read-only-text" style="display:none; text-align: right; font-size: 11px; color: #777; font-style: italic; margin-top: -5px;">read only mode</div>
    </div>"""
html = html.replace(old_type, new_type)

# Show read-only text in practitioner mode
old_prac = "isPractitionerMode = true;"
new_prac = "isPractitionerMode = true;\n      document.querySelectorAll('.read-only-text').forEach(el => el.style.display = '');"
html = html.replace(old_prac, new_prac)

# 3. Disable newly created elements in renderHours()
old_render_btn = "toggles.appendChild(btn);"
new_render_btn = "if (isPractitionerMode) btn.disabled = true;\n          toggles.appendChild(btn);"
html = html.replace(old_render_btn, new_render_btn)

old_render_input = "noteInput.oninput = (e) => updateNote(h, e.target.value);"
new_render_input = "noteInput.oninput = (e) => updateNote(h, e.target.value);\n        if (isPractitionerMode) noteInput.disabled = true;"
html = html.replace(old_render_input, new_render_input)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
