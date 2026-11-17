"""Outils communs de génération des rapports PDF (HTML -> Chrome -> PDF)."""
from __future__ import annotations

import base64
import hashlib
import html
import io
import shutil
import subprocess
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
ASSETS.mkdir(exist_ok=True)
LAB = Path.home() / "iotlab-tp"

MONO = "/usr/share/fonts/liberation-mono-fonts/LiberationMono-Regular.ttf"
MONO_B = "/usr/share/fonts/liberation-mono-fonts/LiberationMono-Bold.ttf"
SANS = "Liberation Sans, DejaVu Sans, sans-serif"
MONO_CSS = "Liberation Mono, DejaVu Sans Mono, monospace"

# ---------------------------------------------------------------- utilitaires


def esc(text: str) -> str:
    return html.escape(str(text), quote=False)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


# ------------------------------------------------------- captures « terminal »


def _wrap(line: str, width: int) -> list[str]:
    if len(line) <= width:
        return [line]
    out: list[str] = []
    first = True
    while len(line) > width:
        cut = line.rfind(" ", 0, width)
        if cut < width * 0.55:
            cut = width
        out.append(line[:cut])
        line = ("    " if not first else "") + line[cut:].lstrip()
        first = False
    out.append(line)
    return out


def terminal(
    name: str,
    title: str,
    lines: list[str],
    highlights: tuple[str, ...] = (),
    max_cols: int = 108,
) -> Path:
    """Rend une sortie de commandes réelle sous forme de capture de terminal."""
    path = ASSETS / f"{name}.png"
    font = ImageFont.truetype(MONO, 27)
    font_b = ImageFont.truetype(MONO_B, 27)
    cw = font.getlength("M")
    lh = 37
    pad_x, pad_top, pad_bottom = 30, 26, 28
    header = 52
    scale = 2

    wrapped: list[str] = []
    for raw in lines:
        for part in _wrap(raw.replace("\t", "    "), max_cols):
            wrapped.append(part)
    cols = max([len(x) for x in wrapped] + [80])
    cols = min(max(cols, 88), max_cols)
    width = int(cols * cw + pad_x * 2)
    height = int(header + pad_top + len(wrapped) * lh + pad_bottom)

    img = Image.new("RGB", (width * scale, height * scale), "#0d1117")
    d = ImageDraw.Draw(img)
    s = scale

    def box(x, y, w, h, r, fill, outline=None):
        d.rounded_rectangle([x * s, y * s, (x + w) * s, (y + h) * s], radius=r * s, fill=fill, outline=outline)

    box(0, 0, width, height, 18, "#0d1117", "#2b3648")
    d.rectangle([2 * s, 2 * s, (width - 2) * s, header * s], fill="#161d27")
    d.line([2 * s, header * s, (width - 2) * s, header * s], fill="#2b3648", width=1 * s)
    for i, color in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        cx, cy, r = 26 + i * 26, header / 2, 8
        d.ellipse([(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s], fill=color)
    tw = d.textlength(title, font=font)
    d.text(((width - tw) / 2 * s, (header / 2 - 15) * s), title, font=font, fill="#8b98a9")

    y = header + pad_top
    for line in wrapped:
        low = line.lower()
        fill = "#c9d4e3"
        fnt = font
        prefix = None
        if line.startswith("$ "):
            prefix, line = "$ ", line[2:]
            fill = "#e6edf3"
        if any(term.lower() in low for term in highlights):
            fill, fnt = "#ffd166", font_b
        elif any(w in low for w in ("refus", "error", "failed", "échec", "echec", "denied", "alert", "traceback")):
            fill = "#ff7b72"
        elif any(w in low for w in ("success", "accepté", "acceptee", " ok", "connack : success", "vérifié")):
            fill = "#7ee787"
        elif line.strip().startswith("#"):
            fill = "#7d8b9e"

        x = pad_x
        if prefix:
            d.text((x * s, y * s), "$", font=font_b, fill="#7ee787")
            x += cw
        d.text((x * s, y * s), line, font=fnt, fill=fill)
        y += lh

    img.save(path, "PNG", optimize=True)
    return path


def figure(num: int, img: Path | str, caption: str, cls: str = "") -> str:
    p = Path(img)
    b64 = base64.b64encode(p.read_bytes()).decode()
    return (
        f'<figure class="{cls}"><img src="data:image/png;base64,{b64}" alt="{esc(caption)}">'
        f"<figcaption><b>Figure {num}</b> — {caption}</figcaption></figure>"
    )


# ---------------------------------------------------------------- composants


def code_block(filename: str, code: str, small: bool = False) -> str:
    cls = "code small" if small else "code"
    return (
        f'<div class="{cls}"><div class="code-head">{esc(filename)}</div>'
        f"<pre>{esc(code.strip(chr(10)))}</pre></div>"
    )


def pkt_table(rows, highlight=(), caption: str = "") -> str:
    head = (
        "<div class='pktwrap'><table class='pkt'>"
        "<colgroup><col style='width:6%'><col style='width:9%'><col style='width:13%'>"
        "<col style='width:13%'><col style='width:11%'><col style='width:48%'></colgroup>"
        "<thead><tr>"
        "<th>N°</th><th>Temps (s)</th><th>Source</th><th>Destination</th>"
        "<th>Protocole</th><th>Info</th></tr></thead><tbody>"
    )
    body = []
    for frame, t, src, dst, proto, info in rows:
        p = proto.lower().replace("tlsv1.2", "tls").replace("tlsv1", "tls")
        cls = " class='hl'" if int(frame) in highlight else ""
        body.append(
            f"<tr{cls}><td>{frame}</td><td>{t}</td><td class='mono'>{esc(src)}</td>"
            f"<td class='mono'>{esc(dst)}</td><td><span class='pbadge {p}'>{esc(proto)}</span></td>"
            f"<td>{esc(info)}</td></tr>"
        )
    cap = f"<div class='pktcap'>{caption}</div>" if caption else ""
    return head + "".join(body) + "</tbody></table></div>" + cap


def table(headers, rows, cls: str = "", widths=None) -> str:
    cols = ""
    if widths:
        cols = "<colgroup>" + "".join(f"<col style='width:{w}'>" for w in widths) + "</colgroup>"
    th = "".join(f"<th>{h}</th>" for h in headers)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table class='std {cls}'>{cols}<thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>"


def qa(num: int, question: str, answer: str) -> str:
    return (
        f"<div class='qa'><div class='q'><span class='qnum'>Q{num}</span> {question}</div>"
        f"<div class='a'>{answer}</div></div>"
    )


def callout(kind: str, title: str, body: str) -> str:
    return f"<div class='callout {kind}'><div class='co-title'>{title}</div><div>{body}</div></div>"


def bullets(items) -> str:
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def badge(text: str, cls: str = "ok") -> str:
    return f"<span class='badge {cls}'>{esc(text)}</span>"


# --------------------------------------------------------------------- SVG


def trust_svg(mtls: bool = False) -> str:
    if not mtls:
        return """
<svg class="diagram" viewBox="0 0 900 330" xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="ar" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
    <path d="M0,0 L0,6 L9,3 z" fill="#0f766e"/></marker></defs>
  <rect x="315" y="20" width="270" height="78" rx="10" fill="#0f2a43"/>
  <text x="450" y="52" text-anchor="middle" fill="#fff" font-family="Liberation Sans" font-size="19" font-weight="bold">CA-Lab</text>
  <text x="450" y="78" text-anchor="middle" fill="#a9c3d6" font-family="Liberation Mono" font-size="13">ca.crt / ca.key</text>
  <rect x="55" y="215" width="330" height="92" rx="10" fill="#e8f3f1" stroke="#0f766e" stroke-width="2"/>
  <text x="220" y="247" text-anchor="middle" fill="#0f2a43" font-family="Liberation Sans" font-size="18" font-weight="bold">Broker Mosquitto</text>
  <text x="220" y="272" text-anchor="middle" fill="#334" font-family="Liberation Mono" font-size="13">broker.crt (CN=localhost)</text>
  <text x="220" y="292" text-anchor="middle" fill="#334" font-family="Liberation Mono" font-size="13">listener 8883 TLS</text>
  <rect x="515" y="215" width="330" height="92" rx="10" fill="#fff4e5" stroke="#b45309" stroke-width="2"/>
  <text x="680" y="247" text-anchor="middle" fill="#0f2a43" font-family="Liberation Sans" font-size="18" font-weight="bold">ESP8266 / client</text>
  <text x="680" y="272" text-anchor="middle" fill="#334" font-family="Liberation Mono" font-size="13">ancre : ca.crt</text>
  <text x="680" y="292" text-anchor="middle" fill="#334" font-family="Liberation Mono" font-size="13">vérifie le serveur</text>
  <line x1="400" y1="98" x2="250" y2="213" stroke="#0f766e" stroke-width="2.5" marker-end="url(#ar)"/>
  <text x="270" y="160" fill="#0f766e" font-family="Liberation Sans" font-size="13">signe broker.crt</text>
  <line x1="560" y1="213" x2="490" y2="100" stroke="#b45309" stroke-width="2.5" stroke-dasharray="7 5" marker-end="url(#ar)"/>
  <text x="520" y="170" fill="#b45309" font-family="Liberation Sans" font-size="13">fait confiance à la CA</text>
  <line x1="515" y1="260" x2="390" y2="260" stroke="#0f766e" stroke-width="2.5" marker-end="url(#ar)"/>
  <text x="450" y="252" text-anchor="middle" fill="#0f766e" font-family="Liberation Sans" font-size="11">TLS 8883</text>
</svg>"""
    return """
<svg class="diagram" viewBox="0 0 900 360" xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="ar2" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
    <path d="M0,0 L0,6 L9,3 z" fill="#0f766e"/></marker></defs>
  <rect x="315" y="18" width="270" height="78" rx="10" fill="#0f2a43"/>
  <text x="450" y="50" text-anchor="middle" fill="#fff" font-family="Liberation Sans" font-size="19" font-weight="bold">CA-Lab</text>
  <text x="450" y="76" text-anchor="middle" fill="#a9c3d6" font-family="Liberation Mono" font-size="13">ca.crt / ca.key</text>
  <rect x="30" y="235" width="330" height="100" rx="10" fill="#e8f3f1" stroke="#0f766e" stroke-width="2"/>
  <text x="195" y="267" text-anchor="middle" fill="#0f2a43" font-family="Liberation Sans" font-size="18" font-weight="bold">Broker Mosquitto</text>
  <text x="195" y="292" text-anchor="middle" fill="#334" font-family="Liberation Mono" font-size="13">broker.crt (serveur)</text>
  <text x="195" y="312" text-anchor="middle" fill="#334" font-family="Liberation Mono" font-size="13">require_certificate true</text>
  <rect x="540" y="235" width="330" height="100" rx="10" fill="#fff4e5" stroke="#b45309" stroke-width="2"/>
  <text x="705" y="267" text-anchor="middle" fill="#0f2a43" font-family="Liberation Sans" font-size="18" font-weight="bold">ESP8266</text>
  <text x="705" y="292" text-anchor="middle" fill="#334" font-family="Liberation Mono" font-size="13">esp01.crt (CN=esp01-client)</text>
  <text x="705" y="312" text-anchor="middle" fill="#334" font-family="Liberation Mono" font-size="13">clé privée esp01.key</text>
  <line x1="395" y1="96" x2="230" y2="233" stroke="#0f766e" stroke-width="2.5" marker-end="url(#ar2)"/>
  <text x="180" y="175" fill="#0f766e" font-family="Liberation Sans" font-size="13">signe broker.crt</text>
  <line x1="505" y1="96" x2="670" y2="233" stroke="#0f766e" stroke-width="2.5" marker-end="url(#ar2)"/>
  <text x="628" y="175" fill="#0f766e" font-family="Liberation Sans" font-size="13">signe esp01.crt</text>
  <line x1="540" y1="285" x2="365" y2="285" stroke="#0f766e" stroke-width="2.5" marker-end="url(#ar2)"/>
  <text x="451" y="277" text-anchor="middle" fill="#0f766e" font-family="Liberation Sans" font-size="11">Certificate Request</text>
  <line x1="360" y1="315" x2="540" y2="315" stroke="#b45309" stroke-width="2.5" marker-end="url(#ar2)"/>
  <text x="451" y="307" text-anchor="middle" fill="#b45309" font-family="Liberation Sans" font-size="11">Certificate + Verify</text>
</svg>"""


def sequence_svg() -> str:
    return """
<svg class="diagram" viewBox="0 0 900 470" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="ar3" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#0f766e"/></marker>
    <marker id="ar4" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#b45309"/></marker>
  </defs>
  <rect x="95" y="15" width="220" height="52" rx="8" fill="#fff4e5" stroke="#b45309" stroke-width="2"/>
  <text x="205" y="47" text-anchor="middle" fill="#0f2a43" font-family="Liberation Sans" font-size="16" font-weight="bold">ESP8266</text>
  <rect x="585" y="15" width="220" height="52" rx="8" fill="#e8f3f1" stroke="#0f766e" stroke-width="2"/>
  <text x="695" y="47" text-anchor="middle" fill="#0f2a43" font-family="Liberation Sans" font-size="16" font-weight="bold">Broker Mosquitto</text>
  <line x1="205" y1="67" x2="205" y2="455" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="5 5"/>
  <line x1="695" y1="67" x2="695" y2="455" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="5 5"/>
  <line x1="205" y1="105" x2="690" y2="105" stroke="#0f766e" stroke-width="2" marker-end="url(#ar3)"/>
  <text x="447" y="97" text-anchor="middle" fill="#0f2a43" font-family="Liberation Sans" font-size="13">1. Client Hello (SNI=localhost)</text>
  <line x1="695" y1="150" x2="210" y2="150" stroke="#b45309" stroke-width="2" marker-end="url(#ar4)"/>
  <text x="447" y="142" text-anchor="middle" fill="#0f2a43" font-family="Liberation Sans" font-size="13">2. Server Hello, Certificate, Certificate Request</text>
  <text x="447" y="172" text-anchor="middle" fill="#64748b" font-family="Liberation Sans" font-size="11">l'ESP vérifie le certificat du broker avec ca.crt</text>
  <line x1="205" y1="215" x2="690" y2="215" stroke="#0f766e" stroke-width="2" marker-end="url(#ar3)"/>
  <text x="447" y="207" text-anchor="middle" fill="#0f2a43" font-family="Liberation Sans" font-size="13">3. Certificate (CN=esp01-client) + Client Key Exchange</text>
  <line x1="205" y1="260" x2="690" y2="260" stroke="#0f766e" stroke-width="2" marker-end="url(#ar3)"/>
  <text x="447" y="252" text-anchor="middle" fill="#0f2a43" font-family="Liberation Sans" font-size="13">4. Certificate Verify : signature avec esp01.key</text>
  <line x1="695" y1="305" x2="210" y2="305" stroke="#b45309" stroke-width="2" marker-end="url(#ar4)"/>
  <text x="447" y="297" text-anchor="middle" fill="#0f2a43" font-family="Liberation Sans" font-size="13">5. Change Cipher Spec, Finished</text>
  <line x1="205" y1="350" x2="690" y2="350" stroke="#0f766e" stroke-width="2" marker-end="url(#ar3)"/>
  <text x="447" y="342" text-anchor="middle" fill="#0f2a43" font-family="Liberation Sans" font-size="13">6. Application Data (MQTT chiffré)</text>
  <line x1="695" y1="395" x2="210" y2="395" stroke="#b45309" stroke-width="2" marker-end="url(#ar4)"/>
  <text x="447" y="387" text-anchor="middle" fill="#0f2a43" font-family="Liberation Sans" font-size="13">7. Application Data (CONNACK, PUBLISH chiffrés)</text>
  <rect x="270" y="420" width="360" height="34" rx="6" fill="#f1f5f9" stroke="#cbd5e1"/>
  <text x="450" y="442" text-anchor="middle" fill="#334155" font-family="Liberation Sans" font-size="12">La clé privée esp01.key ne quitte jamais l'objet.</text>
</svg>"""


# --------------------------------------------------------------------- PDF


CSS = """
:root{
  --navy:#0f2a43; --teal:#0f766e; --teal2:#14b8a6; --amber:#b45309;
  --ink:#1e293b; --muted:#64748b; --line:#dbe3ec; --bg:#f6f9fc;
}
*{box-sizing:border-box}
@page{size:A4;margin:17mm 16mm 18mm 16mm}
@page:first{margin:0}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{margin:0;font-family:"Liberation Sans","DejaVu Sans",sans-serif;font-size:10.2pt;line-height:1.5;color:var(--ink)}
p{margin:.45em 0 .7em}
h1,h2,h3,h4{color:var(--navy);font-weight:bold;line-height:1.25;break-after:avoid}
h1{font-size:19pt;margin:0 0 8pt;padding-bottom:6pt;border-bottom:2.5pt solid var(--teal)}
h1 .num{color:var(--teal);margin-right:8pt}
h2{font-size:13.2pt;margin:16pt 0 5pt}
h3{font-size:11.2pt;margin:12pt 0 4pt;color:#173f5f}
ul,ol{margin:.3em 0 .8em;padding-left:1.35em}
li{margin:.18em 0}
code{font-family:"Liberation Mono","DejaVu Sans Mono",monospace;font-size:9pt;background:#eef3f8;color:#0b3b5c;padding:1px 4px;border-radius:3px}
b,strong{color:#0b2a44}

/* couverture */
.cover{height:297mm;background:linear-gradient(150deg,#0a1f33 0%,#0f2a43 55%,#124a5c 100%);color:#fff;padding:26mm 24mm;position:relative;overflow:hidden}
.cover:before{content:"";position:absolute;right:-70mm;top:-60mm;width:200mm;height:200mm;border-radius:50%;background:rgba(20,184,166,.10)}
.cover:after{content:"";position:absolute;left:-40mm;bottom:-90mm;width:170mm;height:170mm;border-radius:50%;background:rgba(255,255,255,.035)}
.cover .kicker{font-size:10pt;letter-spacing:2.6pt;text-transform:uppercase;color:#7dd3c7;font-weight:bold}
.cover h1{border:0;color:#fff;font-size:33pt;margin:14mm 0 4mm;padding:0;line-height:1.1}
.cover .sub{font-size:14pt;color:#bfd7e6;margin:0 0 18mm;max-width:150mm;line-height:1.35}
.cover .meta{position:absolute;left:24mm;right:24mm;bottom:26mm;border-top:1px solid rgba(255,255,255,.18);padding-top:7mm}
.cover .meta table{width:100%;font-size:10pt;color:#dbe9f2;border-collapse:collapse}
.cover .meta td{padding:2.4mm 0;vertical-align:top;border:0}
.cover .meta td.k{color:#8fb3c9;width:34mm;font-size:8.5pt;text-transform:uppercase;letter-spacing:.7pt}
.cover .meta .v{font-weight:bold;color:#fff}
.cover .stamp{display:inline-block;margin-top:8mm;border:1px solid #2dd4bf;color:#5eead4;border-radius:4pt;padding:3pt 9pt;font-size:9pt;letter-spacing:.5pt}
.cover .files{margin-top:7mm;font-family:"Liberation Mono",monospace;font-size:8.2pt;color:#9fc3d6;line-height:1.6}

/* sommaire */
.toc{background:var(--bg);border:1px solid var(--line);border-radius:8pt;padding:7mm 9mm;margin-top:4mm}
.toc h2{margin:0 0 4mm;font-size:15pt}
.toc ol{margin:0;padding-left:1.4em;columns:2;column-gap:12mm}
.toc li{margin:1.6mm 0;color:#173f5f;font-size:10pt}

/* sections */
section{margin-bottom:4mm}
.lead{font-size:10.8pt;color:#334155}
.small{font-size:9pt;color:var(--muted)}

/* figures */
figure{margin:5mm 0 6mm;break-inside:avoid;page-break-inside:avoid}
figure img{display:block;width:100%;border-radius:5pt;border:1px solid #223047;box-shadow:0 2pt 6pt rgba(15,42,67,.12)}
figcaption{font-size:8.6pt;color:#4b5f73;margin-top:2.4mm;line-height:1.35}
figcaption b{color:var(--teal)}

/* code */
.code{border:1px solid #24344a;border-radius:6pt;overflow:hidden;margin:4mm 0 5mm;break-inside:avoid}
.code-head{background:#161d27;color:#9fb3c8;font-family:"Liberation Mono",monospace;font-size:8pt;padding:4pt 9pt;border-bottom:1px solid #2b3648}
.code pre{margin:0;background:#0d1117;color:#d7dee8;font-family:"Liberation Mono",monospace;font-size:8.1pt;line-height:1.42;padding:7pt 9pt;white-space:pre-wrap;overflow-wrap:anywhere}
.code.small pre{font-size:7.2pt;line-height:1.38}

/* tableaux */
table.std{width:100%;border-collapse:collapse;margin:3mm 0 5mm;font-size:9pt;break-inside:avoid}
table.std th{background:var(--navy);color:#fff;text-align:left;padding:5pt 6pt;font-size:8.6pt;font-weight:bold}
table.std td{padding:4.2pt 6pt;border-bottom:1px solid var(--line);vertical-align:top}
table.std tbody tr:nth-child(even){background:#f7fafc}
table.std td.c{text-align:center}
table.std td.r{text-align:right}

/* paquets */
.pktwrap{break-inside:avoid;margin:3mm 0 1mm}
table.pkt{width:100%;border-collapse:collapse;font-family:"Liberation Mono",monospace;font-size:7.6pt}
table.pkt th{background:#1f2d3d;color:#dbe7f3;text-align:left;white-space:nowrap;padding:4pt 5pt;font-family:"Liberation Sans",sans-serif;font-size:7.6pt}
table.pkt td{padding:3.2pt 5pt;border-bottom:1px solid #e6edf5;vertical-align:top}
table.pkt tbody tr:nth-child(even){background:#f8fafc}
table.pkt tr.hl td{background:#fff6dd;font-weight:bold}
table.pkt td.mono{font-family:"Liberation Mono",monospace}
.pbadge{display:inline-block;padding:1pt 4pt;border-radius:3pt;font-family:"Liberation Sans",sans-serif;font-size:7pt;font-weight:bold;color:#fff}
.pbadge.mqtt{background:#7c3aed}.pbadge.tls{background:#0f766e}.pbadge.tcp{background:#475569}.pbadge.udp{background:#b45309}
.pktcap{font-size:7.8pt;color:var(--muted);margin:0 0 5mm}

/* Q/R */
.qa{border:1px solid var(--line);border-radius:7pt;margin:3.5mm 0;break-inside:avoid;overflow:hidden}
.qa .q{background:#eef6f5;border-left:4pt solid var(--teal);padding:6pt 9pt;font-weight:bold;color:#0b3b45;font-size:9.8pt}
.qa .qnum{display:inline-block;background:var(--teal);color:#fff;border-radius:4pt;padding:1pt 6pt;margin-right:7pt;font-size:8.4pt}
.qa .a{padding:6pt 10pt 7pt;font-size:9.8pt}
.qa .a p:first-child{margin-top:0}.qa .a p:last-child{margin-bottom:0}

/* encadrés */
.callout{border-radius:7pt;padding:6pt 10pt;margin:4mm 0;break-inside:avoid;font-size:9.7pt}
.callout .co-title{font-weight:bold;margin-bottom:2pt;font-size:9.6pt}
.callout.info{background:#eef6ff;border-left:4pt solid #2563eb}
.callout.info .co-title{color:#1d4ed8}
.callout.warn{background:#fff7e6;border-left:4pt solid var(--amber)}
.callout.warn .co-title{color:#92400e}
.callout.ok{background:#ecfdf5;border-left:4pt solid #059669}
.callout.ok .co-title{color:#047857}

/* badges */
.badge{display:inline-block;border-radius:10pt;padding:1.5pt 7pt;font-size:8pt;font-weight:bold}
.badge.ok{background:#d1fae5;color:#065f46;border:1px solid #6ee7b7}
.badge.part{background:#fef3c7;color:#92400e;border:1px solid #fcd34d}
.badge.no{background:#fee2e2;color:#991b1b;border:1px solid #fca5a5}

.diagram{width:100%;height:auto;margin:3mm 0 4mm;break-inside:avoid}
.meta-grid{display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin:3mm 0 5mm}
.meta-card{background:var(--bg);border:1px solid var(--line);border-radius:6pt;padding:4mm 5mm}
.meta-card .k{font-size:8pt;letter-spacing:.8pt;text-transform:uppercase;color:var(--muted);font-weight:bold}
.meta-card .v{font-size:10.5pt;font-weight:bold;color:var(--navy);margin-top:1mm}
.page-break{break-before:page}
.nobreak{break-inside:avoid}
.two-col{columns:2;column-gap:8mm}
.kpi{display:flex;gap:4mm;margin:4mm 0}
.kpi div{flex:1;background:var(--bg);border:1px solid var(--line);border-radius:6pt;padding:3.5mm}
.kpi b{display:block;font-size:16pt;color:var(--teal);line-height:1.1}
.kpi span{font-size:8.4pt;color:var(--muted)}
"""


def render_pdf(body_html: str, out_pdf: Path, footer: str, title: str) -> None:
    html_doc = f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>{esc(title)}</title>
<style>{CSS}</style></head><body>{body_html}</body></html>"""
    html_path = out_pdf.with_suffix(".html")
    html_path.write_text(html_doc, encoding="utf-8")
    subprocess.run(
        [
            "google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox",
            "--no-pdf-header-footer", f"--print-to-pdf={out_pdf}", html_path.as_uri(),
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    add_footer(out_pdf, footer)


def add_footer(pdf_path: Path, left_text: str) -> None:
    """Ajoute un pied de page (texte + pagination) sur toutes les pages sauf la couverture."""
    try:
        import fitz  # PyMuPDF
    except Exception:
        return
    doc = fitz.open(pdf_path)
    total = doc.page_count
    for i, page in enumerate(doc):
        if i == 0:
            continue
        w, h = page.rect.width, page.rect.height
        y = h - 26
        page.draw_line(fitz.Point(45, y - 8), fitz.Point(w - 45, y - 8), color=(0.86, 0.89, 0.93), width=0.7)
        page.insert_text(fitz.Point(45, y + 3), left_text, fontsize=7.4, fontname="helv", color=(0.39, 0.45, 0.53))
        right = f"Page {i + 1} / {total}"
        tw = fitz.get_text_length(right, fontname="helv", fontsize=7.4)
        page.insert_text(fitz.Point(w - 45 - tw, y + 3), right, fontsize=7.4, fontname="helv", color=(0.39, 0.45, 0.53))
    doc.saveIncr()
    doc.close()
