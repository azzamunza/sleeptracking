import sys

file_path = r"C:\Users\Aaron Munro\Documents\GitHub\sleeptracking\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# Fix the CSS for table-date to make it stronger
css_old = ".table-date { min-width: 90px; white-space: nowrap; }"
css_new = ".table-date { min-width: 110px; width: 12ch; white-space: nowrap; }"
html = html.replace(css_old, css_new)

# Add class to the header
h_old = """          <thead>
          <tr>
            <th>Date</th>
            <th>Day</th>
            <th>Type</th>`;"""
h_new = """          <thead>
          <tr>
            <th class="table-date">Date</th>
            <th>Day</th>
            <th>Type of day</th>`;"""
html = html.replace("<th>Date</th>\n            <th>Day</th>\n            <th>Type</th>", "<th class=\"table-date\">Date</th>\n            <th>Day</th>\n            <th class=\"table-type\">Type of day</th>")


# Add class to the rows
r_old = """          html += `<tr>
            <td>${info.date}</td>
            <td>${info.day}</td>
            <td>${row.type_of_day || ''}</td>`;"""
r_new = """          html += `<tr>
            <td class="table-date">${info.date}</td>
            <td>${info.day}</td>
            <td class="table-type">${row.type_of_day || ''}</td>`;"""
html = html.replace(r_old, r_new)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
