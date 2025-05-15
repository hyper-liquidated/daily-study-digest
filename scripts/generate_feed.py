#!/usr/bin/env python3
import requests
from pathlib import Path

# ─── Your 10 studies ────────────────────────────────────────────────────────────
STUDIES = [
    {
        "title": "The Paradox of Choice Revisited",
        "source": "Journal of Experimental Psychology: General, 2024",
        "summary": "Revisits the famous “jam experiment” and finds that fewer choices consistently result in faster decisions and greater satisfaction.",
    },
    {
        "title": "The Inheritance Lottery: How Family Wealth Shapes Risk-Taking and Innovation",
        "source": "Quarterly Journal of Economics, 2024",
        "summary": "Shows unexpected inheritances increase entrepreneurship — but only among top-wealth households.",
    },
    {
        "title": "How Cities Shape Mental Health: Noise, Density, and Access",
        "source": "Lancet Public Health, 2023",
        "summary": "Green space and access to services reduce anxiety, while noise and isolation increase risk across dozens of cities.",
    },
    {
        "title": "The Scarcity Mindset Revisited: Cognitive Load or Learned Helplessness?",
        "source": "Nature Human Behaviour, 2024",
        "summary": "Proposes “learned helplessness” rather than “bandwidth tax” as the mechanism behind scarcity’s cognitive impacts.",
    },
    {
        "title": "Algorithmic Nudges for Civic Participation",
        "source": "PNAS, 2023",
        "summary": "Shows that simple reminder emails outperform social-media campaigns in boosting voter turnout and civic engagement.",
    },
    {
        "title": "What Is a Zero-Knowledge Proof (ZKP) and Why Should You Care?",
        "source": "Ethereum Foundation blog series, 2024",
        "summary": "A ZKP lets you prove you know something—say, a wallet password—without revealing the underlying details.",
    },
    {
        "title": "Latency Arbitrage and the Hidden Economics of Speed",
        "source": "Budish, Cramton & Shim (2015 + 2023 follow-ups)",
        "summary": "High-frequency traders exploit millisecond speed edges for tiny profits, distorting price discovery and social welfare.",
    },
    {
        "title": "Rollups & Data Availability: Why Scaling Isn’t Just About Throughput",
        "source": "Celestia & StarkWare blogs, 2024",
        "summary": "Rollups aggregate transactions to boost throughput, but without guaranteed on-chain data availability, users can’t independently verify state.",
    },
    {
        "title": "Collateral Rehypothecation in DeFi Lending Markets",
        "source": "Gauntlet Research, 2024",
        "summary": "Analyzes how Aave and Compound reuse deposited collateral across protocols, creating hidden leverage chains.",
    },
    {
        "title": "Stablecoin Peg Risk: When “1 : 1” Isn’t Enough",
        "source": "Chicago Booth Working Paper, 2023",
        "summary": "Even fully collateralized stablecoins can break peg due to run-dynamics, liquidity spirals, and price-path dependencies.",
    },
]
# ────────────────────────────────────────────────────────────────────────────────

def fetch_crossref_url(title):
    """Return a DOI.org link or None if lookup fails."""
    try:
        resp = requests.get(
            "https://api.crossref.org/works",
            params={"query.title": title, "rows": 1, "sort": "relevance"},
            timeout=15,
        )
        resp.raise_for_status()
        items = resp.json().get("message", {}).get("items", [])
        if not items:
            return None
        doi = items[0].get("DOI")
        return f"https://doi.org/{doi}" if doi else None
    except requests.RequestException:
        return None

def make_index_html(studies):
    header = """<!DOCTYPE html>
<html lang="en"><head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Daily Study Digest</title>
  <style>
    :root {
      --bg: #fff; --fg: #111;
      --link: #0066cc; --divider: #ccc;
    }
    body.dark-mode {
      --bg: #121212; --fg: #e0e0e0;
      --link: #88c0d0; --divider: #444;
    }
    body {
      margin:0; padding:2rem;
      font-family:sans-serif;
      background-color:var(--bg);
      color:var(--fg);
      line-height:1.5;
    }
    .toggle-btn {
      position:fixed; top:1rem; right:1rem;
      background:none; border:none;
      font-size:1.5rem; cursor:pointer;
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
    .source {
      font-size:.9rem; color:gray;
      margin-bottom:.5rem; display:block;
    }
    .label {
      font-weight:bold;
      margin-top:.5rem;
      display:block;
    }
    hr { border:0; border-top:1px solid var(--divider); margin:2rem 0; }
  </style>
</head><body>
  <button class="toggle-btn" onclick="toggleDarkMode()">🌙</button>
  <p><a href="archive.html">📚 View Past Daily Studies</a></p>

  <h1>The Social Layer</h1><hr>"""

    block_tpl = """
  <div class="study">
    <h2>{title_html}</h2>
    <span class="source">{source}</span>
    <span class="label">Summary:</span>
    <p>{summary}</p>
  </div>"""

    parts = [header]

    # Track 1
    for s in studies[:5]:
        url = fetch_crossref_url(s["title"])
        title_html = f'<a href="{url}" target="_blank">{s["title"]}</a>' if url else s["title"]
        parts.append(block_tpl.format(
            title_html=title_html,
            source=s["source"],
            summary=s["summary"]
        ))

    # Track 2
    parts.append("\n  <h1>Architectures of Capital</h1><hr>")
    for s in studies[5:]:
        url = fetch_crossref_url(s["title"])
        title_html = f'<a href="{url}" target="_blank">{s["title"]}</a>' if url else s["title"]
        parts.append(block_tpl.format(
            title_html=title_html,
            source=s["source"],
            summary=s["summary"]
        ))

    footer = """
  <script>
    function toggleDarkMode() {
      document.body.classList.toggle('dark-mode');
      localStorage.theme = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
    }
    if (localStorage.theme==='dark') document.body.classList.add('dark-mode');
  </script>
</body></html>"""

    parts.append(footer)
    return "".join(parts)

if __name__ == "__main__":
    html = make_index_html(STUDIES)
    Path("index.html").write_text(html, encoding="utf-8")