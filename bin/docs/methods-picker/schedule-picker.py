#!/usr/bin/env python3
"""
NeuroPySeminar: CSV → standalone schedule HTML generator
"""
from __future__ import annotations
import argparse
import csv
import html
from pathlib import Path
import json

PROJECT_FOLDER= Path('/home/arash/Documents/Science/Uni/NeuroPy')
CSV_FILE = PROJECT_FOLDER / 'Management/schedule2025/NeuroPySeminar_Schedule_WiSe2025.csv'
METHODS_FILE = PROJECT_FOLDER / 'Management/selectpaper/methods.json'
OUTPUT_FILE = PROJECT_FOLDER / 'Management/selectpaper/schedule-picker.html'

DEFAULT_META = {
	"Intro Session": {"link": "", "tip": "Introductory session for course structure, logistics, and overview."}
}

CSS_FILE = PROJECT_FOLDER / 'Management/selectpaper/schedule-picker.css'
STYLE = CSS_FILE.read_text(encoding='utf-8')

SCRIPT_PATH = PROJECT_FOLDER / 'Management/selectpaper/schedule-picker.js'
SCRIPT = SCRIPT_PATH.read_text(encoding='utf-8')


def load_meta(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # map by Method Name for easy lookup
    meta = {}
    for m in data:
        name = m["Method Name"]
        meta[name] = {
            "link": m.get("Method_link", ""),
            "tip": m.get("Method_tip", ""),
            "abbr": m.get("Method Abbreviation", ""),
            "category": m.get("Method Category", ""),
        }
    return meta

meta = load_meta(METHODS_FILE)

HTML_HEAD = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <style>{style}</style>
</head>
<body>
  <div class="wrap">
	<h1>{heading}</h1>
	<p class="sub">Hover over a topic for a short description. Pick your top three <em>methods</em> (ranks 1–3). Your rank applies to both the Theory and Exercise session of that method automatically.</p>
	<div class="toolbar">
	  <input id="name" type="text" placeholder="Your name" />
	  <button class="btn" id="exportCsv">Export CSV</button>
	  <button class="btn" id="save">Save</button>
	  <button class="btn" id="clear">Clear</button>
	  <button class="btn" id="email">Save & Email</button>
	</div>
	<div class="tablewrap">
	  <table aria-label="Schedule"><thead><tr>
		<th style="width:60px">Week</th>
		<th style="width:92px">Date</th>
		<th style="width:64px">Day</th>
		<th style="width:220px">Type</th>
		<th>Topic</th>
		<th style="width:160px">Presenter</th>
		<th style="width:140px">Your Rank</th>
	  </tr></thead><tbody>
"""

HTML_FOOT = """
	  </tbody></table>
	  <div id="tooltip" class="tooltip hidden"></div>
	</div>
  </div>
  <script>/* <![CDATA[ */ {script} /* ]]> */</script>
</body>
</html>
"""

def is_rankable(topic: str, presenter: str) -> bool:
	if presenter and presenter.strip():
		return False
	if not topic:
		return False
	t = topic.strip()
	if t == "Intro Session":
		return False
	if "Special Session" in t:
		return False
	return True

def topic_cell_html(topic, meta, rankable):
    """Return the <td> HTML for the topic cell, using JSON metadata."""
    info = meta.get(topic, {})  # get info if available
    link = info.get("link", "")
    tip = info.get("tip", "")

    data_attrs = []
    if rankable:
        data_attrs.append(f'data-topic="{html.escape(topic)}"')
    if link:
        data_attrs.append(f'data-link="{html.escape(link)}"')
    if tip:
        data_attrs.append(f'data-tip="{html.escape(tip)}"')

    data_attr_str = " " + " ".join(data_attrs) if data_attrs else ""

    # rank chip only for rankable methods
    chip_html = '<span class="rank-chip rank-none"></span>' if rankable else ""

    # clickable link if available
    if link:
        topic_html = f'<a href="{html.escape(link)}">{html.escape(topic)}</a>'
    else:
        topic_html = html.escape(topic)

    return f'<td class="topic"{data_attr_str}>{chip_html}{topic_html}</td>'

def row_html(week, date, day, session_type, topic, presenter, rankable, meta):
    topic_td = topic_cell_html(topic, meta, rankable)
    pres_td = f"<strong>{html.escape(presenter)}</strong>" if presenter else ""
    rank_td = (
        f'<td class="rank"><select class="rank-select" data-for="{html.escape(topic)}">'
        '<option value="">No rank</option>'
        '<option value="1">Rank 1</option>'
        '<option value="2">Rank 2</option>'
        '<option value="3">Rank 3</option>'
        "</select></td>"
        if rankable
        else "<td></td>"
    )

    return f"<tr><td>{week}</td><td>{date}</td><td>{day}</td><td>{session_type}</td>{topic_td}<td>{pres_td}</td>{rank_td}</tr>"

def load_rows(csv_path: Path) -> list[dict]:
	with csv_path.open(newline='', encoding='utf-8') as f:
		reader = csv.DictReader(f)
		rows = []
		for r in reader:
			rows.append({
				'Week': (r.get('Week') or '').strip(),
				'Date': (r.get('Date') or '').strip(),
				'Day': (r.get('Day') or '').strip(),
				'Type': (r.get('Type') or '').strip(),
				'Topic': (r.get('Topic') or '').strip(),
				'Presenter': (r.get('Presenter') or '').strip(),
			})
		return rows

def load_methods_meta(methods_path: Path) -> dict:
    """Load method metadata (link + hover tip) from JSON."""
    meta = {}
    with methods_path.open('r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        name = (item.get('Method Name') or '').strip()
        if not name:
            continue

        link = (item.get('Method_link') or '').strip()
        tip = (item.get('Method_tip') or '').strip()

        meta[name] = {'link': link, 'tip': tip}

    return meta

def build_html(rows: list[dict], title: str, heading: str, meta: dict) -> str:
	"""Generate the full HTML document for the schedule."""
	parts = [HTML_HEAD.format(title=html.escape(title), heading=html.escape(heading), style=STYLE)]

	for r in rows:
		week = r['Week']
		date = r['Date']
		day = r['Day']
		session_type = r['Type']
		topic = r['Topic']
		presenter = r['Presenter']

		rankable = is_rankable(topic, presenter)
		row = row_html(week, date, day, session_type, topic, presenter, rankable, meta)
		parts.append(row)

	parts.append(HTML_FOOT.format(script=SCRIPT))
	return ''.join(parts)

def main():
	ap = argparse.ArgumentParser(description="Generate NeuroPy schedule HTML from CSV")
	ap.add_argument('--out', required=False, type=Path, help='Output HTML path (default: alongside CSV)')
	ap.add_argument('--title', required=False, default='NeuroPySeminar • Schedule & Picker (WiSe 2025)')
	ap.add_argument('--heading', required=False, default='NeuroPySeminar — Weeks 1–14')
	ap.add_argument('--meta', required=False, type=Path, help='Optional JSON mapping {"Topic": {"link":..., "tip":...}} to override')
	args = ap.parse_args()

	rows = load_rows(CSV_FILE)

	meta = {}
	meta.update(load_methods_meta(METHODS_FILE))
	meta.update(DEFAULT_META)
	if args.meta and args.meta.exists():
		with args.meta.open('r', encoding='utf-8') as f:
			user_meta = json.load(f)
		if isinstance(user_meta, dict):
			meta.update(user_meta)

	html_out = build_html(rows, args.title, args.heading, meta)
	out_path = OUTPUT_FILE
	out_path.write_text(html_out, encoding='utf-8')
	print(f"Wrote: {out_path}")

if __name__ == '__main__':
	main()
