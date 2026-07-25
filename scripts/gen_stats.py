#!/usr/bin/env python3
"""Genera assets/stats-terminal.svg con stats reales de la API de GitHub.

Requiere GH_TOKEN en el entorno (PAT con scopes repo + read:org).
"""
import json
import os
import urllib.request
from datetime import datetime, timezone

USER = "Zyra-V21"
TOKEN = os.environ["GH_TOKEN"]

BG = "#000000"
GREEN = "#00ff41"
MID = "#00b32c"
DARK = "#008f11"
DIM = "#003b00"
BRIGHT = "#c8ffdb"

HIDE_LANGS = {"Makefile", "HTML", "CSS"}


def api(url, payload=None):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode() if payload else None,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "User-Agent": USER,
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


commits = api(f"https://api.github.com/search/commits?q=author:{USER}&per_page=1")["total_count"]
prs = api(f"https://api.github.com/search/issues?q=type:pr+author:{USER}&per_page=1")["total_count"]
merged = api(f"https://api.github.com/search/issues?q=type:pr+author:{USER}+is:merged&per_page=1")["total_count"]
user = api(f"https://api.github.com/users/{USER}")

created = datetime.fromisoformat(user["created_at"].replace("Z", "+00:00"))
now = datetime.now(timezone.utc)
days = max(1, (now - created).days)
per_day = commits / days

langs_q = """query { user(login: "%s") {
  repositories(first: 100, ownerAffiliations: [OWNER], isFork: false) {
    nodes { languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
      edges { size node { name } } } } } } }""" % USER
langs = {}
for repo in api("https://api.github.com/graphql", {"query": langs_q})["data"]["user"]["repositories"]["nodes"]:
    for e in repo["languages"]["edges"]:
        name = e["node"]["name"]
        if name not in HIDE_LANGS:
            langs[name] = langs.get(name, 0) + e["size"]
total = sum(langs.values()) or 1
top = sorted(langs.items(), key=lambda x: -x[1])[:8]
max_pct = max(100 * s / total for _, s in top)

W, PAD, LH, FS = 900, 24, 22, 15
COL2 = 470


def bar_line(name, size):
    pct = 100 * size / total
    filled = max(1, round(pct / max_pct * 14))
    return [
        (f"{name[:9]:<10}", BRIGHT),
        ("█" * filled, GREEN),
        ("░" * (14 - filled), DIM),
        (f" {pct:4.1f}%", MID),
    ]


# cada elemento: (x, [segmentos (texto, color)])
rows = [
    [(PAD, [("zyra@matrix", GREEN), (":~$ ", MID), ("whoami", BRIGHT)])],
    [(PAD, [(f"{USER} · blockchain engineer @ MigaLabs · EVM, data & ZK", MID)])],
    [],
    [(PAD, [("zyra@matrix", GREEN), (":~$ ", MID), ("stats --refresh", BRIGHT)])],
    [
        (PAD, [("[+] ", DARK), ("commits ", MID), (f"{commits:,}", BRIGHT), (f" · {per_day:.1f}/day", MID)]),
        (COL2, [("[+] ", DARK), ("pull requests ", MID), (f"{prs}", BRIGHT), (f" · {merged} merged", MID)]),
    ],
    [
        (PAD, [("[+] ", DARK), ("uptime ", MID), (f"{days}d", BRIGHT), (f" · since {created:%Y-%m-%d}", MID)]),
        (COL2, [("[+] ", DARK), ("repos ", MID), (f"{user['public_repos']}", BRIGHT), (" · followers ", MID), (f"{user['followers']}", BRIGHT)]),
    ],
    [],
    [(PAD, [("zyra@matrix", GREEN), (":~$ ", MID), ("langs --top", BRIGHT)])],
]
for i in range(0, len(top), 2):
    row = [(PAD, bar_line(*top[i]))]
    if i + 1 < len(top):
        row.append((COL2, bar_line(*top[i + 1])))
    rows.append(row)
rows.append([])

TITLE_H = 36
H = TITLE_H + PAD + LH * (len(rows) + 1) + 10

texts = []
y = TITLE_H + PAD + 4
for row in rows:
    for x, segs in row:
        tspans = "".join(f'<tspan fill="{c}">{esc(t)}</tspan>' for t, c in segs)
        texts.append(f'<text x="{x}" y="{y}" xml:space="preserve">{tspans}</text>')
    y += LH
texts.append(
    f'<text x="{PAD}" y="{y}"><tspan fill="{GREEN}">zyra@matrix</tspan>'
    f'<tspan fill="{MID}">:~$ </tspan><tspan fill="{GREEN}">█'
    f'<animate attributeName="opacity" values="1;1;0;0" dur="1.2s" repeatCount="indefinite"/></tspan></text>'
)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"
     font-family="'Courier New',monospace" font-size="{FS}">
  <rect width="{W}" height="{H}" rx="10" fill="{BG}" stroke="{DIM}" stroke-width="2"/>
  <rect width="{W}" height="{TITLE_H}" rx="10" fill="#010b02"/>
  <rect y="{TITLE_H - 10}" width="{W}" height="10" fill="#010b02"/>
  <circle cx="22" cy="{TITLE_H // 2}" r="6" fill="{DIM}"/>
  <circle cx="44" cy="{TITLE_H // 2}" r="6" fill="{DARK}"/>
  <circle cx="66" cy="{TITLE_H // 2}" r="6" fill="{GREEN}"/>
  <text x="{W // 2}" y="{TITLE_H // 2 + 5}" text-anchor="middle" fill="{MID}" font-size="13">zyra@matrix: ~/stats</text>
  <text x="{W - PAD}" y="{TITLE_H // 2 + 5}" text-anchor="end" fill="{DARK}" font-size="12">sync {now:%Y-%m-%d}</text>
  {"".join(texts)}
</svg>'''

out = os.path.join(os.path.dirname(__file__), "..", "assets", "stats-terminal.svg")
with open(out, "w") as f:
    f.write(svg)
print(f"OK: {commits:,} commits · {per_day:.1f}/day · {prs} PRs ({merged} merged) · {len(top)} langs")
