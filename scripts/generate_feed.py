#!/usr/bin/env python3
import json
from datetime import datetime

# ─── Helpers for date formatting ──────────────────────────────────────────────
def format_pubdate(datestr):
    """Convert YYYY-MM-DD → 'Wed, 14 May 2025 00:00:00 +0000' for RSS."""
    dt = datetime.fromisoformat(datestr)
    return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")

def human_date(datestr):
    """Convert YYYY-MM-DD → 'May 14, 2025' for display."""
    dt = datetime.fromisoformat(datestr)
    return dt.strftime("%B %-d, %Y")

# ─── Load your generated studies.json ───────────────────────────────────────────
with open("data/studies.json", "r", encoding="utf-8") as f:
    studies = json.load(f)

# ─── 1) Build the HTML page ────────────────────────────────────────────────────
html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Daily Study Digest</title>
  <style>
    body { font-family: sans-serif; line-height: 1.5; max-width: 800px; margin: 2em auto; padding: 0 1em; }
    h1 { text-align: center; margin-bottom: 0.5em; }
    .subscribe { text-align: right; margin-bottom: 2em; }
    .subscribe a { font-weight: bold; text-decoration: none; }
    .item { border-bottom: 1px solid #e0e0e0; padding-bottom: 1.5em; margin-bottom: 1.5em; }
    .item h2 { margin: 0.2em 0; }
    .meta { font-size: 0.9em; font-style: italic; color: #666; margin: 0.5em 0; }
    .date { font-style: normal; color: #999; margin-left: 0.5em; }
    ul.notable { margin-left: 1em; margin-bottom: 1em; }
    ul.notable li { margin-bottom: 0.5em; }
  </style>
</head>
<body>
  <h1>Daily Study Digest</h1>
  <div class="subscribe">
    <a href="daily_study_digest.xml">🔗 Subscribe via RSS</a>
  </div>
"""

for s in studies:
    title       = s["title"]
    authors     = ", ".join(s.get("authors", []))
    source      = s.get("source_url", s.get("source", ""))
    summary     = s.get("summary", "")
    why_list    = "\n".join(f"<li>{pt}</li>" for pt in s.get("why_it_matters", []))
    date_display= human_date(s["date"])

    # Meta line under the title
    meta_html = f'<p class="meta">{authors} ({source}) <span class="date">({date_display})</span></p>'

    html += f"""
  <div class="item">
    <h2>{title}</h2>
    {meta_html}
    <p><strong>Summary:</strong> {summary}</p>
    <p><strong>Why it’s notable:</strong></p>
    <ul class="notable">
{why_list}
    </ul>
  </div>
"""

html += """
</body>
</html>
"""

with open("../index.html", "w", encoding="utf-8") as f:
    f.write(html)

# ─── 2) Build the RSS feed ─────────────────────────────────────────────────────
items = []
for s in studies:
    title       = s["title"]
    authors     = ", ".join(s.get("authors", []))
    source      = s.get("source_url", s.get("source", ""))
    summary     = s.get("summary", "")
    pub_date    = format_pubdate(s["date"])
    meta_line   = f"{authors} ({source})" if authors else source

    item = f"""<item>
  <title>{title}</title>
  <description><![CDATA[
{meta_line}

{summary}
  ]]></description>
  <pubDate>{pub_date}</pubDate>
</item>"""
    items.append(item)

rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>Daily Study Digest – Track 1 + Track 2</title>
  <link>https://hyper-liquidated.github.io/daily-study-digest/</link>
  <description>Daily curated studies in behavioral science, crypto, and finance.</description>
{''.join(items)}
</channel>
</rss>"""

with open("../daily_study_digest.xml", "w", encoding="utf-8") as f:
    f.write(rss)

print(f"Generated {len(studies)} items: index.html and daily_study_digest.xml")