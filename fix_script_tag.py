import re

filepath = "C:/Users/Aaron Munro/Documents/GitHub/sleeptracking/index.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# Fix the </script> inside the template literal
html = html.replace("</script>\n            </body></html>", "<\\/script>\n            </body></html>")

# Ensure the file ends with </script></body></html> if it's missing
if not html.strip().endswith("</html>"):
    if "</script>" not in html[html.rfind("// Initial calls"):]:
        html += "\n  </script>\n</body>\n</html>\n"

with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)
