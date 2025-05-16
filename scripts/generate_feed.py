#!/usr/bin/env python3
import json
from pathlib import Path

# ─── Load your daily studies from JSON ────────────────────────────────────────
with open("data/studies.json", encoding="utf-8") as f:
    STUDIES = json.load(f)

# ─── HTML header & shared CSS ────────────────────────────────────────────────
HEADER = """<!DOCTYPE html>
<html lang="en"><head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Daily Study Digest</title>
  <style>
    :root {
      --bg: #fff; --fg: #111; --link: #0066cc; --divider: #ccc;
    }
    body.dark-mode {
      --bg: #121212; --fg: #e0e0e0; --link: #88c0d0; --divider: #444;
    }
    body {
      margin:0; padding:2rem;
      font-family:sans-serif;
      background:var(--bg);
      color:var(--fg);
      line-height:1.5;
    }
    .toggle-btn {
      position:fixed; top:1rem; right:1rem;
      background:none; border:none; font-size:1.5rem; cursor:pointer;
      color:var(--fg);
    }
    a { color:var(--link); text-decoration:none; }
    a:hover { text-decoration:underline; }
    h1 {
      margin-top:4rem;
      border-bottom:1px solid var(--divider);
      padding-bottom:.3rem;
    }
    .study { margin-bottom:2rem; }
    .study h2 {
      margin:.5rem 0 .2rem;
      font-size:1.2rem;
      text-decoration:underline;
    }
    .source, .authors {
      display:block; font-size:.9rem; color:gray;
      margin-bottom:.2rem;
    }
    .label {
      font-weight:bold; margin-top:1rem; display:block;
    }
    ul { margin:.5em 0 1em 1.5em; }
    ul li { margin-bottom:.3em; }
    hr { border:0; border-top:1px solid var(--divider); margin:2rem 0; }
  </style>
</head><body>
  <button class="toggle-btn" onclick="toggleDarkMode()">🌙</button>
  <p><a href="archive.html">📚 View Past Daily Studies</a></p>
"""

FOOTER = """
  <script>
    function toggleDarkMode() {
      document.body.classList.toggle('dark-mode');
      localStorage.theme = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
    }
    if (localStorage.theme === 'dark') {
      document.body.classList.add('dark-mode');
    }
  </script>
</body></html>"""

# ─── Build HTML ────────────────────────────────────────────────────────────────
parts = [HEADER]

# Track 1 header
parts.append("  <h1>The Social Layer</h1><hr>\n")
for s in STUDIES[:5]:
    title = s.get("title", "Untitled Study")
    authors = s.get("authors", "")
    source  = s.get("source", "")
    summary = s.get("summary", "")
    notable = s.get("why_notable", s.get("notable", ""))

    parts.append(f"""
  <div class="study">
    <h2>{title}</h2>
    <span class="authors">Authors: {authors}</span>
    <span class="source">Source: {source}</span>
    <span class="label">Summary:</span>
    <p>{summary}</p>
    <span class="label">Why it’s notable:</span>
    <p>{notable}</p>
  </div>""")

# Track 2 header
parts.append("\n  <h1>Architectures of Capital</h1><hr>\n")
for s in STUDIES[5:]:
    title      = s.get("title", "Untitled Study")
    authors    = s.get("authors", "")
    source     = s.get("source", "")
    summary    = s.get("summary", "")
    example    = s.get("example", "")
    powerful   = s.get("why_powerful", "")
    explain    = s.get("further_explanation", "")
    projects   = s.get("projects", [])

    proj_list = "\n".join(f"<li>{p}</li>" for p in projects)

    parts.append(f"""
  <div class="study">
    <h2>{title}</h2>
    <span class="authors">Authors: {authors}</span>
    <span class="source">Source: {source}</span>
    <span class="label">Summary:</span>
    <p>{summary}</p>
    <span class="label">Example:</span>
    <p>{example}</p>
    <span class="label">Why it’s powerful:</span>
    <p>{powerful}</p>
    <span class="label">Further explanation:</span>
    <p>{explain}</p>
    <span class="label">Projects using this:</span>
    <ul>
      {proj_list}
    </ul>
  </div>""")

parts.append(FOOTER)

# ─── Write out the file ───────────────────────────────────────────────────────
html = "".join(parts)
Path("pages/index.html").write_text(html, encoding="utf-8")
print("Rebuilt pages/index.html with", len(STUDIES), "studies")
