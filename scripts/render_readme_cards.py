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
PAPER, INK, MUTED, LINE = "#0B111C", "#E6EDF6", "#8795AA", "#1E2A3E"
BLUE, RED, YELLOW = "#4C9AFF", "#F0746B", "#E3B341"
BAR_IDLE = "#2B384D"
GRAPH = ["#151F30", "#1B3A66", "#2563B0", "#3D8BEB", "#8CC4FF"]
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


def save(name, body, w, h, defs="", under=""):
    style = f"<style>{FONTS}{'' if STATIC else ANIM}</style>"
    clip = f'<clipPath id="card"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="20"/></clipPath>' if under else ""
    layer = f'<g clip-path="url(#card)">{under}</g>' if under else ""
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
           f'<defs>{style}{defs}{clip}</defs>'
           f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="20" fill="{PAPER}"/>{layer}'
           f'{body}'
           f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="20" fill="none" stroke="{LINE}"/></svg>')
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


def sphere_frames(cx, cy, r, n_nodes=34, frames=36, tilt=0.38):
    """Real 3D: nodes on a Fibonacci sphere, linked to their nearest neighbours, rotated about Y
    and projected with perspective. Returns per-frame screen coords and depth for SMIL playback."""
    import math
    ga = math.pi * (3 - math.sqrt(5))
    pts = []
    for i in range(n_nodes):
        y = 1 - 2 * (i + .5) / n_nodes
        rr = math.sqrt(1 - y * y)
        pts.append((math.cos(ga * i) * rr, y, math.sin(ga * i) * rr))
    edges = set()
    for i, a in enumerate(pts):
        near = sorted(range(n_nodes), key=lambda j: sum((a[k] - pts[j][k]) ** 2 for k in range(3)))[1:4]
        for j in near:
            edges.add((min(i, j), max(i, j)))
    edges = sorted(edges)
    ct, st = math.cos(tilt), math.sin(tilt)
    cam = 3.2

    def project(p, th):
        x, y, z = p
        x, z = x * math.cos(th) + z * math.sin(th), -x * math.sin(th) + z * math.cos(th)
        y, z = y * ct - z * st, y * st + z * ct
        k = cam / (cam - z)
        return cx + x * r * k, cy + y * r * k, z

    out = []
    for f in range(frames + 1):
        th = 2 * math.pi * f / frames
        out.append([project(p, th) for p in pts])
    return edges, out


def vals(items):
    return ";".join(items)


def hero():
    rows = (ROOT / "assets" / "portrait.txt").read_text().rstrip("\n").split("\n")
    fs, lh = 5.6, 5.9
    pw = 76 * fs * 0.6
    W, H = 1000, 420
    px = W - 48 - pw
    py = (H - len(rows) * lh) / 2 + 6
    art = []
    for i, line in enumerate(rows):
        art.append(f'<text xml:space="preserve" x="{px:.1f}" y="{py + i * lh:.1f}"'
                   f'{cls("row", 0.2 + i * 0.018)} font-family="{MONO}" font-size="{fs}" fill="#A9C8F5">{esc(line)}</text>')

    scx, scy, sr = 792, 200, 158
    hz = 262                       # horizon of the perspective floor
    F = H - hz                     # nearest floor line lands on the bottom edge

    # perspective floor: static radial lines + horizontal lines gliding toward the viewer
    floor = []
    for k in range(-14, 15):
        floor.append(f'<line x1="{W/2}" y1="{hz}" x2="{W/2 + k * 150}" y2="{H + 40}" stroke="{BLUE}" stroke-opacity=".28" stroke-width="1"/>')
    n_lines, steps = 9, 12
    for k in range(n_lines):
        ds = [k + 1 - t / steps for t in range(steps + 1)]
        ys = [hz + F / max(d, 0.35) for d in ds]
        ops = [max(0.0, min(.55, .62 - (d - 1) * .07)) * (1 if k else min(1, (d - .35) / .65)) for d in ds]
        if k == n_lines - 1:   # newest far line fades in
            ops = [o * (t / steps) for t, o in enumerate(ops)]
        rect = f'<rect x="0" y="{ys[0]:.1f}" width="{W}" height="1.2" fill="{BLUE}" fill-opacity="{ops[0]:.2f}"'
        if STATIC:
            floor.append(rect + "/>")
        else:
            floor.append(
                rect + ">"
                f'<animate attributeName="y" dur="5s" repeatCount="indefinite" values="{vals(f"{v:.1f}" for v in ys)}"/>'
                f'<animate attributeName="fill-opacity" dur="5s" repeatCount="indefinite" values="{vals(f"{v:.2f}" for v in ops)}"/>'
                f'</rect>')

    # rotating 3D network sphere
    edges, fr = sphere_frames(scx, scy, sr)
    nf = range(len(fr))
    net = []
    for (i, j) in edges:
        def seg(f):
            a, b = fr[f][i], fr[f][j]
            return f'M{a[0]:.0f} {a[1]:.0f}L{b[0]:.0f} {b[1]:.0f}'

        def op(f):
            z = (fr[f][i][2] + fr[f][j][2]) / 2
            return .06 + .34 * (z + 1) / 2
        head = f'<path d="{seg(0)}" stroke="{BLUE}" stroke-opacity="{op(0):.2f}" stroke-width="1" fill="none"'
        if STATIC:
            net.append(head + "/>")
        else:
            net.append(
                head + ">"
                f'<animate attributeName="d" dur="48s" repeatCount="indefinite" values="{vals(seg(f) for f in nf)}"/>'
                f'<animate attributeName="stroke-opacity" dur="48s" repeatCount="indefinite" values="{vals(f"{op(f):.2f}" for f in nf)}"/>'
                f'</path>')
    for i in range(len(fr[0])):
        def rad(f):
            return 1.2 + 2.2 * (fr[f][i][2] + 1) / 2

        def nop(f):
            return .25 + .75 * (fr[f][i][2] + 1) / 2
        a = fr[0][i]
        head = f'<circle cx="{a[0]:.0f}" cy="{a[1]:.0f}" r="{rad(0):.1f}" fill="#9CCBFF" fill-opacity="{nop(0):.2f}"'
        if STATIC:
            net.append(head + "/>")
        else:
            net.append(
                head + ">"
                f'<animate attributeName="cx" dur="48s" repeatCount="indefinite" values="{vals(f"{fr[f][i][0]:.0f}" for f in nf)}"/>'
                f'<animate attributeName="cy" dur="48s" repeatCount="indefinite" values="{vals(f"{fr[f][i][1]:.0f}" for f in nf)}"/>'
                f'<animate attributeName="r" dur="48s" repeatCount="indefinite" values="{vals(f"{rad(f):.1f}" for f in nf)}"/>'
                f'<animate attributeName="fill-opacity" dur="48s" repeatCount="indefinite" values="{vals(f"{nop(f):.2f}" for f in nf)}"/>'
                f'</circle>')

    defs = (
        '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#070B14"/>'
        '<stop offset=".62" stop-color="#0E1A2E"/><stop offset="1" stop-color="#0B111C"/></linearGradient>'
        f'<radialGradient id="glow" cx="{scx}" cy="{scy}" r="300" gradientUnits="userSpaceOnUse">'
        '<stop offset="0" stop-color="#2F6FD6" stop-opacity=".42"/><stop offset=".55" stop-color="#2F6FD6" stop-opacity=".10"/>'
        '<stop offset="1" stop-color="#2F6FD6" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="horizon" x1="0" y1="{hz}" x2="0" y2="{hz + 70}" gradientUnits="userSpaceOnUse">'
        '<stop offset="0" stop-color="#0E1A2E"/><stop offset="1" stop-color="#0E1A2E" stop-opacity="0"/></linearGradient>'
        f'<radialGradient id="fadeArt" cx="{px + pw / 2:.0f}" cy="{H / 2}" r="{pw * .62:.0f}" gradientUnits="userSpaceOnUse">'
        '<stop offset=".55" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
        f'<mask id="artmask"><rect width="{W}" height="{H}" fill="url(#fadeArt)"/></mask>'
        '<linearGradient id="textfade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#070B14" stop-opacity=".85"/>'
        '<stop offset=".5" stop-color="#070B14" stop-opacity=".35"/><stop offset="1" stop-color="#070B14" stop-opacity="0"/></linearGradient>')
    if not STATIC:
        defs += (f'<linearGradient id="g" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="{INK}"/>'
                 f'<stop offset=".42" stop-color="{INK}"/><stop offset=".5" stop-color="{BLUE}"/>'
                 f'<stop offset=".58" stop-color="{INK}"/><stop offset="1" stop-color="{INK}"/>'
                 f'<animateTransform attributeName="gradientTransform" type="translate" from="-1 0" to="1 0" '
                 f'dur="6s" begin="2s" repeatCount="indefinite"/></linearGradient>')
    last = "url(#g)" if not STATIC else INK

    under = (
        f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
        f'<rect width="{W}" height="{H}" fill="url(#glow)"/>'
        f'{"".join(floor)}'
        f'<rect x="0" y="{hz}" width="{W}" height="70" fill="url(#horizon)"/>'
        f'<line x1="0" y1="{hz}" x2="{W}" y2="{hz}" stroke="{BLUE}" stroke-opacity=".35"/>'
        f'{"".join(net)}'
        f'<rect width="640" height="{H}" fill="url(#textfade)"/>')

    body = f'''
<text x="48" y="64" fill="{MUTED}" font-family="{MONO}" font-size="12" letter-spacing="3"{cls("rise", 0)}>HELLO, WORLD / PROFILE</text>
<text x="48" y="146" fill="{INK}" font-family="{SERIF}" font-size="76"{cls("rise", .15)}>Chetan</text>
<text x="48" y="220" fill="{last}" font-family="{SERIF}" font-size="76"{cls("rise", .3)}>Biranje</text>
<text x="50" y="270" fill="{INK}" font-family="{MONO}" font-size="14"{cls("rise", .5)}>Application security. Web and API VAPT.</text>
<text x="50" y="292" fill="{INK}" font-family="{MONO}" font-size="14"{cls("rise", .6)}>DevSecOps and security research.</text>
<text x="50" y="324" fill="{MUTED}" font-family="{MONO}" font-size="12"{cls("rise", .7)}>Pune, India</text>
<circle cx="56" cy="{H - 46}" r="4" fill="{BLUE}"{'' if STATIC else ' class="dot"'}/>
<text x="70" y="{H - 42}" fill="{INK}" font-family="{MONO}" font-size="12"{cls("rise", .8)}>Full-stack dev, security-focused, at AI4See</text>
<g mask="url(#artmask)" opacity=".92">{''.join(art)}</g>'''
    save("hero.svg", body, W, H, defs, under)


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
            f'<g clip-path="url(#c)"><rect class="shine" x="0" y="0" width="90" height="170" fill="#fff" opacity=".10" '
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
