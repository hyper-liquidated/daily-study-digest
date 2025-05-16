#!/usr/bin/env python3
import json
from datetime import datetime

# ─── 1) Load the studies you already generate nightly ───
with open("data/studies.json") as f:
    studies = json.load(f)

# ─── 2) Helper to format the publication date for RSS ───
def format_pubdate(datestr):
    # assumes datestr is "YYYY-MM-DD"
    dt = datetime.fromisoformat(datestr)
    return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")

# ─── 3) Build each <item> including authors & source ───
items_xml = []
for s in studies:
    title       = s["title"]
    summary     = s["summary"]
    authors     = s.get("authors", [])
    source      = s.get("source_url", s.get("source", ""))

    # ←── These two lines pull in authors + journal under the title
    authors_line = ", ".join(authors)                # "Dr. A, Prof. B"
    meta_line    = f"{authors_line} ({source})" if authors_line else source

    pub_date = format_pubdate(s["date"])

    item = f"""<item>
  <title>{title}</title>
  <description><![CDATA[
{meta_line}

{summary}
  ]]></description>
  <pubDate>{pub_date}</pubDate>
</item>"""
    items_xml.append(item)

# ─── 4) Wrap everything in your <rss> template ───
rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>Daily Study Digest – Track 1 + Track 2</title>
  <link>https://hyper-liquidated.github.io/daily-study-digest/</link>
  <description>Daily curated studies in behavioral science, crypto, and finance.</description>
{''.join(items_xml)}
</channel>
</rss>"""

# ─── 5) Write out the refreshed RSS file ───
with open("daily_study_digest.xml", "w", encoding="utf-8") as f:
    f.write(rss)
print(f"Wrote {len(items_xml)} items to daily_study_digest.xml")