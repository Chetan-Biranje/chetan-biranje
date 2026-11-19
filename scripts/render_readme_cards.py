#!/usr/bin/env python3
"""Render the animated SVG cards used by the profile README.

Input : data/contributions.json (written by fetch_contributions.py)
Output: cards/*.svg
Preview without animation: STATIC=1 python scripts/render_readme_cards.py
Use another data file:     DATA=path/to/file.json python scripts/render_readme_cards.py
Standard library only.
"""
import base64
import calendar
import html
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATIC = os.getenv("STATIC", "0") == "1"
PAPER, INK, MUTED, LINE = "#F5F1E8", "#242A30", "#77766F", "#D8D1C4"
BLUE, RED, YELLOW = "#245B9B", "#B94B43", "#D7A92E"
BAR_IDLE = "#B8B1A5"
GRAPH = ["#E6E0D5", "#C7D7E8", "#8EAFD1", "#4F83B6", BLUE]
SERIF = "'Instrument Serif', Georgia, serif"
MONO = "'Geist Mono', 'SFMono-Regular', Consolas, monospace"


def esc(s):
    return html.escape(str(s), quote=True)


def font_css():
    out = []
    for fam, fn, weight in [("Instrument Serif", "serif-400", 400),
                            ("Geist Mono", "mono-400", 400),
                            ("Geist Mono", "mono-500", 500)]:
        b64 = base64.b64encode((ROOT / "fonts" / f"{fn}.woff").read_bytes()).decode()
        out.append(f"@font-face{{font-family:'{fam}';font-weight:{weight};"
                   f"src:url(data:font/woff;base64,{b64}) format('woff')}}")
    return "".join(out)


FONTS = font_css()

ANIM = """
.rise{opacity:0;animation:rise .8s cubic-bezier(.2,.8,.2,1) forwards}
.row{opacity:0;animation:fade .35s ease-out forwards}
.bar{transform-box:fill-box;transform-origin:bottom;transform:scaleY(0);animation:grow .7s cubic-bezier(.2,.8,.2,1) forwards}
.pop{opacity:0;animation:fade .5s ease-out forwards}
.cell{opacity:0;transform-box:fill-box;transform-origin:center;transform:scale(.3);animation:cell .3s ease-out forwards}
.tile{opacity:0;transform-box:fill-box;transform-origin:50% 100%;animation:swing .9s cubic-bezier(.2,.9,.3,1.25) forwards}
.ring{transform-box:fill-box;transform-origin:center;opacity:0;animation:ring 2.8s ease-out infinite}
.nudge{animation:nudge 2.4s ease-in-out infinite}
.dot{animation:dot 2.2s ease-in-out infinite}
.shine{transform-box:fill-box;animation:sweep 6s ease-in-out infinite}
.rm{display:none}
@keyframes rise{from{opacity:0;transform:translateY(22px)}to{opacity:1;transform:none}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes grow{to{transform:scaleY(1)}}
@keyframes cell{to{opacity:1;transform:scale(1)}}
@keyframes swing{0%{opacity:0;transform:translateY(40px) rotate(-5deg)}100%{opacity:1;transform:none}}
@keyframes ring{0%{opacity:.6;transform:scale(.4)}100%{opacity:0;transform:scale(2.4)}}
@keyframes nudge{0%,100%{transform:translate(0,0)}50%{transform:translate(3px,-3px)}}
@keyframes dot{0%,100%{opacity:.35}50%{opacity:1}}
@keyframes sweep{0%,60%{transform:translateX(-120%)}90%,100%{transform:translateX(120%)}}
@media (prefers-reduced-motion:reduce){
 *{animation:none!important}
 .rise,.row,.pop,.cell,.tile{opacity:1!important;transform:none!important}
 .bar{transform:none!important}
 .ring,.shine{display:none}
 .cf{display:none}
 .rm{display:inline}
}
"""


def save(name, body, w, h, defs=""):
    style = f"<style>{FONTS}{'' if STATIC else ANIM}</style>"
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
           f'<defs>{style}{defs}</defs>'
           f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="20" fill="{PAPER}" stroke="{LINE}"/>'
           f'{body}</svg>')
    (ROOT / "cards").mkdir(exist_ok=True)
    (ROOT / "cards" / name).write_text(svg, encoding="utf-8")


def cls(c, delay):
    """CSS class + inline delay, or nothing in STATIC mode."""
    return "" if STATIC else f' class="{c}" style="animation-delay:{delay:.2f}s"'


def load():
    p = Path(os.getenv("DATA", ROOT / "data" / "contributions.json"))
    try:
        return json.loads(p.read_text())
    except Exception:
        return {}


def hero():
    rows = (ROOT / "assets" / "portrait.txt").read_text().rstrip("\n").split("\n")
    fs, lh = 5.6, 5.9
    pw = 76 * fs * 0.6
    px, py = 1000 - 48 - pw, 40
    art = []
    for i, line in enumerate(rows):
        art.append(f'<text xml:space="preserve" x="{px:.1f}" y="{py + i * lh:.1f}"'
                   f'{cls("row", 0.2 + i * 0.018)} font-family="{MONO}" font-size="{fs}" fill="{INK}">{esc(line)}</text>')
    h = int(py + len(rows) * lh + 24)
    shine = "" if STATIC else (
        f'<linearGradient id="g" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="{INK}"/>'
        f'<stop offset=".42" stop-color="{INK}"/><stop offset=".5" stop-color="{BLUE}"/>'
        f'<stop offset=".58" stop-color="{INK}"/><stop offset="1" stop-color="{INK}"/>'
        f'<animateTransform attributeName="gradientTransform" type="translate" from="-1 0" to="1 0" '
        f'dur="6s" begin="2s" repeatCount="indefinite"/></linearGradient>')
    last = "url(#g)" if not STATIC else INK
    body = f'''
<text x="48" y="58" fill="{MUTED}" font-family="{MONO}" font-size="12" letter-spacing="3"{cls("rise", 0)}>HELLO, WORLD / PROFILE</text>
<text x="48" y="140" fill="{INK}" font-family="{SERIF}" font-size="76"{cls("rise", .15)}>Chetan</text>
<text x="48" y="214" fill="{last}" font-family="{SERIF}" font-size="76"{cls("rise", .3)}>Biranje</text>
<text x="50" y="262" fill="{INK}" font-family="{MONO}" font-size="14"{cls("rise", .5)}>Application security. Web and API VAPT.</text>
<text x="50" y="284" fill="{INK}" font-family="{MONO}" font-size="14"{cls("rise", .6)}>DevSecOps and security research.</text>
<text x="50" y="316" fill="{MUTED}" font-family="{MONO}" font-size="12"{cls("rise", .7)}>Pune, India</text>
<circle cx="56" cy="{h-46}" r="4" fill="{BLUE}"{'' if STATIC else ' class="dot"'}/>
<text x="70" y="{h-42}" fill="{INK}" font-family="{MONO}" font-size="12"{cls("rise", .8)}>Full-stack dev, security-focused, at AI4See</text>
{''.join(art)}'''
    save("hero.svg", body, 1000, h, shine)


def count_text(x, y, n, t0, color, size):
    """Counts up with SMIL <set> frames. One text element per value; CSS cannot change text."""
    final = (f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" fill="{color}">{n}</text>')
    if STATIC:
        return final
    steps = min(n, 18) if n > 0 else 1
    vals = sorted({round(n * k / steps) for k in range(1, steps + 1)})
    frames = []
    for k, v in enumerate(vals):
        last = k == len(vals) - 1
        begin = t0 + k * 0.045
        fill = "freeze" if last else "remove"
        frames.append(f'<text class="cf" x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" fill="{color}" opacity="0">'
                      f'{v}<set attributeName="opacity" to="1" begin="{begin:.3f}s" dur="0.045s" fill="{fill}"/></text>')
    rm = final.replace("<text ", '<text class="rm" ', 1)
    return "".join(frames) + rm


def tiles(d):
    repos = int(d.get("repos", 21))
    stars = int(d.get("stars", 88))
    items = [
        ("build.svg", "BUILD", "Public repositories", BLUE, repos, "repos", "pentest tools and labs"),
        ("brand.svg", "BRAND", "Stars received", RED, stars, "stars", "across my projects"),
        ("learn.svg", "LEARN", "Certifications", YELLOW, 4, "courses", "AppSec, DevSecOps, SOC"),
    ]
    for i, (fn, title, sub, color, n, unit, note) in enumerate(items):
        t = 0.2 + i * 0.25
        shine = "" if STATIC else (
            f'<g clip-path="url(#c)"><rect class="shine" x="0" y="0" width="90" height="170" fill="#fff" opacity=".35" '
            f'transform="skewX(-18)" style="animation-delay:{3 + i * .8}s"/></g>')
        defs = f'<clipPath id="c"><rect x="2" y="2" width="316" height="166" rx="18"/></clipPath>'
        ring = "" if STATIC else f'<circle class="ring" cx="286" cy="38" r="14" fill="none" stroke="{color}" stroke-width="2" style="animation-delay:{t + .9}s"/>'
        body = f'''
<g{'' if STATIC else f' class="tile" style="animation-delay:{t:.2f}s"'}>
<rect x="2" y="2" width="316" height="166" rx="18" fill="{PAPER}" stroke="{color}" stroke-width="2"/>
<text x="24" y="38" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{MUTED}">{title}</text>
<circle cx="286" cy="38" r="6" fill="{color}"/>{ring}
{count_text(24, 112, n, t + .5, INK, 72)}
<text x="{24 + len(str(n)) * 32 + 8}" y="112" font-family="{MONO}" font-size="13" fill="{MUTED}">{unit}</text>
<text x="25" y="140" font-family="{MONO}" font-size="12" fill="{INK}">{esc(sub)}</text>
<text x="25" y="157" font-family="{MONO}" font-size="11" fill="{MUTED}">{esc(note)}</text>
<text x="284" y="152" font-family="{MONO}" font-size="20" fill="{color}"{'' if STATIC else ' class="nudge"'}>&#8599;</text>
{shine}</g>'''
        save(fn, body, 320, 172, defs)


def monthly(d):
    months = (d.get("months") or [])[-12:]
    total = int(d.get("total", 0))
    maxv = max([int(m["count"]) for m in months] + [1])
    best = max(range(len(months)), key=lambda i: months[i]["count"]) if months else -1
    bars = []
    for i, m in enumerate(months):
        c = int(m["count"])
        x = 48 + i * 56
        h = max(2.0, 100 * c / maxv)
        col = BLUE if i == best else BAR_IDLE
        mon = calendar.month_abbr[int(m["label"][5:7])].upper()
        bars.append(f'<rect x="{x}" y="{200 - h:.1f}" width="34" height="{h:.1f}" rx="5" fill="{col}"'
                    f'{cls("bar", .3 + i * .06)}><title>{mon}: {c}</title></rect>'
                    f'<text x="{x + 17}" y="220" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{MUTED}">{mon}</text>')
        if i == best:
            bars.append(f'<text x="{x + 17}" y="{192 - h:.1f}" text-anchor="middle" font-family="{SERIF}" font-size="22" fill="{BLUE}"'
                        f'{cls("pop", 1.3)}>{c}</text>')
    empty = f'<text x="48" y="140" font-family="{MONO}" font-size="13" fill="{MUTED}">Chart fills in after the first scheduled run.</text>'
    body = f'''
<text x="48" y="48" font-family="{SERIF}" font-size="34" fill="{INK}">Contributions by month</text>
<text x="48" y="72" font-family="{MONO}" font-size="12" fill="{MUTED}">{total:,} in the last year. {int(d.get("active_days", 0))} active days. Busiest weekday: {esc(d.get("busiest_day", "-"))}.</text>
{''.join(bars) or empty}
<text x="770" y="120" font-family="{SERIF}" font-size="56" fill="{BLUE}">{int(d.get("current_streak", 0))}</text>
<text x="770" y="142" font-family="{MONO}" font-size="11" letter-spacing="2" fill="{MUTED}">CURRENT STREAK</text>
<text x="770" y="190" font-family="{SERIF}" font-size="40" fill="{INK}">{int(d.get("longest_streak", 0))}</text>
<text x="770" y="212" font-family="{MONO}" font-size="11" letter-spacing="2" fill="{MUTED}">LONGEST STREAK</text>'''
    save("monthly.svg", body, 1000, 244)


def activity(d):
    weeks = (d.get("weeks") or [])[-53:]
    cells = []
    for wi, week in enumerate(weeks):
        for di, day in enumerate(week):
            lvl = max(0, min(4, int(day.get("level", 0))))
            cells.append(f'<rect x="{48 + wi * 17}" y="{84 + di * 16}" width="12" height="12" rx="2.5" fill="{GRAPH[lvl]}"'
                         f'{cls("cell", 1.5 + wi * .035)}><title>{esc(day["date"])}: {int(day.get("count", 0))}</title></rect>')
    empty = f'<text x="48" y="150" font-family="{MONO}" font-size="13" fill="{MUTED}">Graph fills in after the first scheduled run.</text>'
    body = f'''
<text x="48" y="44" font-family="{SERIF}" font-size="30" fill="{INK}">Contribution graph</text>
<text x="48" y="66" font-family="{MONO}" font-size="12" fill="{MUTED}">Daily activity, refreshed every morning.</text>
{''.join(cells) or empty}'''
    save("activity.svg", body, 1000, 208)


REPOS = [
    ("webapp-pentest-framework", "Web application penetration testing framework and tools"),
    ("web-rest-api-pentest-research", "Web and REST API pentest research and techniques"),
    ("offensive-security-skill-development", "Offensive security training materials and hands-on labs"),
]


def repos():
    for i, (name, desc) in enumerate(REPOS):
        body = f'''
<g{cls("rise", 2.4 + i * .2)}>
<text x="40" y="44" font-family="{SERIF}" font-size="28" fill="{INK}">{esc(name)}</text>
<text x="40" y="68" font-family="{MONO}" font-size="12" fill="{MUTED}">{esc(desc)}</text>
<text x="960" y="56" text-anchor="end" font-family="{MONO}" font-size="12" font-weight="500" fill="{BLUE}">OPEN &#8599;</text>
</g>'''
        save(f"repo-{i + 1}.svg", body, 1000, 92)


def main():
    d = load()
    hero()
    tiles(d)
    monthly(d)
    activity(d)
    repos()
    print("cards written:", len(list((ROOT / "cards").glob("*.svg"))))


if __name__ == "__main__":
    main()
