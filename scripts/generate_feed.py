#!/usr/bin/env python3
import requests
from pathlib import Path

STUDIES = [
    {
        "title": "The Paradox of Choice Revisited",
        "source": "Journal of Experimental Psychology: General, 2024",
        "summary": "Revisits the famous 'jam experiment' and finds that fewer choices consistently result in faster decisions and greater satisfaction.",
    },
    # … your other 9 studies here …
]

def fetch_crossref_url(title: str) -> str | None:
    try:
        resp = requests.get(
            "https://api.crossref.org/works",
            params={"query.title": title, "rows": 1, "sort": "relevance"},
            timeout=30
        )
        resp.raise_for_status()
        items = resp.json().get("message", {}).get("items", [])
        if not items:
            return None
        doi = items[0].get("DOI")
        return f"https://doi.org/{doi}" if doi else None
    except requests.RequestException:
        # On timeout, DNS error, 5xx from Crossref, etc. → just skip linking
        return None

def make_index_html(studies: list[dict]) -> str:
    header = """<!DOCTYPE html>
<html lang="en"><head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>The Social Layer + Architectures of Capital</title>
  <style>
    /* your CSS (same as before) */
  </style>
</head><body>
  <button class="toggle-btn" onclick="toggleDarkMode()">🌙</button>
  <p><a href="archive.html">📚 View Past Daily Studies</a></p>
  <h1>The Social Layer</h1><hr>
"""
    footer = """
  <script>
    function toggleDarkMode() {
      document.body.classList.toggle('dark-mode');
    }
  </script>
</body></html>"""
    study_tpl = """
  <div class="study">
    <strong><u>{title_html}</u></strong><br>
    <span class="source">Source: {source}</span>
    <span class="label">Summary:</span>
    <p>{summary}</p>
  </div>"""

    parts = [header]
    # Track 1
    for s in studies[:5]:
        link = fetch_crossref_url(s["title"])
        title_html = f'<a href="{link}" target="_blank">{s["title"]}</a>' if link else s["title"]
        parts.append(study_tpl.format(
            title_html=title_html,
            source=s["source"],
            summary=s["summary"]
        ))
    # Track 2
    parts.append("\n  <h1>Architectures of Capital</h1><hr>")
    for s in studies[5:]:
        link = fetch_crossref_url(s["title"])
        title_html = f'<a href="{link}" target="_blank">{s["title"]}</a>' if link else s["title"]
        parts.append(study_tpl.format(
            title_html=title_html,
            source=s["source"],
            summary=s["summary"]
        ))
    parts.append(footer)
    return "".join(parts)

if __name__ == "__main__":
    html = make_index_html(STUDIES)
    Path("index.html").write_text(html, encoding="utf-8")