import re

filepath = "C:/Users/Aaron Munro/Documents/GitHub/sleeptracking/index.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# Fix HTML escaped characters in the <script> block
script_start = html.find("<script>")
if script_start != -1:
    before = html[:script_start]
    script_content = html[script_start:]
    
    script_content = script_content.replace("&gt;", ">")
    script_content = script_content.replace("&lt;", "<")
    script_content = script_content.replace("&amp;", "&")
    
    # Check if there are any other html entities that need decoding?
    # Usually it's just those three.
    
    html = before + script_content

with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)
