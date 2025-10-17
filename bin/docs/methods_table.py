# Create JSON source, then generate both a Markdown table and an HTML grid from it.
import json, textwrap, pandas as pd
from pathlib import Path

# Save JSON
script_path = Path(__file__).resolve()
sys_path = str(script_path.parents)
from config import REPO_PATH
outdir = REPO_PATH / "notes"
outdir.mkdir(parents=True, exist_ok=True)
json_path = outdir / "methods.json"
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Generate Markdown table
headers = ["Method Abbreviation", "Method Name", "Method Category", "Method_png_path", "Method_link", "Extra"]
md_lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"]*len(headers)) + " |"]
for row in data:
    md_row = [str(row.get(h,"")) for h in headers]
    md_lines.append("| " + " | ".join(md_row) + " |")
md_content = "\n".join(md_lines)

md_path = outdir / "methods.md"
md_path.write_text(md_content, encoding="utf-8")

# Generate HTML grid (4 columns) from the same JSON
card_template = textwrap.dedent("""
<div class="card">
  {img_tag}
  <strong>{abbr}</strong><br/>
  {name}<br/>
  <em>{cat}</em><br/>
  {link_tag}
  {extra_tag}
</div>
""").strip()

cards_html = []
for row in data:
    img = row.get("Method_png_path") or ""
    link = row.get("Method_link") or ""
    extra = row.get("Extra") or ""
    img_tag = f'<img src="{img}" alt="{row["Method Name"]}" width="150"/><br/>' if img else ""
    link_tag = f'<a href="{link}">Link</a>' if link else ""
    extra_tag = f'<br/><a href="{extra}">Extra</a>' if extra else ""
    cards_html.append(card_template.format(
        img_tag=img_tag,
        abbr=row["Method Abbreviation"],
        name=row["Method Name"],
        cat=row["Method Category"],
        link_tag=link_tag,
        extra_tag=extra_tag
    ))

html_content = textwrap.dedent(f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>NeuroPySeminar Methods Grid</title>
  <style>
    :root {{ --gap: 20px; --card-pad: 12px; }}
    body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 24px; }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
      gap: var(--gap);
      text-align: center;
      align-items: start;
    }}
    .card {{
      border: 1px solid #e5e7eb;
      border-radius: 12px;
      padding: var(--card-pad);
      box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }}
    .card img {{ max-width: 100%; height: auto; border-radius: 8px; }}
    .card a {{ text-decoration: none; }}
    .card a:hover {{ text-decoration: underline; }}
    .header {{ margin-bottom: 16px; display:flex; justify-content: space-between; align-items: baseline; }}
    .header h1 {{ font-size: 20px; margin: 0; }}
    .count {{ color: #6b7280; font-size: 14px; }}
  </style>
</head>
<body>
  <div class="header">
    <h1>NeuroPySeminar Methods</h1>
    <div class="count">{len(data)} items</div>
  </div>
  <div class="grid">
    {"".join(cards_html)}
  </div>
</body>
</html>
""").strip()

html_path = outdir / "methods_grid.html"
html_path.write_text(html_content, encoding="utf-8")

# Also create a tiny JS snippet that would render from methods.json directly (optional, saved separately)
js_html = textwrap.dedent("""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>NeuroPySeminar Methods Grid (JS)</title>
  <style>
    :root { --gap: 20px; --card-pad: 12px; }
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 24px; }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
      gap: var(--gap);
      text-align: center;
      align-items: start;
    }
    .card {
      border: 1px solid #e5e7eb;
      border-radius: 12px;
      padding: var(--card-pad);
      box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    .card img { max-width: 100%; height: auto; border-radius: 8px; }
    .card a { text-decoration: none; }
    .card a:hover { text-decoration: underline; }
    .header { margin-bottom: 16px; display:flex; justify-content: space-between; align-items: baseline; }
    .header h1 { font-size: 20px; margin: 0; }
    .count { color: #6b7280; font-size: 14px; }
  </style>
</head>
<body>
  <div class="header">
    <h1>NeuroPySeminar Methods</h1>
    <div class="count" id="count"></div>
  </div>
  <div id="grid" class="grid"></div>
  <script>
    async function main() {
      const res = await fetch('methods.json');
      const data = await res.json();
      const grid = document.getElementById('grid');
      document.getElementById('count').textContent = `${data.length} items`;
      grid.innerHTML = data.map(row => {
        const img = row.Method_png_path ? `<img src="${row.Method_png_path}" alt="${row["Method Name"]}" width="150"/><br/>` : "";
        const link = row.Method_link ? `<a href="${row.Method_link}">Link</a>` : "";
        const extra = row.Extra ? `<br/><a href="${row.Extra}">Extra</a>` : "";
        return `<div class="card">${img}<strong>${row["Method Abbreviation"]}</strong><br/>${row["Method Name"]}<br/><em>${row["Method Category"]}</em><br/>${link}${extra}</div>`;
      }).join('');
    }
    main();
  </script>
</body>
</html>
""").strip()

js_html_path = outdir / "methods_grid_from_json.html"
js_html_path.write_text(js_html, encoding="utf-8")

# Methods grid table (GitHub-friendly: no CSS; uses <table> with 4 columns)
# === Generate Markdown file with explicit 4 columns × 3 rows ===
cards_per_row = 4
rows_html = []

for i in range(0, len(data), cards_per_row):
    tds = []
    for row in data[i:i+cards_per_row]:
        img = row.get("Method_png_path") or ""
        abbr = row.get("Method Abbreviation", "")
        name = row.get("Method Name", "")
        cat  = row.get("Method Category", "")
        link = row.get("Method_link") or ""
        extra = row.get("Extra") or ""

        img_tag   = f'<img src="png/{img}" width="150"><br>' if img else ""
        link_tag  = f'<a href="{link}">Link</a>' if link else ""
        extra_tag = f'<br><a href="{extra}">Extra</a>' if extra else ""

        cell = f"""<td align="center" valign="top">
  {img_tag}
  <strong>{abbr}</strong><br>
  {name}<br>
  <em>{cat}</em><br>
  {link_tag}{extra_tag}
</td>"""
        tds.append(cell)

    # pad row if not a multiple of 4 (future-proofing)
    while len(tds) < cards_per_row:
        tds.append("<td></td>")

    rows_html.append("<tr>\n" + "\n".join(tds) + "\n</tr>")

table_md = "<table>\n" + "\n".join(rows_html) + "\n</table>\n"

md_grid_path = outdir / "methods_grid.md"
md_grid_path.write_text(table_md, encoding="utf-8")

# Print summary
print(f"Generated {json_path}, {md_path}, {html_path}, {js_html_path}, and {md_grid_path}")