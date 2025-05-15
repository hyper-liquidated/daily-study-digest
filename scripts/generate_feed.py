#!/usr/bin/env python3
import requests
from pathlib import Path

STUDIES = [
  {
    "title": "The Paradox of Choice Revisited",
    "source": "Journal of Experimental Psychology: General, 2024",
    "summary": "Revisits the famous 'jam experiment' …"
  },
  # … all 10 studies here …
]

def fetch_crossref_url(title):
    resp = requests.get(
        "https://api.crossref.org/works",
        params={"query.title": title, "rows":1, "sort":"relevance"},
        timeout=10
    )
    resp.raise_for_status()
    items = resp.json().get("message", {}).get("items", [])
    if not items: return None
    doi = items[0].get("DOI")
    return f"https://doi.org/{doi}" if doi else None

def make_index_html(studies):
    parts = [
        "<!DOCTYPE html>",
        "<html lang=\"en\"><head>",
        "  <meta charset=\"UTF-8\">",
        "  <meta name=\"viewport\" content=\"width=device-width,initial-scale=1.0\">",
        "  <title>The Social Layer + Architectures of Capital</title>",
        "  <!-- your full <style>…&ndash;>…</style> -->",
        "</head><body>",
        "  <button class=\"toggle-btn\" onclick=\"toggleDarkMode()\">🌙</button>",
        "  <p><a href=\"archive.html\">📚 View Past Daily Studies</a></p>",
        "  <h1>The Social Layer</h1><hr>"
    ]
    # track 1
    for s in studies[:5]:
        link = fetch_crossref_url(s["title"])
        title_html = f'<a href="{link}" target="_blank">{s["title"]}</a>' if link else s["title"]
        parts += [
          "<div class=\"study\">",
          f"<strong><u>{title_html}</u></strong><br>",
          f"<span class=\"source\">Source: {s['source']}</span>",
          "<span class=\"label\">Summary:</span>",
          f"<p>{s['summary']}</p>",
          "</div>"
        ]
    parts += ["  <h1>Architectures of Capital</h1><hr>"]
    # track 2 (same pattern… include example, why, takeaway)
    for s in studies[5:]:
        link = fetch_crossref_url(s["title"])
        title_html = f'<a href=\"{link}\" target=\"_blank\">{s[\"title\"]}</a>' if link else s["title"]
        parts += [
          "<div class=\"study\">",
          f"<strong><u>{title_html}</u></strong><br>",
          f"<span class=\"source\">Source: {s['source']}</span>",
          "<span class=\"label\">Summary:</span>",
          f"<p>{s['summary']}</p>",
          # … your other sub-sections here …
          "</div>"
        ]
    parts += [
        "<script>function toggleDarkMode(){document.body.classList.toggle('dark-mode')}</script>",
        "</body></html>"
    ]
    return "\n".join(parts)

if __name__ == "__main__":
    html = make_index_html(STUDIES)
    Path("index.html").write_text(html, encoding="utf-8")