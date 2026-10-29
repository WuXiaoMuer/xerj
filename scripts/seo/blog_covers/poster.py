"""Milestone poster: the celebratory cover for /blog/100-contributors.

The series covers in covers.py are square-matrix art with no text on the
hero. A milestone post gets a poster instead: the headline numbers set large
in Big Shoulders Display, over a curve of the repository's real star count.
covers.py calls ``page(post, kind, W, H)`` for any POSTS entry that sets
``poster``; the outputs, sizes and file names are the same as the series.

Every number on the poster is in the post, and the post's PR names where it
came from:

    stars        post["stars"]: GitHub stargazers_count, re-read right
                 before rendering
    curve        data/xerj-stargazers.json: the running star count per day
                 (America/Chicago), from every page of the stargazers API
    100          contributors on GitHub's contributor list, see the post
    7,226        hub.xerj.org/contributors/ on 2026-10-29
    #1           Trendshift: #1 Rust repository of the day and of the week
    5,000 to 17,000 stars in 12 days: the 5,000th star (2026-10-15) and the
                 17,000th star (2026-10-27) in data/xerj-stargazers.json

Colours are the site's day tokens (landing/style.css, landing/brand.html):
paper #FAFAF7, ink #1A1A1A, yellow #FFC400 as a fill, ochre #6B4400 for
accent text. Yellow never carries text on paper; ink text may sit on yellow.
"""

from __future__ import annotations

import html
import json
import pathlib
from datetime import date

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE / "data" / "xerj-stargazers.json"

T = {"paper": "#FAFAF7", "ink": "#1A1A1A", "yellow": "#FFC400", "ochre": "#6B4400",
     "mute": "#5f5d58", "rule": "#d9d6cc", "grid": "#ecebe4"}


def _f(v: float) -> str:
    return f"{v:.1f}".rstrip("0").rstrip(".")


def curve(w: float, h: float, stars: int) -> str:
    """The running star count as a filled area: yellow fill, ink edge, a
    square marker on today's count and two milestone ticks."""
    d = json.loads(DATA.read_text())
    days = list(d["daily"].items())
    d0 = date.fromisoformat(days[0][0])
    span = (date.fromisoformat(days[-1][0]) - d0).days or 1
    top = max(stars, days[-1][1])
    pts = [((date.fromisoformat(k) - d0).days / span * w, h - v / top * h) for k, v in days]
    line = " ".join(f"{_f(x)},{_f(y)}" for x, y in pts)
    area = f"0,{_f(h)} {line} {_f(w)},{_f(h)}"
    out = [f'<polygon points="{area}" fill="{T["yellow"]}"/>',
           f'<polyline points="{line}" fill="none" stroke="{T["ink"]}" stroke-width="3" stroke-linejoin="round"/>',
           f'<line x1="0" y1="{_f(h)}" x2="{_f(w)}" y2="{_f(h)}" stroke="{T["ink"]}" stroke-width="1.5"/>']
    for n, iso in d["milestones"].items():
        n = int(n)
        if n not in (5000, 17000):
            continue
        k = date.fromisoformat(iso[:10])
        x = (k - d0).days / span * w
        y = h - n / top * h
        out.append(f'<line x1="{_f(x)}" y1="{_f(y)}" x2="{_f(x)}" y2="{_f(h)}" stroke="{T["ink"]}" stroke-width="1" stroke-dasharray="3 4"/>')
        out.append(f'<rect x="{_f(x - 7)}" y="{_f(y - 7)}" width="14" height="14" fill="{T["paper"]}" stroke="{T["ink"]}" stroke-width="2.5"/>')
        lab = f"{n:,} · {k.strftime('%b').upper()} {k.day}"
        out.append(f'<text x="{_f(x - 14)}" y="{_f(y + 5)}" text-anchor="end" class="ct">{lab}</text>')
    # month ticks on the base line
    for m, name in ((7, "JUL"), (8, "AUG"), (9, "SEP"), (10, "OCT")):
        k = date(2026, m, 1)
        x = max(0.0, (k - d0).days / span * w)
        out.append(f'<text x="{_f(x)}" y="{_f(h + 22)}" class="cm">{name}</text>')
    return "".join(out)


CSS = """
@font-face { font-family: 'Big Shoulders Display'; font-weight: 100 900; src: url('%(display)s') format('truetype'); }
@font-face { font-family: 'JetBrains Mono'; font-weight: 100 800; src: url('%(mono)s') format('truetype'); }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: %(paper)s; }
.card { position: relative; overflow: hidden; width: %(W)spx; height: %(H)spx; color: %(ink)s;
        background-color: %(paper)s;
        background-image: linear-gradient(%(grid)s 1px, transparent 1px), linear-gradient(90deg, %(grid)s 1px, transparent 1px);
        background-size: 24px 24px; }
.mono { font-family: 'JetBrains Mono', monospace; letter-spacing: .12em; text-transform: uppercase; font-weight: 600; }
.disp { font-family: 'Big Shoulders Display', sans-serif; font-weight: 900; text-transform: uppercase; line-height: .86; }
.kicker { position: absolute; left: %(P)spx; top: %(P)spx; font-size: %(kfs)spx; display: flex; gap: 12px; align-items: center; }
.kicker i { width: 14px; height: 14px; background: %(yellow)s; outline: 1.5px solid %(ink)s; display: block; }
.hero { position: absolute; left: %(P)spx; top: %(htop)spx; }
.hero .n { font-size: %(nfs)spx; letter-spacing: -.005em; }
.hero .n span { background: linear-gradient(transparent 52%%, %(yellow)s 52%%, %(yellow)s 96%%, transparent 96%%); padding: 0 .05em; }
.hero .l { font-size: %(lfs)spx; margin-top: 22px; }
.hero .s { font-size: %(sfs)spx; color: %(ochre)s; margin-top: 12px; font-weight: 800; }
.chart { position: absolute; left: %(cx)spx; top: %(cy)spx; overflow: visible; }
.ct { font: 700 %(ctfs)spx 'JetBrains Mono', monospace; letter-spacing: .06em; fill: %(ink)s;
      paint-order: stroke; stroke: %(paper)s; stroke-width: 6px; stroke-linejoin: round; }
.cm { font: 600 %(cmfs)spx 'JetBrains Mono', monospace; letter-spacing: .1em; fill: %(mute)s; }
.stats { position: absolute; left: %(P)spx; right: %(P)spx; top: %(stop)spx; display: grid;
         grid-template-columns: %(cols)s; gap: 28px; }
.stat { border-top: 2px solid %(ink)s; padding-top: 12px; }
.stat .v { font-size: %(vfs)spx; }
.stat .v.hl span { background: %(yellow)s; padding: 0 .08em; }
.stat .k { font-size: %(kkfs)spx; margin-top: 8px; color: %(ink)s; line-height: 1.35; }
.foot { position: absolute; left: %(P)spx; right: %(P)spx; bottom: %(fb)spx; display: flex; font-size: %(ffs)spx; color: %(mute)s; }
.foot b { color: %(ink)s; }
.foot .r { margin-left: auto; }
"""


def layout(kind: str, W: int, H: int) -> dict:
    if kind == "hero":
        return dict(P=56, kfs=15, htop=100, nfs=190, lfs=16, sfs=40, cx=780, cy=96, cw=756, ch=250,
                    ctfs=15, cmfs=13, stop=402, vfs=72, kkfs=13, ffs=14, fb=30,
                    cols="1fr 1.25fr 1.6fr")
    # og, and the thumbnail (rendered at og size, downscaled by covers.py)
    return dict(P=48, kfs=14, htop=92, nfs=170, lfs=15, sfs=34, cx=620, cy=110, cw=532, ch=210,
                ctfs=13, cmfs=12, stop=398, vfs=66, kkfs=12, ffs=13, fb=26,
                cols="1fr 1.25fr 1.6fr")


def page(post: dict, kind: str, W: int, H: int, fonts: dict) -> str:
    L = layout(kind, W, H)
    e = html.escape
    stars = int(post["stars"])
    css = CSS % {**T, **L, **fonts, "W": W, "H": H}
    chart = (f'<svg class="chart" width="{L["cw"]}" height="{L["ch"] + 26}" overflow="visible" '
             f'xmlns="http://www.w3.org/2000/svg">{curve(L["cw"], L["ch"], stars)}</svg>')
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{css}</style></head><body>
<div class="card">
<div class="kicker mono"><i></i><span>XERJ · MILESTONE · {e(post["date"])}</span></div>
<div class="hero">
 <div class="n disp"><span>{stars:,}</span></div>
 <div class="l mono">GitHub stars</div>
 <div class="s disp">5,000 to 17,000 stars in 12 days</div>
</div>
{chart}
<div class="stats">
 <div class="stat"><div class="v disp">100</div><div class="k mono">contributors<br>since July</div></div>
 <div class="stat"><div class="v disp">7,226</div><div class="k mono">Corpus Hub<br>contributors</div></div>
 <div class="stat"><div class="v disp hl"><span>#1</span></div><div class="k mono">Rust repo of the day<br>and week on Trendshift</div></div>
</div>
<div class="foot mono"><span><b>xerj.org/blog/{e(post["slug"])}</b></span><span class="r">The search engine for AI agents</span></div>
</div></body></html>"""
