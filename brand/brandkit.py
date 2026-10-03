"""ABADE brand kit for README assets: header, KPI strip, case arc, charts, method track, portfolio map.

All text is outlined Lato (fontTools), so every SVG renders identically on GitHub, with light and dark
variants for <picture>. Charts follow Storytelling with Data: action title, neutrals first, one
highlighted series, direct labels, no gridlines or legends where a label can do the job.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONTS = Path.home() / ".local/share/fonts"
HERE = Path(__file__).resolve().parent
_sym = (HERE / "symbol_path.txt").read_text().split("\n", 1)
SYM_W, SYM_D = float(_sym[0]), _sym[1]  # symbol path normalised to height 100

CARBON, IVORY, GRAPHITE, STEEL = "#050505", "#F6F5F0", "#1B1C1F", "#7E8791"
COBALT, AURUM, POSITIVE, ATTENTION, RISK = "#5B6CFF", "#C8B680", "#52D6A5", "#E6B85C", "#E06A6A"


def theme(dark: bool) -> dict:
    if dark:
        return dict(bg=CARBON, fg=IVORY, sub="#9BA2AA", muted="#3A3E46", card=GRAPHITE, line="#2C2F35", on_accent="#FFFFFF")
    return dict(bg=IVORY, fg=CARBON, sub="#5C646D", muted="#C5CAD0", card="#FFFFFF", line="#E2E0D8", on_accent="#FFFFFF")


@lru_cache(None)
def _font(weight: str):
    f = TTFont(FONTS / f"Lato-{weight}.ttf")
    return f, f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm


def width(text: str, size: float, weight: str = "Regular", tracking: float = 0) -> float:
    _, gs, cmap, upm = _font(weight)
    w = sum(gs[cmap[ord(c)]].width for c in text if ord(c) in cmap) * size / upm
    return w + tracking * max(len(text) - 1, 0)


def text(s: str, x: float, y: float, size: float, fill: str, weight: str = "Regular",
         tracking: float = 0, anchor: str = "start", opacity: float = 1) -> str:
    if anchor != "start":
        w = width(s, size, weight, tracking)
        x -= w if anchor == "end" else w / 2
    _, gs, cmap, upm = _font(weight)
    k, cur, out = size / upm, x, []
    for ch in s:
        name = cmap.get(ord(ch))
        if name is None:
            continue
        gid = f"{weight}-{name}".replace(".", "_")
        if gid not in _GLYPHS:
            pen = SVGPathPen(gs)
            gs[name].draw(pen)
            _GLYPHS[gid] = pen.getCommands()
        if _GLYPHS[gid]:
            out.append(f'<use xlink:href="#{gid}" transform="translate({cur:.1f} {y:.1f}) scale({k:.5f} {-k:.5f})"/>')
        cur += gs[name].width * k + tracking
    op = f' fill-opacity="{opacity}"' if opacity < 1 else ""
    return f'<g fill="{fill}"{op}>{"".join(out)}</g>'


_GLYPHS: dict[str, str] = {}


def wrap(s: str, size: float, maxw: float, weight: str = "Regular") -> list[str]:
    lines, cur = [], ""
    for word in s.split():
        trial = f"{cur} {word}".strip()
        if width(trial, size, weight) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    return lines + [cur] if cur else lines


def symbol(x: float, y: float, h: float, fill: str) -> str:
    k = h / 100
    return f'<path transform="translate({x:.1f} {y:.1f}) scale({k:.4f})" d="{SYM_D}" fill="{fill}" fill-rule="evenodd"/>'


def svg(w: int, h: int, body: str, label: str, bg: str | None = None, pad: int = 0) -> str:
    """pad > 0 draws a rounded background panel, so the asset reads on any page colour."""
    if pad:
        body = f'<g transform="translate({pad} {pad})">{body}</g>'
        w, h = w + 2 * pad, h + 2 * pad
    rect = f'<rect width="{w}" height="{h}" rx="{24 if pad else 0}" fill="{bg}"/>' if bg else ""
    defs = "".join(f'<path id="{g}" d="{d}"/>' for g, d in _GLYPHS.items())
    _GLYPHS.clear()
    defs = f"<defs>{defs}</defs>" if defs else ""
    lab = label.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{lab}">{defs}{rect}{body}</svg>\n')


def arrow(x1: float, y: float, x2: float, color: str, sw: float = 3) -> str:
    return (f'<path d="M{x1} {y} H{x2}" stroke="{color}" stroke-width="{sw}" fill="none" stroke-linecap="round"/>'
            f'<path d="M{x2 - 12} {y - 9} L{x2} {y} L{x2 - 12} {y + 9}" stroke="{color}" stroke-width="{sw}" '
            f'fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


# ---------------------------------------------------------------- header
def header(dark: bool, eyebrow: str, title: str, tagline: str) -> str:
    t = theme(dark)
    W, H = 1600, 380
    hair = "".join(f'<path d="M{760 + i * 64} {H} L{1000 + i * 64} 0" stroke="{t["fg"]}" stroke-opacity="0.05"/>' for i in range(16))
    size = 76
    while width(title, size, "Black") > 1130 and size > 40:
        size -= 2
    lines = wrap(tagline, 30, 1150)[:2]
    body = [hair, symbol(80, 118, 132, t["fg"]),
            text(eyebrow.upper(), 330, 112, 18, COBALT, "Bold", tracking=4),
            text(title, 330, 196, size, t["fg"], "Black")]
    for i, ln in enumerate(lines):
        body.append(text(ln, 330, 254 + i * 40, 30, t["sub"]))
    yb = 254 + len(lines) * 40 + 2
    body.append(f'<rect x="330" y="{yb}" width="96" height="5" rx="2.5" fill="{COBALT}"/>')
    body.append(text("ABADE  ·  STRATEGY  ·  DATA  ·  GROWTH", 1520, H - 36, 13, t["sub"], "Bold", tracking=5, anchor="end"))
    return svg(W, H, "".join(body), f"{title}: {tagline}", t["bg"])


# ---------------------------------------------------------------- KPI strip
def kpis(dark: bool, items: list[tuple[str, str, str]]) -> str:
    """items: (label, value, note). The first value carries the accent: one highlight per composition."""
    t = theme(dark)
    W, gap, n = 1200, 24, len(items)
    tw = (W - gap * (n - 1)) / n
    notes = [wrap(note, 19, tw - 72)[:3] for _, _, note in items]
    H = 196 + max(len(x) for x in notes) * 27
    body = []
    for i, ((label, value, _), nl) in enumerate(zip(items, notes)):
        x = i * (tw + gap)
        stroke = f' stroke="{t["line"]}"' if not dark else ""
        body.append(f'<rect x="{x + 1}" y="1" width="{tw - 2}" height="{H - 2}" rx="22" fill="{t["card"]}"{stroke}/>')
        body.append(text(label.upper(), x + 36, 56, 14, t["sub"], "Bold", tracking=3))
        vs = 60
        while width(value, vs, "Black") > tw - 72:
            vs -= 2
        body.append(text(value, x + 36, 134, vs, COBALT if i == 0 else t["fg"], "Black"))
        for j, ln in enumerate(nl):
            body.append(text(ln, x + 36, 178 + j * 27, 19, t["sub"]))
    lab = "; ".join(f"{l}: {v} ({n})" for l, v, n in items)
    return svg(W, H, "".join(body), lab, t["bg"], pad=48)


# ---------------------------------------------------------------- case arc (the framework)
STEPS = ("Context", "Problem", "Strategy", "Result")


def arc(dark: bool, texts: list[str]) -> str:
    """Context -> Problem -> Strategy -> Result, the result node filled in Cobalt."""
    t = theme(dark)
    W, colw, gap = 1200, 258, 56
    wrapped = [wrap(s, 20, colw - 20)[:6] for s in texts]
    H = 128 + max(len(w) for w in wrapped) * 29
    body = []
    for i, (name, lines) in enumerate(zip(STEPS, wrapped)):
        x = i * (colw + gap)
        last = i == 3
        fill = COBALT if last else "none"
        stroke = COBALT if last else t["fg"]
        body.append(f'<rect x="{x + 1.5}" y="1.5" width="{colw - 3}" height="62" rx="31" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>')
        lab = f"0{i + 1}  {name.upper()}"
        body.append(text(lab, x + colw / 2, 40, 16, t["on_accent"] if last else t["fg"], "Bold", tracking=2.5, anchor="middle"))
        if i < 3:
            body.append(arrow(x + colw + 10, 33, x + colw + gap - 10, COBALT))
        for j, ln in enumerate(lines):
            body.append(text(ln, x + colw / 2, 112 + j * 29, 20, t["fg"] if last else t["sub"],
                             "Bold" if last else "Regular", anchor="middle"))
    lab = " → ".join(f"{n}: {s}" for n, s in zip(STEPS, texts))
    return svg(W, H, "".join(body), lab, t["bg"], pad=48)


# ---------------------------------------------------------------- horizontal bar chart
def bars(dark: bool, title: str, subtitle: str, rows: list[tuple], fmt: str = "{:.2f}",
         highlight: dict | None = None, refs: list[tuple[float, str]] = (), source: str = "",
         series: list[tuple[str, str]] | None = None, xmax: float | None = None) -> str:
    """rows: (label, value) or (label, [v1, v2]) when `series` names two series.

    highlight maps row label -> colour; un-highlighted rows stay neutral. With two series, the first
    series is the accent and the second the neutral comparison.
    """
    t = theme(dark)
    highlight = highlight or {}
    W, x0, x1 = 1200, 330, 1060
    tl = wrap(title, 34, W - 40, "Black")
    y = 0
    body = []
    for ln in tl:
        y += 46
        body.append(text(ln, 0, y, 34, t["fg"], "Black"))
    for ln in wrap(subtitle, 21, W - 40):
        y += 34
        body.append(text(ln, 0, y, 21, t["sub"]))
    if series:
        y += 40
        cx = 0
        for (name, col) in series:
            c = t["muted"] if col == "muted" else col
            body.append(f'<rect x="{cx}" y="{y - 14}" width="16" height="16" rx="3" fill="{c}"/>')
            body.append(text(name, cx + 26, y, 18, t["fg"], "Bold"))
            cx += 26 + width(name, 18, "Bold") + 36
    y += 34 + (24 if refs else 0)
    vals = [v for _, v in rows for v in (v if isinstance(v, (list, tuple)) else [v])]
    top = xmax or max(vals + [r[0] for r in refs]) * 1.08
    sx = lambda v: x0 + (x1 - x0) * v / top
    nser = len(series) if series else 1
    bh, rowh = (26, 50) if nser == 1 else (18, 58)
    y_rows = y
    for label, v in rows:
        vs = v if isinstance(v, (list, tuple)) else [v]
        body.append(text(label, x0 - 22, y + (rowh - 14) / 2 + 2 - (0 if nser == 1 else 2), 21, t["fg"], anchor="end"))
        for k, val in enumerate(vs):
            if series:
                col = series[k][1]
                c = t["muted"] if col == "muted" else col
            else:
                c = highlight.get(label, t["muted"])
            by = y + 4 + k * (bh + 4)
            body.append(f'<rect x="{x0}" y="{by}" width="{max(sx(val) - x0, 2):.1f}" height="{bh}" rx="3" fill="{c}"/>')
            strong = c != t["muted"]
            body.append(text(fmt.format(val), sx(val) + 12, by + bh / 2 + 7, 19 if nser > 1 else 21,
                             c if strong else t["sub"], "Bold" if strong else "Regular"))
        y += rowh
    for v, lab in refs:
        xr = sx(v)
        body.append(f'<path d="M{xr:.1f} {y_rows - 14} V{y - 4}" stroke="{t["fg"]}" stroke-opacity="0.55" stroke-width="1.5" stroke-dasharray="5 5"/>')
        body.append(text(lab.upper(), xr, y_rows - 22, 13, t["sub"], "Bold", tracking=2, anchor="middle"))
    body.append(f'<path d="M{x0} {y_rows - 4} V{y - 4}" stroke="{t["fg"]}" stroke-opacity="0.35" stroke-width="1.5"/>')
    if source:
        y += 30
        body.append(text(source, 0, y, 16, t["sub"]))
    H = int(y + 16)
    lab = f"{title}. " + "; ".join(f"{l}: {v}" for l, v in rows)
    return svg(W, H, "".join(body), lab, t["bg"], pad=48)


# ---------------------------------------------------------------- method track (footer)
STAGES = (("Validate", "Find real signal"), ("Scale", "Concentrate on what works"),
          ("Retain", "Make value stay"), ("Build", "Research and products"))


def track(dark: bool, stage: str | None) -> str:
    t = theme(dark)
    W, H, colw, gap = 1200, 150, 258, 56
    body = []
    for i, (name, desc) in enumerate(STAGES):
        x = i * (colw + gap)
        on = name == stage
        col = COBALT if on else t["sub"]
        body.append(f'<rect x="{x}" y="0" width="{colw}" height="4" rx="2" fill="{col}" fill-opacity="{1 if on else 0.45}"/>')
        body.append(text(f"0{i + 1}  {name.upper()}", x, 48, 18, COBALT if on else t["fg"], "Bold", tracking=3.5))
        body.append(text(desc, x, 84, 20, t["sub"]))
        if on:
            body.append(text("THIS REPOSITORY", x, 122, 13, COBALT, "Bold", tracking=3))
        if i < 2:
            body.append(arrow(x + colw + 14, 40, x + colw + gap - 14, t["sub"], 2))
    lab = f"ABADE method: validate, scale, retain, build. This repository: {stage or 'portfolio'}"
    return svg(W, H, "".join(body), lab, t["bg"], pad=48)


# ---------------------------------------------------------------- portfolio map (profile)
def portfolio_map(dark: bool, columns: dict[str, list[tuple[str, str]]]) -> str:
    t = theme(dark)
    W, colw, gap = 1200, 258, 56
    rows = max(len(v) for v in columns.values())
    H = 150 + rows * 112
    body = []
    for i, (name, desc) in enumerate(STAGES):
        x = i * (colw + gap)
        col = COBALT if i < 3 else AURUM
        body.append(f'<rect x="{x}" y="0" width="{colw}" height="5" rx="2.5" fill="{col}"/>')
        body.append(text(f"0{i + 1}  {name.upper()}", x, 50, 20, t["fg"], "Bold", tracking=3.5))
        body.append(text(desc, x, 86, 20, t["sub"]))
        if i < 2:
            body.append(arrow(x + colw + 14, 42, x + colw + gap - 14, COBALT, 2.5))
        for j, (repo, line) in enumerate(columns.get(name, [])):
            yy = 136 + j * 112
            body.append(f'<rect x="{x}" y="{yy}" width="{colw}" height="100" rx="16" fill="{t["card"]}" stroke="{t["line"]}"/>')
            rs = 20
            while width(repo, rs, "Bold") > colw - 40:
                rs -= 1
            body.append(text(repo, x + 20, yy + 38, rs, t["fg"], "Bold"))
            for k, ln in enumerate(wrap(line, 16, colw - 40)[:2]):
                body.append(text(ln, x + 20, yy + 66 + k * 22, 16, t["sub"]))
    lab = "; ".join(f"{k}: {', '.join(r for r, _ in v)}" for k, v in columns.items())
    return svg(W, H, "".join(body), lab, t["bg"], pad=48)


def emit(out: Path, name: str, fn, *args, **kw) -> None:
    out.mkdir(parents=True, exist_ok=True)
    for mode in ("light", "dark"):
        (out / f"{name}-{mode}.svg").write_text(fn(mode == "dark", *args, **kw), encoding="utf-8")


def picture(path: str, alt: str, w: str = "100%") -> str:
    """The README snippet for a themed asset pair."""
    return (f'<p align="center">\n  <picture>\n    <source media="(prefers-color-scheme: dark)" srcset="{path}-dark.svg">\n'
            f'    <img alt="{alt}" src="{path}-light.svg" width="{w}">\n  </picture>\n</p>')
