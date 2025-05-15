#!/usr/bin/env python3
import requests
from pathlib import Path

# ─── Your 10 studies ────────────────────────────────────────────────────────────
STUDIES = [
    {
        "title": "The Paradox of Choice Revisited",
        "source": "Journal of Experimental Psychology: General, 2024",
        "summary": "Revisits the famous 'jam experiment' and finds that fewer choices consistently result in faster decisions and greater satisfaction.",
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

def fetch_crossref_url(title: str) -> str | None:
    resp = requests.get(
        "https://api.crossref.org/works",
        params={"query.title": title, "rows": 1, "sort": "relevance"},
        timeout=10
    )
    resp.raise_for_status()
    items = resp.json().get("message", {}).get("items", [])
    if not items:
        return None
    doi = items[0].get("DOI")
    return f"https://doi.org/{doi}" if doi else None

def make_index_html(studies: list[dict]) -> str:
    # Base HTML up through your toggle button & archive link
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>The Social Layer + Architectures of Capital</title>
  <style>
    /* … your existing CSS here … */
  </style>
</head>
<body>
  <button class="toggle-btn" onclick="toggleDarkMode()">🌙</button>
  <p><a href="archive.html">📚 View Past Daily Studies</a></p>"""
    # Track 1
    html += """
  <h1>The Social Layer</h1>
  <hr>"""
    for s in studies[:5]:
        link = fetch_crossref_url(s["title"])
        if link:
            title_html = f'<a href="{link}" target="_blank">{s["title"]}</a>'
        else:
            title_html = s["title"]
        html += f"""
  <div class="study">
    <strong><u>{title_html}</u></strong><br>
    <span class="source">Source: {s['source']}</span>
    <span class="label">Summary:</span>
    <p>{s['summary']}</p>
  </div>"""

    # Track 2
    html += """
  <h1>Architectures of Capital</h1>
  <hr>"""
    for s in studies[5:]:
        link = fetch_crossref_url(s["title"])
        title_html = f'<a href="{link}" target="_blank">{s["title"]}</a>' if link else s["title"]
        html += f"""
  <div class="study">
    <strong><u>{title_html}</u></strong><br>
    <span class="source">Source: {s['source']}</span>
    <span class="label">Summary:</span>
    <p>{s['summary']}</p>
  </div>"""

    # Footer script
    html += """
  <script>
    function toggleDarkMode() {
      document.body.classList.toggle('dark-mode');
    }
  </script>
</body>
</html>"""
    return html

if __name__ == "__main__":
    content = make_index_html(STUDIES)
    Path("index.html").write_text(content, encoding="utf-8")