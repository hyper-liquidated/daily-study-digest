#!/usr/bin/env python3
"""
generate_feed.py

Builds a tab-based HTML homepage from data/studies.json
"""

import json
from pathlib import Path

# ---------- 1. Load studies --------------------------------------------------
DATA_FILE = Path("data/studies.json")
if not DATA_FILE.exists():
    raise FileNotFoundError("data/studies.json not found — ensure previous step copied it in")

studies = json.loads(DATA_FILE.read_text(encoding="utf-8"))

# ---------- 2. Group by track ------------------------------------------------
# ---------- 2. Group by track ------------------------------------------------
by_track = {}
for entry in studies:
    if isinstance(entry, dict) and "track" in entry:
        by_track.setdefault(entry["track"], []).append(entry)
    else:
        print(f"[WARN] Skipping malformed study entry: {entry!r}")
        
track_map = {
    "The Social Layer": "social-layer",
    "Architectures of Capital": "capital",
    "Systems of Play": "play",
    "The Health Layer": "health",
    "Long Horizons": "horizons",
    "The State Layer": "state",
}
order = list(track_map.values())

# ---------- 3. Render helpers ------------------------------------------------
def render_study(s):
    """Return HTML for a single study block."""
    h = [f'<div class="study-entry">', f'<h2>{s["title"]}</h2>']
    h.append(f'<span class="label">Summary:</span><p>{s["summary"]}</p>')
    h.append(f'<span class="label">Why notable:</span><p>{s["why_notable"]}</p>')

    # Track-specific optional fields
    if s.get("example"):
        h.append(f'<span class="label">Example:</span><p>{s["example"]}</p>')
    if s.get("why_powerful"):
        h.append(f'<span class="label">Why powerful:</span><p>{s["why_powerful"]}</p>')
    if s.get("further_explanation"):
        h.append(f'<span class="label">Further explanation:</span><p>{s["further_explanation"]}</p>')
    if s.get("projects"):
        h.append('<span class="label">Projects using this:</span><ul>')
        h.extend([f"<li>{p}</li>" for p in s["projects"]])
        h.append("</ul>")
    if s.get("lean"):
        h.append(f'<span class="label">Lean:</span> {s["lean"]}<br>')
    if s.get("counterpoint"):
        h.append(f'<span class="label">Counterpoint:</span><p>{s["counterpoint"]}</p>')

    h.append("</div>")
    return "\n".join(h)


def make_tab_buttons():
    return "".join(
        f'<button class="tab-btn" data-track="{tid}">{name}</button>'
        for name, tid in track_map.items()
    )


def make_track_sections():
    sections = []
    for name, tid in track_map.items():
        block = [f'<section id="{tid}" class="track-panel">']
        block.append('<button class="set-default">Set as Default Track</button>')
        for study in by_track.get(name, []):
            block.append(render_study(study))
        block.append("</section>")
        sections.append("\n".join(block))
    return "\n".join(sections)


# ---------- 4. Assemble full HTML -------------------------------------------
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Daily Study Digest</title>
  <style>
    :root {{ --bg:#fff; --fg:#111; --accent:#0077ff; }}
    [data-theme="dark"] {{ --bg:#121212; --fg:#e5e5e5; --accent:#3399ff; }}
    body {{ margin:0;font-family:system-ui,sans-serif;background:var(--bg);color:var(--fg); }}
    header {{ padding:1rem;display:flex;justify-content:space-between;
             align-items:center;border-bottom:1px solid var(--fg); }}
    .tabs {{ display:flex;flex-wrap:wrap;gap:0.5rem;padding:0 1rem; }}
    .tab-btn {{ cursor:pointer;padding:0.4rem 0.8rem;border:1px solid var(--fg);
                border-radius:4px;background:none;color:var(--fg); }}
    .tab-btn.active {{ background:var(--accent);color:#fff; }}
    .track-panel {{ display:none;padding:1rem;animation:fade .2s ease-in-out; }}
    .track-panel.active {{ display:block; }}
    @keyframes fade {{ from{{opacity:0}} to{{opacity:1}} }}
    .set-default {{ margin:0.5rem 0 1rem;padding:0.3rem 0.6rem;border:1px solid var(--accent);
                    background:none;color:var(--accent);cursor:pointer;border-radius:4px; }}
    .study-entry {{ border-bottom:1px solid var(--fg);padding:0.8rem 0; }}
    .study-entry h2 {{ margin:0 0 0.3rem;font-size:1.1rem; }}
    .label {{ font-weight:600; }}
  </style>
</head>
<body>
<header>
  <h1>Daily Study Digest</h1>
  <button id="themeToggle" title="Toggle dark/light mode">🌙</button>
</header>

<nav class="tabs" id="tabBar">{make_tab_buttons()}</nav>
{make_track_sections()}

<script>
  // ---------- Theme toggle ----------
  const themeBtn = document.getElementById('themeToggle');
  function setTheme(t) {{
    document.documentElement.dataset.theme = t;
    localStorage.theme = t;
    themeBtn.textContent = t === 'dark' ? '☀️' : '🌙';
  }}
  setTheme(localStorage.theme || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'));
  themeBtn.onclick = () => setTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark');

  // ---------- Tabs ----------
  const defaultTrack = localStorage.defaultTrack || '{order[0]}';
  const panels = document.querySelectorAll('.track-panel');
  document.querySelectorAll('.tab-btn').forEach(btn => {{
      btn.classList.toggle('active', btn.dataset.track === defaultTrack);
  }});
  panels.forEach(p => p.classList.toggle('active', p.id === defaultTrack));

  document.getElementById('tabBar').onclick = e => {{
    if (!e.target.matches('.tab-btn')) return;
    const id = e.target.dataset.track;
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.toggle('active', b === e.target));
    panels.forEach(p => p.classList.toggle('active', p.id === id));
  }};

  // ---------- Set as default ----------
  document.querySelectorAll('.set-default').forEach(btn => {{
      btn.onclick = () => {{
          const id = btn.parentElement.id;
          localStorage.defaultTrack = id;
          alert(id.replace(/-/g,' ') + ' is now your default track');
      }};
  }});
</script>
</body>
</html>
"""

# ---------- 5. Write file ----------------------------------------------------
out_path = Path("pages/index.html")
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(html, encoding="utf-8")
print(f"[INFO] Wrote {out_path}")