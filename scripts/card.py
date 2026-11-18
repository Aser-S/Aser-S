"""Generate the neofetch-style profile card (assets/neofetch-dark.svg / -light.svg).

Runs daily from .github/workflows/card.yml so the uptime (age) and IDE versions stay current.
Pure standard library, no network access: the workflow looks up the latest IDE versions
and passes them in as VSCODE_VERSION / PYCHARM_VERSION.
"""
import datetime as dt
import os
import random
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIRTHDAY = dt.date(2004, 6, 10)
COLS = 48
INFO_W = 56

# Lines of code across my repos (GitHub contributor stats, includes private repos)
LOC_ADD, LOC_DEL = 2_975_520, 1_797_204


# ---------------------------------------------------------------- live data
def age(today=None):
    today = today or dt.date.today()
    y, m, d = today.year - BIRTHDAY.year, today.month - BIRTHDAY.month, today.day - BIRTHDAY.day
    if d < 0:
        m -= 1
        d += (today.replace(day=1) - dt.timedelta(days=1)).day
    if m < 0:
        y -= 1
        m += 12
    plural = lambda n, w: f"{n} {w}" + ("" if n == 1 else "s")
    return f"{plural(y, 'year')}, {plural(m, 'month')}, {plural(d, 'day')}"


def ide_versions():
    vscode = os.environ.get("VSCODE_VERSION") or "1.147"
    pycharm = os.environ.get("PYCHARM_VERSION") or "2026.3"
    vscode = ".".join(vscode.split(".")[:2])
    return f"VS Code {vscode}, PyCharm {pycharm}"


# ---------------------------------------------------------------- info rows
# a row is a list of (text, css-class) segments
def kv(key, val, width=INFO_W, lead=". "):
    dots = width - len(lead) - len(key) - 1 - len(val) - 2
    return [(lead, "dim"), (key + ":", "key"), (" " + "." * max(dots, 1) + " ", "dim"), (val, "val")]


def kv2(lk, lv, rk, rv):
    return kv(lk, lv, width=29) + [(" | ", "dim")] + kv(rk, rv, width=24, lead="")


def header(title):
    return [(title + " ", "title"), ("-" * (INFO_W - len(title) - 1), "dim")]


def blank():
    return [(". ", "dim")]


def info_rows():
    phone = kv("Phone", "[CLASSIFIED]")[:-1] + [("[CLASSIFIED]", "classified")]
    return [
        header("aser@sherif"),
        kv("OS", "Windows 11"),
        kv("Uptime", age()),
        kv("Host", "Ain Shams University"),
        kv("Kernel", "AI Engineer"),
        kv("IDE", ide_versions()),
        blank(),
        kv("Languages.Programming", "Python, Java, JavaScript, C++"),
        kv("Languages.Real", "English, Arabic"),
        blank(),
        header("- AI Stack"),
        kv("Deep Learning", "PyTorch, TensorFlow, Hugging Face"),
        kv("Classical ML", "scikit-learn, XGBoost, Pandas, NumPy"),
        kv("LLMs", "LangChain, RAG, OpenAI API, Ollama"),
        kv("NLP", "NLTK, spaCy, Transformers"),
        kv("Vision", "OpenCV, CNNs, transfer learning"),
        kv("Shipping", "FastAPI, Docker, Streamlit, Next.js"),
        blank(),
        header("- Contact"),
        kv("Email", "asersherif2004" + "@" + "gmail.com"),
        kv("LinkedIn", "asersherif"),
        phone,
        blank(),
        header("- Runtime Stats"),
        kv("Lines of Code", f"{LOC_ADD:,}++, {LOC_DEL:,}--")[:-1] +
        [(f"{LOC_ADD:,}++", "add"), (", ", "dim"), (f"{LOC_DEL:,}--", "del")],
        kv2("Bugs fixed", "∞", "Bugs made", "∞+1"),
        kv2("GPU", "borrowed", "Sleep", "404 Not Found"),
        kv("Fueled by", "ChatGPT + Claude"),
        blank(),
    ]


# ---------------------------------------------------------------- visuals
THEMES = {
    # dark matches github.com dark mode (#0d1117); light matches the white site
    "dark": {"bg": "#0d1117", "art": "#e6edf3", "key": "#79c0ff", "val": "#e6edf3", "dim": "#2f4a6b", "title": "#a5d6ff",
             "add": "#56d364", "del": "#ff7b72", "redact": "#2f4a6b", "classified": "#ff7b72",
             "rain": "#388bfd", "rainhead": "#e6edf3", "rainop": .40,
             "edge": "#58a6ff", "edgeop": .30, "pulse": "#cae8ff", "node": "#58a6ff", "nodefill": "#0d1117",
             "bar": "#79c0ff", "barbg": "#162a45", "panel": .82},
    "light": {"bg": "#ffffff", "art": "#1f2328", "key": "#0969da", "val": "#1f2328", "dim": "#a8c7ea", "title": "#0550ae",
              "add": "#1a7f37", "del": "#cf222e", "redact": "#a8c7ea", "classified": "#cf222e",
              "rain": "#54aeff", "rainhead": "#0550ae", "rainop": .30,
              "edge": "#0969da", "edgeop": .28, "pulse": "#218bff", "node": "#0969da", "nodefill": "#ffffff",
              "bar": "#218bff", "barbg": "#ddf4ff", "panel": .85},
}

RAIN_CHARS = "01θλσΣ∂∇πμ∑αβ0123456789.·"

# forward pass that rebuilds me in the digital world (a la VisionQuest)
LAYERS = [
    (3, "input", "loading memories.zip"),
    (5, "embed", "attaching feelings..."),
    (6, "conv", "mapping his mind"),
    (6, "attention", "syncing the mind stone"),
    (5, "mlp", "becoming self-aware"),
    (2, "output", "I am Aser."),
]


def rain(width, height, lh, t, seed=4):
    rnd = random.Random(seed)
    out = [f'<g opacity="{t["rainop"]}">']
    x = 6
    while x < width - 6:
        n = rnd.randint(6, 16)
        dur = rnd.uniform(7, 14)
        delay = -rnd.uniform(0, dur)
        col = "".join(f'<tspan x="{x}" y="{i*lh}"' + (f' fill="{t["rainhead"]}"' if i == n - 1 else "") +
                      f'>{escape(rnd.choice("aser") if i == n - 1 else rnd.choice(RAIN_CHARS))}</tspan>' for i in range(n))
        out.append(f'<g style="animation:rn{height + n*lh} {dur:.1f}s linear {delay:.1f}s infinite">'
                   f'<text fill="{t["rain"]}" transform="translate(0,{-n*lh})">{col}</text></g>')
        x += rnd.choice([21, 29, 38, 46])
    out.append('</g>')
    return out


def wrap2(text):
    """Split a title into two balanced lines at a space."""
    words = text.split()
    if len(words) < 2:
        return [text]
    best = min(range(1, len(words)),
               key=lambda i: abs(len(" ".join(words[:i])) - len(" ".join(words[i:]))))
    return [" ".join(words[:best]), " ".join(words[best:])]


def network(x0, y0, w, h, t, T, seed=9):
    rnd = random.Random(seed)
    n_layers = len(LAYERS)
    xs = [x0 + 70 + i * (w - 140) / (n_layers - 1) for i in range(n_layers)]
    top, bot = y0 + 14, y0 + h - 56
    nodes = [[(xs[li], top + (bot - top) * (j + .5) / n) for j in range(n)] for li, (n, _, _) in enumerate(LAYERS)]
    period = 3.2
    out = [f'<g stroke="{t["edge"]}" stroke-width="1" opacity="{t["edgeop"]}">']
    edges = []
    for li in range(n_layers - 1):
        for a in nodes[li]:
            for b in nodes[li + 1]:
                edges.append((li, a, b))
                out.append(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}"/>')
    out.append('</g>')
    out.append(f'<g stroke="{t["pulse"]}" stroke-width="2.2" stroke-linecap="round" fill="none">')
    for (li, a, b) in rnd.sample(edges, 40):
        delay = li * period / (n_layers - 1) * .9 + rnd.uniform(0, .25)
        out.append(f'<line class="p-{T}" pathLength="100" stroke-dasharray="8 100" style="animation-delay:{delay:.2f}s" '
                   f'x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}"/>')
    out.append('</g>')
    out.append(f'<g fill="{t["nodefill"]}" stroke="{t["node"]}" stroke-width="1.6">')
    for li, layer in enumerate(nodes):
        for (x, y) in layer:
            d = li * period / (n_layers - 1) * .9 + .3 + rnd.uniform(0, .2)
            out.append(f'<circle class="n-{T}" style="animation-delay:{d:.2f}s" cx="{x:.0f}" cy="{y:.0f}" r="5"/>')
    out.append('</g>')
    for li, (_, name, joke) in enumerate(LAYERS):
        lines = wrap2(joke)
        y_first = y0 + h - 12 - 15 * (len(lines) - 1)
        out.append(f'<text class="{T}-val" text-anchor="middle" font-size="12px">' +
                   "".join(f'<tspan x="{xs[li]:.0f}" y="{y_first + 15*k}">{escape(s)}</tspan>' for k, s in enumerate(lines)) +
                   '</text>')
    return out


def svg(art, rows, theme):
    t, T = THEMES[theme], theme
    fs, lh, cw = 14, 18, 8.43
    ix = int(30 + COLS * cw + 30)
    n_info = len(rows) + 2          # + prompt line + training bar
    n = max(len(art), n_info) + 1
    width = int(ix + INFO_W * cw + 30)
    base_h = n * lh + 50
    band_h = 175
    height = base_h + band_h
    off_art = 25 + max(0, (n_info - len(art)) // 2) * lh
    off_info = 25 + max(0, (len(art) - n_info) // 2) * lh
    colors = "".join(f'.{T}-{k}{{fill:{t[k]}}}' for k in ("key", "val", "dim", "title", "add", "del", "redact", "classified"))
    style = (
        colors + 'text,tspan{white-space:pre}'
        '.cur{animation:bl 1s steps(1,end) infinite}@keyframes bl{50%{opacity:0}}'
        + "".join(f'@keyframes rn{height + k*lh}{{from{{transform:translateY(0)}}to{{transform:translateY({height + k*lh}px)}}}}' for k in range(6, 17)) +
        f'.p-{T}{{animation:pl{T} 3.2s linear infinite;stroke-dashoffset:106}}'
        f'@keyframes pl{T}{{0%{{stroke-dashoffset:106;opacity:1}}45%{{stroke-dashoffset:0;opacity:1}}46%,100%{{stroke-dashoffset:0;opacity:0}}}}'
        f'.n-{T}{{animation:nf{T} 3.2s ease-out infinite}}'
        f'@keyframes nf{T}{{0%,100%{{opacity:.6;fill:{t["nodefill"]}}}10%{{opacity:1;fill:{t["pulse"]}}}28%{{opacity:.6;fill:{t["nodefill"]}}}}}'
        f'.bar-{T}{{animation:br{T} 5s linear infinite;transform-box:fill-box;transform-origin:left}}'
        f'@keyframes br{T}{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}'
        f'.ls-{T}{{animation:ls{T} 5s steps(1,end) infinite;opacity:0}}'
        f'@keyframes ls{T}{{0%{{opacity:1}}20%,100%{{opacity:0}}}}'
    )
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
           f'font-family="ConsolasFallback,Consolas,\'Courier New\',monospace" font-size="{fs}px">',
           '<title>Aser Sherif - AI Engineer neofetch card</title>',
           f'<style>{style}</style>',
           f'<defs><clipPath id="card-{T}"><rect width="{width}" height="{height}" rx="15"/></clipPath></defs>',
           f'<g clip-path="url(#card-{T})">',
           f'<rect width="{width}" height="{height}" fill="{t["bg"]}"/>']
    out += rain(width, height, lh, t)
    out.append(f'<line x1="30" y1="{base_h - 8}" x2="{width-30}" y2="{base_h - 8}" stroke="{t["dim"]}" stroke-dasharray="2 6"/>')
    out += network(30, base_h + 10, width - 60, band_h - 16, t, T)
    out.append(f'<rect x="{ix-12}" y="{off_info-18}" width="{INFO_W*cw+24:.0f}" height="{n_info*lh+12}" rx="8" fill="{t["bg"]}" opacity="{t["panel"]}"/>')
    out.append(f'<text x="30" y="{off_art}" fill="{t["art"]}">')
    for i, line in enumerate(art):
        out.append(f'<tspan x="30" y="{off_art + i*lh}">{escape(line)}</tspan>')
    out.append('</text>')
    out.append(f'<text x="{ix}" y="{off_info}">')
    for i, segs in enumerate(rows):
        out.append(f'<tspan x="{ix}" y="{off_info + i*lh}">' +
                   "".join(f'<tspan class="{T}-{cls}">{escape(txt)}</tspan>' for txt, cls in segs) + '</tspan>')
    out.append('</text>')
    # prompt first, then the training bar
    y = off_info + len(rows) * lh
    out.append(f'<text x="{ix}" y="{y}"><tspan class="{T}-key">aser@sherif</tspan><tspan class="{T}-dim">:</tspan>'
               f'<tspan class="{T}-val">~</tspan><tspan class="{T}-dim">$ </tspan><tspan class="{T}-title">python train.py</tspan></text>')
    y += lh
    out.append(f'<text x="{ix}" y="{y}"><tspan class="{T}-dim">. </tspan><tspan class="{T}-key">Training:</tspan></text>')
    bx, bw, bh = ix + 12 * cw, 22 * cw, 9
    out.append(f'<rect x="{bx:.0f}" y="{y-bh}" width="{bw:.0f}" height="{bh}" rx="2" fill="{t["barbg"]}"/>')
    out.append(f'<rect class="bar-{T}" x="{bx:.0f}" y="{y-bh}" width="{bw:.0f}" height="{bh}" rx="2" fill="{t["bar"]}"/>')
    lx = bx + bw + 2 * cw
    out.append(f'<text x="{lx:.0f}" y="{y}" class="{T}-dim">loss</text>')
    for i, v in enumerate(["0.693", "0.412", "0.218", "0.097", "0.042"]):
        out.append(f'<text class="ls-{T} {T}-val" style="animation-delay:{-((5 - i) % 5)}s" x="{lx + 5*cw:.0f}" y="{y}">{v}</text>')
    out.append('</g></svg>')
    return "\n".join(out)


def main():
    art = open(os.path.join(ROOT, "assets", "ascii.txt"), encoding="utf8").read().rstrip("\n").split("\n")
    rows = info_rows()
    for theme in THEMES:
        with open(os.path.join(ROOT, "assets", f"neofetch-{theme}.svg"), "w", encoding="utf8", newline="\n") as f:
            f.write(svg(art, rows, theme))
    print("card updated:", age())


if __name__ == "__main__":
    main()
