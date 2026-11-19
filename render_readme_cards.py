
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance
import json, os, html

ROOT = Path(__file__).resolve().parents[1]
STATIC = os.getenv("STATIC", "0") == "1"
PAPER, INK, MUTED = "#F5F1E8", "#242A30", "#77766F"
BLUE, RED, YELLOW = "#245B9B", "#B94B43", "#D7A92E"
SERIF = "Georgia, 'Times New Roman', serif"
MONO = "'SFMono-Regular', Consolas, monospace"

def esc(value):
    return html.escape(str(value), quote=True)

def save_svg(filename, body, width=1000, height=260):
    animation = ""
    if not STATIC:
        animation = """
        <style>
          .enter { opacity: 0; animation: rise .8s ease-out forwards; }
          .shine { animation: shine 5s ease-in-out infinite; }
          @keyframes rise { to { opacity: 1; transform: translateY(0); } }
          @keyframes shine { 0%,65% { transform: translateX(-140%); } 95%,100% { transform: translateX(140%); } }
          @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after { animation: none !important; opacity: 1 !important; transform: none !important; }
          }
        </style>
        """
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><rect width="100%" height="100%" rx="20" fill="{PAPER}"/>{animation}{body}</svg>'
    (ROOT / "cards" / filename).write_text(svg, encoding="utf-8")

def make_ascii_portrait():
    image = Image.open(ROOT / "assets" / "portrait.jpg").convert("L")
    image = ImageOps.fit(image, (68, 88))
    image = ImageEnhance.Contrast(image).enhance(1.35)
    alphabet = " .'`^,:;Il!i><~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    pixels = list(image.getdata())
    rows = []
    for y in range(image.height):
        values = pixels[y * image.width:(y + 1) * image.width]
        rows.append("".join(alphabet[min(len(alphabet)-1, int(v / 256 * len(alphabet)))] for v in values))
    return rows

def main():
    data_path = ROOT / "data" / "contributions.json"
    data = json.loads(data_path.read_text(encoding="utf-8"))
    portrait = "".join(
        f'<text x="0" y="{16 + i*2.25}" font-family="{MONO}" font-size="2.1" fill="{BLUE}">{esc(row)}</text>'
        for i, row in enumerate(make_ascii_portrait())
    )

    hero = f"""
      <text x="48" y="45" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{MUTED}">HELLO, WORLD / PROFILE README</text>
      <text x="48" y="118" font-family="{SERIF}" font-size="62" fill="{INK}">Chetan Biranje</text>
      <text x="52" y="157" font-family="{MONO}" font-size="14" fill="{INK}">Aspiring Researcher · Software Developer · Cybersecurity</text>
      <text x="52" y="190" font-family="{MONO}" font-size="12" fill="{MUTED}">Pune, India / Building, breaking, learning.</text>
      <g transform="translate(720,12) scale(1.12)">{portrait}</g>
    """
    save_svg("hero.svg", hero, 1000, 250)

    tiles = [
        ("build.svg", "BUILD", "Software, Python & projects", BLUE, "⌘"),
        ("brand.svg", "BRAND", "Ideas, writing & personal work", RED, "✳"),
        ("learn.svg", "LEARN", "Security research & learning", YELLOW, "↗"),
    ]
    for filename, title, subtitle, color, symbol in tiles:
        body = f"""
          <rect x="2" y="2" width="316" height="146" rx="17" fill="{PAPER}" stroke="{color}" stroke-width="2"/>
          <text x="22" y="35" font-family="{MONO}" font-size="11" fill="{MUTED}" letter-spacing="2">CHETAN / {title}</text>
          <text x="22" y="88" font-family="{SERIF}" font-size="40" fill="{INK}">{title}</text>
          <text x="22" y="117" font-family="{MONO}" font-size="10" fill="{MUTED}">{subtitle}</text>
          <text x="276" y="84" font-size="28" fill="{color}">{symbol}</text>
        """
        save_svg(filename, body, 320, 150)

    months = data.get("months", [])[-12:]
    maximum = max([int(item.get("count", 0)) for item in months] + [1])
    bars = ""
    for index, item in enumerate(months):
        count = int(item.get("count", 0))
        bar_height = 95 * count / maximum
        x = 45 + index * 70
        color = BLUE if count == maximum else "#B8B1A5"
        bars += f'<rect x="{x}" y="{175-bar_height:.1f}" width="32" height="{bar_height:.1f}" rx="4" fill="{color}"/>'
        bars += f'<text x="{x+16}" y="198" text-anchor="middle" font-family="{MONO}" font-size="9" fill="{MUTED}">{esc(str(item.get("label", ""))[-3:])}</text>'

    monthly = f"""
      <text x="36" y="38" font-family="{SERIF}" font-size="28" fill="{INK}">A year in contributions</text>
      <text x="38" y="61" font-family="{MONO}" font-size="11" fill="{MUTED}">{int(data.get("total",0))} contributions · {int(data.get("active_days",0))} active days · busiest: {esc(data.get("busiest_day","—"))}</text>
      {bars if bars else '<text x="42" y="130" font-family="monospace" font-size="13" fill="#77766F">Chart populates after the first GitHub Actions run.</text>'}
      <text x="825" y="120" font-family="{SERIF}" font-size="36" fill="{BLUE}">{int(data.get("current_streak",0))}</text>
      <text x="825" y="140" font-family="{MONO}" font-size="10" fill="{MUTED}">CURRENT STREAK</text>
      <text x="825" y="178" font-family="{SERIF}" font-size="25" fill="{INK}">{int(data.get("longest_streak",0))}</text>
      <text x="825" y="196" font-family="{MONO}" font-size="10" fill="{MUTED}">LONGEST STREAK</text>
    """
    save_svg("monthly.svg", monthly, 1000, 230)

    weeks = data.get("weeks", [])
    cells = ""
    palette = ["#E6E0D5", "#C7D7E8", "#8EAFD1", "#4F83B6", BLUE]
    for week_index, week in enumerate(weeks[-53:]):
        for day_index, day in enumerate(week):
            level = max(0, min(4, int(day.get("level", 0))))
            cells += f'<rect x="{35+week_index*16}" y="{64+day_index*16}" width="11" height="11" rx="2" fill="{palette[level]}"><title>{esc(day.get("date",""))}: {int(day.get("count",0))}</title></rect>'
    activity = f"""
      <text x="35" y="36" font-family="{SERIF}" font-size="27" fill="{INK}">The contribution graph</text>
      {cells if cells else '<text x="40" y="100" font-family="monospace" font-size="13" fill="#77766F">Contribution grid appears after the scheduled update.</text>'}
    """
    save_svg("activity.svg", activity, 1000, 190)

    repos = [
        ("Featured project 01", "Replace with your actual repository name and description", "repo-1.svg"),
        ("Featured project 02", "Replace with your actual repository name and description", "repo-2.svg"),
        ("Featured project 03", "Replace with your actual repository name and description", "repo-3.svg"),
    ]
    for title, description, filename in repos:
        body = f"""
          <text x="35" y="38" font-family="{SERIF}" font-size="27" fill="{INK}">Featured work</text>
          <rect x="35" y="58" width="930" height="64" rx="12" fill="#EEE9DF"/>
          <text x="58" y="85" font-family="{SERIF}" font-size="20" fill="{INK}">{title}</text>
          <text x="58" y="105" font-family="{MONO}" font-size="11" fill="{MUTED}">{description}</text>
        """
        save_svg(filename, body, 1000, 150)

if __name__ == "__main__":
    main()
