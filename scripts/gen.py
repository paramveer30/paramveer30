import math, os, html
from string import Template

FONT = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
THEMES = {
    "dark": dict(panel="#0d1117", panel2="#121a23", border="#263040", fg="#e6edf3", dim="#8b949e",
                 faint="#2d3640", grid="#1c2530", l1="#a78bfa", l2="#e3a857", l3="#f47067",
                 l4="#39d0c8", ok="#3fb950", ink="#0d1117"),
    "light": dict(panel="#ffffff", panel2="#f6f8fa", border="#d0d7de", fg="#1f2328", dim="#59636e",
                  faint="#d0d7de", grid="#e6eaef", l1="#6e40c9", l2="#9a5b13", l3="#cf222e",
                  l4="#0a7f78", ok="#1a7f37", ink="#ffffff"),
}
BASE = ("text{font-family:%s}" % FONT +
        ".pulse{stroke-dasharray:8 120;animation:flow 3s linear infinite}"
        "@keyframes flow{from{stroke-dashoffset:128}to{stroke-dashoffset:0}}"
        ".blink{animation:blink 1s steps(1) infinite}@keyframes blink{50%{opacity:0}}"
        ".breathe{animation:breathe 2.4s ease-in-out infinite}@keyframes breathe{50%{opacity:.3}}")
LAYER = {"1": "$l1", "2": "$l2", "3": "$l3", "4": "$l4"}


def e(s):
    return html.escape(s, quote=True).replace("$", "$$")


def svg(w, h, label, body, css=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{e(label)}"><title>{e(label)}</title><style>{BASE}{css}</style>{body}</svg>')


def T(x, y, s, size=12, fill="$fg", anchor="start", weight=None, extra=""):
    w = f' font-weight="{weight}"' if weight else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"{w} {extra}>'
            f'{s}</text>')


# ---------------------------------------------------------------- header
LS = 'letter-spacing="1"'


def rainbow(W, gid="rb", dur=6, x0=0):
    return (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x0}" y1="0" x2="{x0+W}" y2="0" '
            'spreadMethod="repeat"><stop offset="0" stop-color="$l1"/><stop offset=".25" stop-color="$l3"/>'
            '<stop offset=".5" stop-color="$l2"/><stop offset=".75" stop-color="$l4"/><stop offset="1" stop-color="$l1"/>'
            f'<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="{W} 0" '
            f'dur="{dur}s" repeatCount="indefinite"/></linearGradient>')


def panel(W, H, rx=14):
    return (f'<defs>{rainbow(W)}<clipPath id="pc"><rect width="{W}" height="{H}" rx="{rx}"/></clipPath></defs>'
            f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="{rx}" fill="$panel" stroke="$border"/>'
            f'<rect clip-path="url(#pc)" width="{W}" height="3" fill="url(#rb)"/>')


FX = (".fi{opacity:0;animation:fi .7s ease-out forwards}"
      "@keyframes fi{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}"
      ".pin{opacity:0;animation:pin 2.4s infinite}@keyframes pin{0%{opacity:0}8%{opacity:1}30%,100%{opacity:0}}")
SPLINE = 'calcMode="spline" keyTimes="0;1" keySplines=".2 .7 .2 1"'


def typed(x, y, n, cw, begin, dur, h=20):
    """clip rect that types n characters, plus a cursor that follows it"""
    vals = ";".join(f"{i*cw+(6 if i == n else 0):.1f}" for i in range(n + 1))
    cvals = ";".join(f"{x+i*cw+2:.1f}" for i in range(n + 1))
    clip = (f'<clipPath id="ty"><rect x="{x-2}" y="{y-h+5}" width="0" height="{h}">'
            f'<animate attributeName="width" values="{vals}" calcMode="discrete" begin="{begin}s" dur="{dur}s" '
            'fill="freeze"/></rect></clipPath>')
    cur = (f'<rect class="blink" x="{x+2}" y="{y-11}" width="8" height="14" fill="$l4">'
           f'<animate attributeName="x" values="{cvals}" calcMode="discrete" begin="{begin}s" dur="{dur}s" '
           'fill="freeze"/></rect>')
    return clip, cur


def header():
    W, H = 1000, 300
    name = "PARAMVEER MULTANI"
    nw = 456
    b = [panel(W, H),
         '<defs>', rainbow(nw, "ng", 7, 40),
         '<filter id="gl" x="-10%" y="-40%" width="120%" height="180%"><feGaussianBlur stdDeviation="7"/></filter>',
         '<filter id="gs" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="4"/></filter>',
         '<radialGradient id="halo"><stop offset="0" stop-color="$l1" stop-opacity=".3">'
         '<animate attributeName="stop-color" values="$l1;$l4;$l3;$l2;$l1" dur="12s" repeatCount="indefinite"/>'
         '</stop><stop offset="1" stop-color="$l1" stop-opacity="0"/></radialGradient>',
         '<pattern id="g" width="16" height="16" patternUnits="userSpaceOnUse">'
         '<circle cx="2" cy="2" r="1" fill="$grid"/></pattern>',
         f'<clipPath id="rv"><rect x="30" y="50" width="0" height="72"><animate attributeName="width" from="0" '
         f'to="{nw+40}" begin=".2s" dur="1.4s" fill="freeze" {SPLINE}/></rect></clipPath>',
         '<clipPath id="die"><rect x="720" y="92" width="150" height="136" rx="8"/></clipPath>',
         '</defs>',
         '<rect x="600" y="46" width="390" height="244" fill="url(#g)"/>',
         '<circle cx="795" cy="160" r="150" fill="url(#halo)"><animate attributeName="r" values="120;175;120" '
         'dur="6s" repeatCount="indefinite"/></circle>',
         T(24, 28, "DATASHEET · U1 · PM-29", 11, "$dim", extra='letter-spacing="2"'),
         T(976, 28, "github.com/paramveer30 · rev 2026.10", 11, "$dim", "end"),
         '<line x1="16" y1="42" x2="984" y2="42" stroke="$faint"/>']
    # name: wipe-in reveal with a light bar, then a slow colour sweep forever
    txt = (f'x="40" y="102" font-size="42" font-weight="700" textLength="{nw}" lengthAdjust="spacing" '
           f'fill="url(#ng)"')
    b.append(f'<g clip-path="url(#rv)"><text {txt} filter="url(#gl)" opacity=".55">{name}</text>'
             f'<text {txt}>{name}</text></g>')
    b.append(f'<rect x="30" y="56" width="3" height="60" rx="1.5" fill="$fg">'
             f'<animate attributeName="x" from="30" to="{nw+70}" begin=".2s" dur="1.4s" fill="freeze" {SPLINE}/>'
             '<animate attributeName="opacity" from="1" to="0" begin="1.6s" dur=".3s" fill="freeze"/></rect>')
    b.append(T(40, 134, "Computer Engineering Co-op · McMaster · Class of 2029", 14, "$dim",
               extra='class="fi" style="animation-delay:1.2s"'))
    rows = [("FUNCTION", T(140, 178, "builds from logic gates up to the browser", 13, "$fg")),
            ("STACK", '<text x="140" y="202" font-size="13" fill="$dim"><tspan fill="$l1">SystemVerilog</tspan> · '
                      '<tspan fill="$l2">C</tspan> · <tspan fill="$l3">Python</tspan> · '
                      '<tspan fill="$l4">TypeScript</tspan></text>'),
            ("STATUS", '<circle class="breathe" cx="146" cy="222" r="4" fill="$ok"/>' +
                       T(158, 226, "open to 2027 co-op terms", 13, "$ok"))]
    for i, (k, v) in enumerate(rows):
        y = 178 + i * 24
        b.append(f'<g class="fi" style="animation-delay:{1.45+i*0.18:.2f}s">'
                 f'{T(40, y, k, 12, "$dim", extra=LS)}{v}</g>')
    prompt = "param@mcmaster:~$ ./build --from=silicon --to=software"
    cw = 7.8
    clip, cur = typed(40, 266, len(prompt), cw, 2.2, 2.0)
    b.append(f'<defs>{clip}</defs>')
    b.append(f'<text x="40" y="266" font-size="13" fill="$dim" textLength="{len(prompt)*cw:.1f}" '
             'lengthAdjust="spacing" clip-path="url(#ty)"><tspan fill="$l4">param@mcmaster</tspan>:~$$ '
             '<tspan fill="$fg">./build</tspan> <tspan fill="$l1">--from=silicon</tspan> '
             '<tspan fill="$l3">--to=software</tspan></text>')
    b.append(cur)

    # chip
    cx0, cy0, cw2, ch = 720, 92, 150, 136
    pal = ["$l1", "$l3", "$l2", "$l4"]
    for i in range(6):
        x = cx0 + 17 + i * 23
        b.append(f'<line x1="{x}" y1="{cy0}" x2="{x}" y2="62" stroke="$faint" stroke-width="2"/>')
        b.append(f'<circle cx="{x}" cy="60" r="3" fill="$panel" stroke="$dim"/>')
        b.append(f'<line x1="{x}" y1="{cy0+ch}" x2="{x}" y2="258" stroke="$faint" stroke-width="2"/>')
        b.append(f'<circle cx="{x}" cy="260" r="3" fill="$panel" stroke="$dim"/>')
        for yy, d in ((cy0 - 12, i), (cy0 + ch, 11 - i)):
            b.append(f'<rect x="{x-3}" y="{yy}" width="6" height="12" fill="$l2"/>')
            b.append(f'<rect class="pin" x="{x-3}" y="{yy}" width="6" height="12" fill="{pal[i%4]}" '
                     f'style="animation-delay:{d*0.2:.1f}s"/>')
    layers = [("web", "$l4"), ("ml", "$l3"), ("embedded", "$l2"), ("fpga", "$l1")]
    for i in range(4):
        py = cy0 + 26 + i * 28
        b.append(f'<rect x="{cx0-12}" y="{py-3}" width="12" height="6" fill="$l2"/>')
        b.append(f'<rect x="{cx0+cw2}" y="{py-3}" width="12" height="6" fill="$l2"/>')
        ty = 92 + i * 46
        d = f"M{cx0-12} {py} H682 L652 {ty} H614"
        name_, col = layers[i]
        b.append(f'<path d="{d}" fill="none" stroke="$faint" stroke-width="2"/>')
        b.append(f'<path class="pulse" d="{d}" pathLength="100" fill="none" stroke="{col}" stroke-width="2.5" '
                 f'style="animation-delay:{-i*0.7:.1f}s"/>')
        b.append(f'<circle cx="608" cy="{ty}" r="5" fill="$panel" stroke="{col}" stroke-width="2"/>')
        b.append(f'<circle class="breathe" cx="608" cy="{ty}" r="2.5" fill="{col}" '
                 f'style="animation-delay:{-i*0.6:.1f}s"/>')
        b.append(T(594, ty + 4, name_, 11, col, "end"))
        ry = 110 + i * 32
        d2 = f"M{cx0+cw2+12} {py} H902 L920 {ry} H940"
        b.append(f'<path d="{d2}" fill="none" stroke="$faint" stroke-width="2"/>')
        b.append(f'<path class="pulse" d="{d2}" pathLength="100" fill="none" stroke="{col}" stroke-width="2.5" '
                 f'style="animation-delay:{-1.5-i*0.6:.1f}s"/>')
        b.append(f'<rect x="938" y="{ry-3}" width="8" height="6" fill="$l2"/>')
    b.append('<rect x="944" y="96" width="22" height="128" rx="3" fill="$panel2" stroke="$border"/>')
    for i in range(4):
        b.append(f'<rect class="breathe" x="950" y="{106+i*32}" width="10" height="8" rx="2" fill="{pal[i]}" '
                 f'style="animation-delay:{-i*0.5:.1f}s"/>')
    b.append(T(955, 88, "J1", 10, "$dim", "middle"))
    b.append(T(955, 240, "OUT", 10, "$dim", "middle"))
    b.append(f'<rect x="{cx0}" y="{cy0}" width="{cw2}" height="{ch}" rx="8" fill="none" stroke="url(#rb)" '
             'stroke-width="5" filter="url(#gs)" opacity=".8"/>')
    b.append(f'<rect x="{cx0}" y="{cy0}" width="{cw2}" height="{ch}" rx="8" fill="$panel2" stroke="url(#rb)" '
             'stroke-width="2"/>')
    b.append('<g clip-path="url(#die)"><rect x="720" y="92" width="150" height="2" fill="$l4" opacity=".55">'
             '<animate attributeName="y" values="92;226;92" dur="4s" repeatCount="indefinite"/></rect></g>')
    b.append(f'<circle cx="{cx0+13}" cy="{cy0+13}" r="3.5" fill="$dim"/>')
    b.append(T(cx0 + cw2 / 2, 158, "PM-29", 26, "url(#rb)", "middle", 700))
    b.append(T(cx0 + cw2 / 2, 180, "McMaster · CE", 11, "$dim", "middle"))
    b.append(T(cx0 + cw2 / 2, 198, "rev 3.0", 10, "$dim", "middle"))
    b.append(T(cx0 + cw2 + 4, 82, "U1", 11, "$dim"))
    label = ("Paramveer Multani, Computer Engineering co-op at McMaster. "
             "Builds from logic gates up to the browser: FPGA, embedded C, machine learning and full stack.")
    return svg(W, H, label, "".join(b), FX)


# ---------------------------------------------------------------- section banners + footer
SECTIONS = {
    "now": ("~/now", "# pulled live from github every 6 hours"),
    "projects": ("~/projects", "# one card per layer, silicon up to product"),
    "experience": ("~/experience", "# timing diagram, one channel per role"),
    "stack": ("~/stack", "# where each tool actually gets used"),
    "contributions": ("~/contributions", "# commit history, eaten daily"),
}


def section(title, note):
    W, H = 1000, 56
    tw = len(title) * 14.4
    nx = 56 + tw + 18
    rx = nx + len(note) * 7.2 + 18
    b = [f'<defs>{rainbow(W)}{rainbow(tw, "tg", 5, 52)}</defs>',
         T(26, 37, "&gt;", 22, "$l4", weight=700, extra='class="blink"'),
         f'<text x="52" y="38" font-size="24" font-weight="700" fill="url(#tg)" textLength="{tw:.0f}" '
         f'lengthAdjust="spacing">{e(title)}</text>',
         T(nx, 36, e(note), 12, "$dim"),
         f'<line x1="{rx:.0f}" y1="32" x2="{W-12}" y2="32" stroke="$faint" stroke-width="2"/>',
         f'<line x1="{rx:.0f}" y1="32" x2="{W-12}" y2="32" stroke="url(#rb)" stroke-width="2" opacity=".9" '
         f'stroke-dasharray="{(W-12-rx):.0f}" stroke-dashoffset="{(W-12-rx):.0f}">'
         f'<animate attributeName="stroke-dashoffset" from="{(W-12-rx):.0f}" to="0" dur="1.6s" fill="freeze" '
         f'{SPLINE}/></line>']
    return svg(W, H, f"{title} {note.lstrip('# ')}", "".join(b))


def footer():
    W, H = 1000, 150
    hobbies = ["basketball", "ufc", "chess", "hiking", "hip-hop", "horror movies", "catan"]
    pal = ["$l1", "$l3", "$l2", "$l4"]
    b = [panel(W, H),
         '<text x="28" y="40" font-size="13" fill="$dim"><tspan fill="$l4">param@mcmaster</tspan>:~$$ '
         '<tspan fill="$fg">make</tspan> <tspan fill="$l2">profile</tspan></text>',
         '<rect x="28" y="54" width="944" height="6" rx="3" fill="$faint"/>',
         '<rect x="28" y="54" width="0" height="6" rx="3" fill="url(#rb)">'
         '<animate attributeName="width" values="0;944;944" keyTimes="0;.55;1" dur="6s" repeatCount="indefinite"/>'
         '</rect>',
         '<text x="28" y="84" font-size="12.5" fill="$dim"><tspan fill="$l1">silicon</tspan> · '
         '<tspan fill="$l2">firmware</tspan> · <tspan fill="$l3">models</tspan> · '
         '<tspan fill="$l4">product</tspan>  <tspan fill="$ok" font-weight="700">build ok</tspan>'
         '  0 errors · 0 warnings</text>',
         T(972, 84, "off the clock:", 11, "$dim", "end")]
    x = 28
    for i, h in enumerate(hobbies):
        w = len(h) * 7.2 + 22
        c = pal[i % 4]
        b.append(f'<rect x="{x:.0f}" y="104" width="{w:.0f}" height="26" rx="13" fill="{c}" fill-opacity=".1" '
                 f'stroke="{c}" stroke-opacity=".6"/>')
        b.append(f'<rect class="pin" x="{x:.0f}" y="104" width="{w:.0f}" height="26" rx="13" fill="{c}" '
                 f'fill-opacity=".28" style="animation-delay:{i*0.34:.2f}s"/>')
        b.append(T(x + w / 2, 121, e(h), 12, c, "middle"))
        x += w + 10
    return svg(W, H, "Build successful. Off the clock: " + ", ".join(hobbies), "".join(b), FX)


# ---------------------------------------------------------------- cards
def card(layer, layer_name, repo, badge, title, sub, tags, visual, label, css=""):
    W, H = 480, 270
    col = LAYER[layer]
    col2 = LAYER[str(int(layer) % 4 + 1)]
    tag = f"L{layer} {layer_name}"
    b = [f'<defs><linearGradient id="cs" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="0" '
         f'spreadMethod="repeat"><stop offset="0" stop-color="{col}"/><stop offset=".5" stop-color="{col2}"/>'
         f'<stop offset="1" stop-color="{col}"/><animateTransform attributeName="gradientTransform" type="translate" '
         f'from="0 0" to="{W} 0" dur="5s" repeatCount="indefinite"/></linearGradient>'
         f'<radialGradient id="cg" cx="1" cy="0" r="1"><stop offset="0" stop-color="{col}" stop-opacity=".18"/>'
         f'<stop offset=".65" stop-color="{col}" stop-opacity="0"/></radialGradient>'
         f'<clipPath id="pc"><rect width="{W}" height="{H}" rx="12"/></clipPath></defs>',
         f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="$panel" stroke="{col}" stroke-opacity=".45"/>',
         f'<rect clip-path="url(#pc)" width="{W}" height="{H}" fill="url(#cg)"/>',
         f'<rect clip-path="url(#pc)" width="{W}" height="3" fill="url(#cs)"/>',
         f'<rect x="1" y="18" width="3" height="{H-36}" rx="1.5" fill="url(#cs)"/>',
         T(20, 29, e(tag), 11, col, weight=700, extra='letter-spacing="1"'),
         T(20 + len(tag) * 7.7 + 10, 29, e("· " + repo), 11, "$dim")]
    bw = len(badge) * 6.7 + 18
    b.append(f'<rect x="{W-20-bw:.0f}" y="15" width="{bw:.0f}" height="19" rx="9.5" fill="{col}" fill-opacity=".12" '
             f'stroke="{col}"/>')
    b.append(T(W - 20 - bw / 2, 28.5, e(badge), 11, col, "middle"))
    b.append(f'<line x1="20" y1="44" x2="{W-20}" y2="44" stroke="$faint" stroke-dasharray="2 4"/>')
    b.append(f'<g transform="translate(20,54)">{visual}</g>')
    b.append(T(20, 200, e(title), 20, "$fg", weight=700))
    b.append(f'<rect x="20" y="206" width="28" height="2" rx="1" fill="url(#cs)"/>')
    b.append(T(20, 224, e(sub), 12.5, "$dim"))
    x = 20
    for t in tags:
        w = len(t) * 7 + 16
        b.append(f'<rect x="{x}" y="236" width="{w}" height="20" rx="4" fill="{col}" fill-opacity=".1" '
                 f'stroke="{col}" stroke-opacity=".45"/>')
        b.append(T(x + w / 2, 250, e(t), 11, "$fg", "middle"))
        x += w + 6
    return svg(W, H, label, "".join(b), css)


def _bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
            u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1])


AERO_TOP = [((8, 86), (8, 74), (14, 66), (34, 62)),
            ((34, 62), (46, 60), (58, 58), (70, 56)),
            ((70, 56), (88, 44), (108, 34), (134, 32)),
            ((134, 32), (160, 31), (182, 42), (204, 58)),
            ((204, 58), (210, 62), (214, 64), (218, 66)),
            ((218, 66), (224, 72), (224, 82), (220, 88))]


def v_aero():
    s = []
    pts = []
    for seg in AERO_TOP:
        for k in range(10):
            pts.append(_bez(*seg, k / 10))
    pts.append(AERO_TOP[-1][3])
    body = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " L8 88 Z"
    # streamlines that hug the body, offset upward
    for k, (off, c) in enumerate([(10, "$l4"), (22, "$l1"), (34, "$l4"), (46, "$l1")]):
        line = [(-8, 86 - off * 0.55)]
        for x, y in pts[::3]:
            if x <= 212:
                line.append((x, y - off))
        line.append((236, line[-1][1] + 10 - off * 0.15))
        d = "M" + " L".join(f"{x:.1f} {max(2, y):.1f}" for x, y in line)
        s.append(f'<path d="{d}" fill="none" stroke="$faint" stroke-width="1.2" stroke-linejoin="round"/>')
        s.append(f'<path class="fl" d="{d}" fill="none" stroke="{c}" stroke-width="1.6" stroke-linejoin="round" '
                 f'style="animation-delay:{-k*0.3:.1f}s"/>')
    s.append(f'<path d="{body}" fill="$panel2" stroke="$border"/>')
    s.append('<path d="M84 52 L108 40 C120 36 132 36 140 38 L146 52 Z" fill="$faint"/>')
    # surface pressure points: high at the nose, low over the roof
    for i, (x, y) in enumerate(pts[1:-1:2]):
        c = "$l3" if x < 50 else "$l2" if x < 105 else "$l4" if x < 190 else "$l1"
        s.append(f'<circle class="pd" cx="{x:.1f}" cy="{y:.1f}" r="2.2" fill="{c}" '
                 f'style="animation-delay:{x/120:.2f}s"/>')
    s.append('<line x1="-4" y1="98" x2="232" y2="98" stroke="$faint"/>')
    for wx in (54, 176):
        s.append(f'<circle cx="{wx}" cy="88" r="10" fill="$panel" stroke="$dim" stroke-width="2"/>'
                 f'<circle cx="{wx}" cy="88" r="3" fill="$dim"/>')
    s.append(T(0, 114, "Cp: nose high · roof low", 9.5, "$dim"))
    s.append('<rect x="246" y="2" width="194" height="96" rx="6" fill="$panel2" stroke="$faint"/>')
    lines = [(256, 20, '<tspan fill="$dim">agent loop · trust gated</tspan>', 9.5),
             (256, 42, '<tspan fill="$l1">propose</tspan>  roof −8 mm', 11.5),
             (256, 62, '<tspan fill="$l3">predict</tspan>  Cd 0.287 ± 0.006', 11.5),
             (256, 82, '<tspan fill="$ok">gate</tspan>     pass · 0.25 ms', 11.5)]
    for i, (x, y, t, sz) in enumerate(lines):
        s.append(f'<text x="{x}" y="{y}" font-size="{sz}" fill="$fg" xml:space="preserve" class="ln" '
                 f'style="animation-delay:{i*0.7:.1f}s">{t}</text>')
    s.append(T(440, 114, "R² 0.868 on unseen car designs", 9.5, "$dim", "end"))
    return "".join(s)


AERO_CSS = (".fl{stroke-dasharray:6 12;animation:fl 1.1s linear infinite}@keyframes fl{to{stroke-dashoffset:-18}}"
            ".pd{animation:pd 2.2s ease-in-out infinite}@keyframes pd{50%{opacity:.25}}"
            ".ln{opacity:0;animation:ln 7s infinite}@keyframes ln{0%{opacity:0}8%,85%{opacity:1}95%,100%{opacity:0}}")


FADE = (".em{opacity:0;animation:em 14s infinite}@keyframes em{0%,12%{opacity:1}14.3%,100%{opacity:0}}"
        ".bar{transform-box:fill-box;transform-origin:center;animation:eq .9s ease-in-out infinite alternate}"
        "@keyframes eq{from{transform:scaleY(.3)}to{transform:scaleY(1)}}"
        ".fr{opacity:0;animation:fr 2s steps(1) infinite}@keyframes fr{0%{opacity:1}25%{opacity:0}}"
        ".tk{opacity:0;animation:tk 2.5s steps(1) infinite}@keyframes tk{0%{opacity:1}20%{opacity:0}}"
        ".cf{transform-box:fill-box;transform-origin:left;animation:cf 2s ease-in-out infinite alternate}"
        "@keyframes cf{from{transform:scaleX(.45)}to{transform:scaleX(.92)}}")


def v_attune():
    s = []
    for lab, y in [("audio", 20), ("video", 60), ("text", 100)]:
        s.append(T(0, y + 4, lab, 10.5, "$dim"))
    for i in range(14):
        h = 6 + (i * 37 % 11) * 1.6
        s.append(f'<rect class="bar" x="{48+i*9}" y="{20-h/2:.1f}" width="5" height="{h:.1f}" rx="2" fill="$l3" '
                 f'style="animation-delay:{-i*0.13:.2f}s"/>')
    for i in range(4):
        x = 48 + i * 30
        s.append(f'<rect x="{x}" y="45" width="24" height="30" rx="3" fill="$panel2" stroke="$faint"/>')
        s.append(f'<circle cx="{x+12}" cy="58" r="7" fill="none" stroke="$dim"/>')
        s.append(f'<circle cx="{x+9.5}" cy="56" r="1" fill="$dim"/><circle cx="{x+14.5}" cy="56" r="1" fill="$dim"/>')
        curve = [-2, 2, 0, 2][i]
        s.append(f'<path d="M{x+8.5} 61 Q{x+12} {61+curve} {x+15.5} 61" fill="none" stroke="$dim"/>')
        s.append(f'<rect class="fr" x="{x}" y="45" width="24" height="30" rx="3" fill="none" stroke="$l3" '
                 f'stroke-width="1.5" style="animation-delay:{i*0.5}s"/>')
    x = 48
    for i, w in enumerate([18, 30, 14, 24, 20]):
        s.append(f'<rect x="{x}" y="93" width="{w}" height="14" rx="3" fill="$faint"/>')
        s.append(f'<rect class="tk" x="{x}" y="93" width="{w}" height="14" rx="3" fill="$l3" fill-opacity=".55" '
                 f'style="animation-delay:{i*0.5}s"/>')
        x += w + 4
    for i, y in enumerate([20, 60, 100]):
        d = f"M178 {y} C212 {y} 206 60 238 60"
        s.append(f'<path d="{d}" fill="none" stroke="$faint" stroke-width="1.5"/>')
        s.append(f'<path class="pulse" d="{d}" pathLength="100" fill="none" stroke="$l3" stroke-width="2" '
                 f'style="animation-delay:{-i*0.9:.1f}s;animation-duration:2.2s"/>')
    s.append('<circle cx="254" cy="60" r="16" fill="$panel2" stroke="$l3" stroke-width="1.5"/>')
    s.append(T(254, 63.5, "fuse", 9.5, "$dim", "middle"))
    s.append('<path d="M270 60 H290 M285 56 L291 60 L285 64" fill="none" stroke="$dim" stroke-width="1.5"/>')
    s.append(T(298, 24, "emotion", 9.5, "$dim"))
    s.append('<rect x="296" y="30" width="144" height="52" rx="8" fill="$panel2" stroke="$l3"/>')
    for i, em in enumerate(["neutral", "joy", "surprise", "sadness", "anger", "fear", "disgust"]):
        s.append(T(368, 62, em, 17, "$l3", "middle", 700, f'class="em" style="animation-delay:{i*2}s"'))
    s.append('<rect x="296" y="92" width="144" height="6" rx="3" fill="$faint"/>')
    s.append('<rect class="cf" x="296" y="92" width="144" height="6" rx="3" fill="$l3"/>')
    s.append(T(440, 114, e("≤ 6B params · no cloud APIs"), 10, "$dim", "end"))
    return "".join(s)


def hexpts(x, y, r):
    return " ".join(f"{x+r*math.cos(math.radians(60*k-90)):.1f},{y+r*math.sin(math.radians(60*k-90)):.1f}"
                    for k in range(6))


def v_hex():
    s = []
    r = 13.5
    hw = math.sqrt(3) * r
    rows = [3, 4, 5, 4, 3]
    cx, cy = 110, 59
    nums = iter([10, 2, 9, 12, 4, 11, 3, 4, 10, 9, 3, 11, 5, 6, 8])
    fixed = {(1, 1): 8, (1, 2): 5, (2, 2): 6}
    tints = ["$l1", "$l2", "$l3", "$l4", "$dim"]
    k = 0
    for ri, n in enumerate(rows):
        y = cy + (ri - 2) * 1.5 * r
        for i in range(n):
            x = cx + (i - (n - 1) / 2) * hw
            if (ri, i) == (2, 0):
                num = None
            else:
                num = fixed.get((ri, i)) or next(nums)
            s.append(f'<polygon points="{hexpts(x, y, r-0.8)}" fill="{tints[k%5]}" fill-opacity=".13" stroke="$faint"/>')
            k += 1
            if num:
                c = "$l3" if num in (6, 8) else "$dim"
                s.append(T(x, y + 3.5, str(num), 9.5, c, "middle", 700 if num in (6, 8) else None))
    vx, vy = cx, cy - r
    s.append(f'<path d="M{vx+8} {vy} L236 64" stroke="$l3" stroke-dasharray="3 3" stroke-opacity=".7"/>')
    s.append(f'<circle class="ping" cx="{vx}" cy="{vy}" r="9" fill="none" stroke="$l3" stroke-width="2"/>')
    s.append(f'<circle cx="{vx}" cy="{vy}" r="4.5" fill="$l3" stroke="$panel" stroke-width="1.5"/>')
    s.append('<rect x="236" y="4" width="204" height="110" rx="6" fill="$panel2" stroke="$faint"/>')
    lines = [(248, 24, "ws ▸ msgpack ▸ state", 10, "$dim"),
             (248, 46, "&gt; best opening", 12, "$fg"),
             (262, 66, "settle 6 · 8 · 5", 12, "$l3"),
             (262, 86, "pips 14 · rank 1 of 54", 11, "$dim")]
    for i, (x, y, t, sz, c) in enumerate(lines):
        s.append(T(x, y, t, sz, c, extra=f'class="ln" style="animation-delay:{i*0.6:.1f}s"'))
    s.append(T(248, 106, "&gt;", 12, "$fg"))
    s.append('<rect class="blink" x="260" y="96" width="7" height="12" fill="$l3"/>')
    return "".join(s)


HEX_CSS = (".ping{transform-box:fill-box;transform-origin:center;animation:ping 1.8s ease-out infinite}"
           "@keyframes ping{from{transform:scale(.5);opacity:1}to{transform:scale(1.9);opacity:0}}"
           ".ln{opacity:0;animation:ln 6s infinite}@keyframes ln{0%{opacity:0}8%,85%{opacity:1}95%,100%{opacity:0}}")


def v_lidar():
    s = []
    room = [(0, 0), (70, 0), (70, 18), (52, 18), (52, 40), (16, 40), (16, 26), (0, 26)]
    sc, zs = 0.95, 9

    def iso(x, y, z):
        return ((x - y) * 0.87 * sc, ((x + y) * 0.5 - z) * sc)
    allp = [iso(x, y, z) for x, y in room for z in (0, 5 * zs)]
    minx = min(p[0] for p in allp); maxx = max(p[0] for p in allp)
    miny = min(p[1] for p in allp); maxy = max(p[1] for p in allp)
    ox = 100 - (minx + maxx) / 2
    oy = 60 - (miny + maxy) / 2
    for x, y in room:
        a = iso(x, y, 0); b2 = iso(x, y, 5 * zs)
        s.append(f'<line x1="{a[0]+ox:.1f}" y1="{a[1]+oy:.1f}" x2="{b2[0]+ox:.1f}" y2="{b2[1]+oy:.1f}" '
                 f'stroke="$faint" stroke-dasharray="2 3"/>')
    for k in range(6):
        z = k * zs
        pts = [iso(x, y, z) for x, y in room]
        ps = " ".join(f"{px+ox:.1f},{py+oy:.1f}" for px, py in pts)
        dots = []
        for j in range(len(room)):
            (x1, y1), (x2, y2) = room[j], room[(j + 1) % len(room)]
            L = math.hypot(x2 - x1, y2 - y1)
            n = max(1, int(L / 6))
            for t in range(n):
                px, py = iso(x1 + (x2 - x1) * t / n, y1 + (y2 - y1) * t / n, z)
                dots.append(f'<circle cx="{px+ox:.1f}" cy="{py+oy:.1f}" r="1.1" fill="$l2"/>')
        s.append(f'<g class="sl" style="animation-delay:{k*0.45:.2f}s"><polygon points="{ps}" fill="$l2" '
                 f'fill-opacity=".07" stroke="$l2" stroke-opacity=".55"/>{"".join(dots)}</g>')
    # top-down sweep
    cx, cy, R = 340, 54, 46
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="$panel2" stroke="$faint"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{R*0.5}" fill="none" stroke="$faint" stroke-dasharray="2 3"/>')
    s.append(f'<path d="M{cx-R} {cy} H{cx+R} M{cx} {cy-R} V{cy+R}" stroke="$faint"/>')
    k = 0.9
    for j in range(len(room)):
        (x1, y1), (x2, y2) = room[j], room[(j + 1) % len(room)]
        L = math.hypot(x2 - x1, y2 - y1)
        n = max(1, int(L / 5))
        for t in range(n):
            px = cx + (x1 + (x2 - x1) * t / n - 35) * k
            py = cy + (y1 + (y2 - y1) * t / n - 20) * k
            s.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="1.3" fill="$l2" fill-opacity=".8"/>')
    ex = cx + R * math.cos(math.radians(-35)); ey = cy + R * math.sin(math.radians(-35))
    s.append(f'<path d="M{cx} {cy} L{cx+R} {cy} A{R} {R} 0 0 0 {ex:.1f} {ey:.1f} Z" fill="$l2" fill-opacity=".22">'
             f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="-360 {cx} {cy}" '
             f'dur="3s" repeatCount="indefinite"/></path>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="$l2"/>')
    s.append(T(cx, 114, "VL53L1X top view", 9.5, "$dim", "middle"))
    s.append(T(214, 114, "z slices", 9.5, "$dim", "end"))
    return "".join(s)


SLICE_CSS = ".sl{opacity:0;animation:sl 5s infinite}@keyframes sl{0%{opacity:0}6%,80%{opacity:1}92%,100%{opacity:0}}"


def v_fpga():
    s = []
    cols, rows, sz, gap = 12, 7, 10, 1.5
    s.append(f'<rect x="-3" y="5" width="{cols*(sz+gap)+4.5:.1f}" height="{rows*(sz+gap)+4.5:.1f}" rx="3" '
             f'fill="$panel2" stroke="$faint"/>')
    idx = 0
    for r in range(rows):
        for c in range(cols):
            if math.hypot(c - 8.2, r - 1.6) < 1.6:
                col, op = "$l2", 1.0
            elif r < 4:
                col, op = "$l1", 0.22 + 0.13 * r
            else:
                col, op = "$l4", 0.45 + 0.25 * ((c + r) % 2) - 0.05 * (r - 4)
            s.append(f'<rect class="tl" x="{c*(sz+gap):.1f}" y="{8+r*(sz+gap):.1f}" width="{sz}" height="{sz}" '
                     f'rx="1.5" fill="{col}" fill-opacity="{op:.2f}" style="animation-delay:{idx*0.05:.2f}s"/>')
            idx += 1
    s.append(T(0, 104, "framebuffer", 9.5, "$dim"))
    stages = ["decode", "dequant", "IDCT", "upsamp", "RGB"]
    for i, st in enumerate(stages):
        x = 160 + i * 57
        s.append(f'<rect x="{x}" y="8" width="50" height="30" rx="4" fill="$panel2" stroke="$faint"/>')
        s.append(f'<rect class="st" x="{x}" y="8" width="50" height="30" rx="4" fill="$l1" fill-opacity=".25" '
                 f'stroke="$l1" style="animation-delay:{i*0.8:.1f}s"/>')
        s.append(T(x + 25, 27, st, 10, "$fg", "middle"))
        if i < 4:
            s.append(f'<path d="M{x+51} 23 h5 M{x+53} 20 l3 3 l-3 3" fill="none" stroke="$dim"/>')
    s.append(T(160, 66, "SRAM", 10, "$dim"))
    for i in range(20):
        s.append(f'<rect x="{196+i*12}" y="56" width="10" height="12" rx="1.5" fill="$faint"/>')
    s.append('<rect x="196" y="56" width="10" height="12" rx="1.5" fill="$l1" fill-opacity=".6" stroke="$l1">'
             '<animateTransform attributeName="transform" type="translate" values="0 0;228 0" dur="3s" '
             'repeatCount="indefinite"/></rect>')
    s.append(T(160, 96, "clk", 10, "$dim"))
    s.append('<defs><clipPath id="ck"><rect x="196" y="80" width="244" height="24"/></clipPath></defs>')
    wave = "M176 98 " + "".join(f"h10 v-12 h10 v12 " for _ in range(14))
    s.append(f'<g clip-path="url(#ck)"><path d="{wave}" fill="none" stroke="$l1" stroke-width="1.5">'
             '<animateTransform attributeName="transform" type="translate" values="0 0;20 0" dur=".6s" '
             'repeatCount="indefinite"/></path></g>')
    s.append(T(440, 114, "882 blocks to 224×168 RGB, bit-exact", 9.5, "$dim", "end"))
    return "".join(s)


FPGA_CSS = (".tl{opacity:0;animation:tl 7s infinite}@keyframes tl{0%{opacity:0}2%,85%{opacity:1}95%,100%{opacity:0}}"
            ".st{opacity:0;animation:st 4s steps(1) infinite}@keyframes st{0%{opacity:1}20%{opacity:0}}")


def v_housing():
    s = ['<rect x="0" y="2" width="168" height="114" rx="8" fill="$panel2" stroke="$faint"/>',
         '<rect x="8" y="10" width="152" height="52" rx="5" fill="$l4" fill-opacity=".12"/>',
         '<path d="M68 38 L84 24 L100 38" fill="none" stroke="$l4" stroke-width="2" stroke-linejoin="round"/>',
         '<rect x="72" y="37" width="24" height="17" fill="none" stroke="$l4" stroke-width="2"/>',
         '<rect x="81" y="44" width="6" height="10" fill="$l4"/>',
         T(10, 79, "2 bed · near campus", 11, "$fg", weight=700),
         T(10, 93, "$$1,250/mo · 6 min walk", 10, "$dim"),
         '<rect x="10" y="99" width="148" height="13" rx="6.5" fill="none" stroke="$l4"/>',
         T(84, 108.5, "message landlord", 9, "$l4", "middle")]
    for i, d in enumerate(["M176 52 H246", "M246 66 H176"]):
        s.append(f'<path d="{d}" stroke="$faint" stroke-width="1.5"/>')
        s.append(f'<path class="pulse" d="{d}" pathLength="100" fill="none" stroke="$l4" stroke-width="2.5" '
                 f'style="animation-delay:{-i*1.4:.1f}s;animation-duration:2.4s"/>')
    s.append(T(211, 40, "socket.io", 9.5, "$dim", "middle"))
    s.append('<circle class="breathe" cx="196" cy="84" r="3.5" fill="$ok"/>')
    s.append(T(204, 87.5, "live", 9.5, "$dim"))
    s.append('<rect x="252" y="2" width="188" height="114" rx="10" fill="$panel2" stroke="$faint"/>')
    msgs = [("r", "still available?", 10), ("l", "yes! tour on sat?", 36), ("r", "works, see you then", 62)]
    for i, (side, t, y) in enumerate(msgs):
        w = len(t) * 6.2 + 16
        x = 432 - w if side == "r" else 260
        fill, tc = ("$l4", "$ink") if side == "r" else ("$faint", "$fg")
        s.append(f'<g class="bb" style="animation-delay:{i*1.2:.1f}s"><rect x="{x:.1f}" y="{y}" width="{w:.1f}" '
                 f'height="20" rx="10" fill="{fill}"/>{T(x+w/2, y+13.5, t, 10, tc, "middle")}</g>')
    s.append('<g class="bb" style="animation-delay:3.6s"><rect x="260" y="88" width="42" height="20" rx="10" fill="$faint"/>')
    for j in range(3):
        s.append(f'<circle class="dt" cx="{272+j*9}" cy="98" r="2.5" fill="$dim" style="animation-delay:{j*0.15:.2f}s"/>')
    s.append('</g>')
    return "".join(s)


HOUSE_CSS = (".bb{opacity:0;animation:bb 8s infinite}"
             "@keyframes bb{0%{opacity:0;transform:translateY(4px)}5%,85%{opacity:1;transform:translateY(0)}95%,100%{opacity:0}}"
             ".dt{animation:dt 1s ease-in-out infinite}@keyframes dt{50%{transform:translateY(-3px)}}")


def v_bag():
    s = ['<defs><clipPath id="belt"><rect x="0" y="0" width="300" height="118"/></clipPath></defs>',
         '<rect x="0" y="78" width="300" height="10" rx="5" fill="$faint"/>',
         '<line class="belt" x1="6" y1="83" x2="294" y2="83" stroke="$dim" stroke-dasharray="4 6"/>',
         '<circle cx="6" cy="83" r="7" fill="$panel2" stroke="$dim"/>',
         '<circle cx="294" cy="83" r="7" fill="$panel2" stroke="$dim"/>',
         '<line x1="140" y1="4" x2="140" y2="20" stroke="$dim" stroke-width="2"/>',
         '<rect x="128" y="18" width="24" height="12" rx="3" fill="$panel2" stroke="$l2"/>',
         '<polygon class="beam" points="133,30 147,30 162,56 118,56" fill="$l2" fill-opacity=".25"/>',
         T(158, 14, "scan", 9.5, "$dim"),
         '<g clip-path="url(#belt)">']
    for i in range(3):
        bag = ('<rect x="0" y="0" width="34" height="24" rx="4" fill="$panel2" stroke="$l2" stroke-width="1.5"/>'
               '<path d="M11 0 v-5 h12 v5" fill="none" stroke="$l2" stroke-width="1.5"/>' +
               "".join(f'<line x1="{8+j*3+(j>2)*2}" y1="8" x2="{8+j*3+(j>2)*2}" y2="17" stroke="$dim" '
                       f'stroke-width="{1.5 if j%2 else 1}"/>' for j in range(6)))
        s.append(f'<g transform="translate(0,54)"><g class="bag" style="animation-delay:{-i*2}s">{bag}</g></g>')
    s.append('</g>')
    s.append('<rect x="310" y="100" width="26" height="14" rx="3" fill="$panel2" stroke="$dim"/>')
    s.append('<g><path d="M323 100 V60 L352 46" fill="none" stroke="$dim" stroke-width="5" stroke-linecap="round" '
             'stroke-linejoin="round"/><circle cx="323" cy="60" r="4" fill="$l2"/>'
             '<path d="M350 40 l6 6 l-4 5 M350 40 l8 2" fill="none" stroke="$l2" stroke-width="2"/>'
             '<animateTransform attributeName="transform" type="rotate" values="-18 323 100;22 323 100;-18 323 100" '
             'dur="4s" repeatCount="indefinite"/></g>')
    for i, code in enumerate(["YYZ", "YVR", "YUL"]):
        y = 6 + i * 37
        s.append(f'<rect x="372" y="{y}" width="68" height="30" rx="4" fill="$panel2" stroke="$faint"/>')
        s.append(f'<rect class="st" x="372" y="{y}" width="68" height="30" rx="4" fill="$l2" fill-opacity=".2" '
                 f'stroke="$l2" style="animation-delay:{i*2}s;animation-duration:6s"/>')
        s.append(T(406, y + 19.5, f"bin {code}", 10, "$fg", "middle"))
    s.append(T(150, 112, "scan ▸ classify ▸ pick ▸ place", 9.5, "$dim", "middle"))
    return "".join(s)


BAG_CSS = (".bag{animation:bag 6s linear infinite}@keyframes bag{from{transform:translateX(-40px)}to{transform:translateX(300px)}}"
           ".belt{animation:belt .8s linear infinite}@keyframes belt{to{stroke-dashoffset:-10}}"
           ".beam{animation:beam 1.2s steps(2) infinite}@keyframes beam{50%{opacity:.2}}"
           ".st{opacity:0;animation:st 6s steps(1) infinite}@keyframes st{0%{opacity:1}33%{opacity:0}}")


CARDS = {
    "attune": lambda: card("3", "ML", "HCL-ML-Challenge", "on-device", "Attune",
                           "companion robot that reads emotion from voice, face and words",
                           ["Python", "MELD", "multimodal", "local inference"], v_attune(),
                           "Attune: emotion-aware companion robot that fuses audio, video and text on-device", FADE),
    "aero": lambda: card("3", "ML", "Aero-Surrogate", "hackathon", "Aero Surrogate",
                         "car drag in 0.25 ms, not hours of CFD, with a trust gate",
                         ["PyTorch", "FastAPI", "three.js", "Nemotron"], v_aero(),
                         "Aero Surrogate: neural surrogate that predicts car drag in about 0.25 ms, steered by a design agent",
                         AERO_CSS),
    "hexcoach": lambda: card("3", "ML", "Hex-Coach", "live game", "Hexcoach",
                             "rules engine and AI coach that reads live game state",
                             ["Python", "FastAPI", "TypeScript", "MessagePack"], v_hex(),
                             "Hexcoach: rules engine and AI coach for a Catan-style game", HEX_CSS),
    "lidar": lambda: card("2", "EMBEDDED", "Lidar-Spatial-Mapping-System", "hardware", "LIDAR Spatial Mapping",
                          "time-of-flight scans on an ARM Cortex-M4F, rebuilt in 3D",
                          ["C", "Cortex-M4F", "VL53L1X", "I²C", "Python"], v_lidar(),
                          "LIDAR spatial mapping system on an ARM Cortex-M4F", SLICE_CSS),
    "decompressor": lambda: card("1", "SILICON", "DE2-115 · 50 MHz", "in progress", "JPEG-Style Decompressor",
                                 "full decode pipeline in hardware, from bitstream to pixels",
                                 ["SystemVerilog", "DE2-115", "Quartus"], v_fpga(),
                                 "JPEG style image decompressor built in SystemVerilog on an FPGA", FPGA_CSS),
    "housinghub": lambda: card("4", "PRODUCT", "HousingHub", "full stack", "HousingHub",
                               "student housing marketplace with live messaging",
                               ["React", "TypeScript", "Express", "Socket.IO"], v_housing(),
                               "HousingHub: student housing marketplace with live messaging", HOUSE_CSS),
    "baggage": lambda: card("2", "EMBEDDED", "Automated-Airport-Baggage-System", "robotics",
                            "Automated Baggage Sorter",
                            "Quanser Q-Arm that sorts luggage by barcode scan",
                            ["Python", "Q-Arm", "sensors"], v_bag(),
                            "Automated baggage sorter: a robot arm that sorts luggage by barcode", BAG_CSS),
}


# ---------------------------------------------------------------- experience
def experience():
    W = 1000
    x0, x1 = 240, 968

    def mx(y, m, d=1):
        return x0 + ((y - 2024) * 12 + (m - 1) + (d - 1) / 30) / 36 * (x1 - x0)
    rows = [
        dict(col="$l3", org="Mac-AI", org2="McMaster AI Society", dates="Oct 2026 → now",
             role="Machine Learning Engineer", s=(2026, 10), e=None,
             bul=["building a rice price forecasting model for client Griffith Foods",
                  "monthly export price data, pitched as a prediction service for bulk buyers"]),
        dict(col="$l2", org="Hoskin Scientific", org2="co-op term", dates="May → Sep 2026",
             role="Calibration & Test Engineering Intern", s=(2026, 5), e=(2026, 10),
             bul=["built a report tool that cut a 10 minute job to under 1, used at every Canadian office",
                  "Isolation Forest anomaly detection for sensors drifting while still in spec",
                  "repaired 100+ scientific instruments at the board level"]),
        dict(col="$l1", org="Simcoe CC", org2="Barrie, ON", dates="Apr → Jun 2026",
             role="Full Stack Developer", s=(2026, 4), e=(2026, 7),
             bul=["SMS lead assistant used with real leads: Next.js, TypeScript, Prisma, Twilio",
                  "signed, idempotent webhooks and a live owner dashboard over Server-Sent Events"]),
        dict(col="$l4", org="BS Transportation", org2="Hamilton, ON", dates="May → Dec 2024",
             role="Operations & Technical Assistant", s=(2024, 5), e=(2025, 1),
             bul=["automated freight manifests in Python, saving 50+ hours a year"]),
    ]
    b = [T(24, 30, "CH · SOURCE", 11, "$dim", extra='letter-spacing="1"')]
    for yr in (2024, 2025, 2026, 2027):
        x = mx(yr, 1)
        b.append(T(x, 30, str(yr), 11, "$dim", "middle"))
    b.append(f'<line x1="{x0}" y1="40" x2="{x1}" y2="40" stroke="$faint"/>')
    top = 52
    for i, r in enumerate(rows):
        h = 58 + 18 * len(r["bul"])
        c = r["col"]
        b.append(T(24, top + 18, f"CH{i}", 11, c, weight=700))
        b.append(T(58, top + 18, e(r["org"]), 14, "$fg", weight=700))
        b.append(T(58, top + 36, e(r["org2"]), 10.5, "$dim"))
        b.append(T(58, top + 52, e(r["dates"]), 10.5, c))
        yl, yh = top + 20, top + 6
        xs = mx(*r["s"])
        xe = mx(*r["e"]) if r["e"] else x1
        b.append(f'<rect x="{xs:.1f}" y="{yh}" width="{xe-xs:.1f}" height="{yl-yh}" fill="{c}" fill-opacity=".14"/>')
        if r["e"]:
            pts = f"{x0},{yl} {xs:.1f},{yl} {xs:.1f},{yh} {xe:.1f},{yh} {xe:.1f},{yl} {x1},{yl}"
        else:
            pts = f"{x0},{yl} {xs:.1f},{yl} {xs:.1f},{yh} {x1},{yh}"
        b.append(f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="1.6"/>')
        b.append(T(x0, top + 44, e(r["role"]), 12.5, "$fg", weight=700))
        for j, bl in enumerate(r["bul"]):
            b.append(f'<text x="{x0}" y="{top+62+18*j}" font-size="12" fill="$dim"><tspan fill="{c}">›</tspan> {e(bl)}</text>')
        top += h
        if i < len(rows) - 1:
            b.append(f'<line x1="24" y1="{top-8}" x2="{x1}" y2="{top-8}" stroke="$faint" stroke-dasharray="2 4"/>')
    H = top + 6
    nx = mx(2026, 10, 27)
    b.append(f'<line x1="{nx:.1f}" y1="40" x2="{nx:.1f}" y2="{H-10}" stroke="$dim" stroke-dasharray="3 3"/>')
    b.append(T(nx - 6, 30, "now", 10, "$dim", "end"))
    b.append(f'<line class="scan" x1="{x0}" y1="44" x2="{x0}" y2="{H-10}" stroke="$l4" stroke-opacity=".45" stroke-width="1.5"/>')
    body = panel(W, H) + "".join(b)
    css = (".scan{animation:scan 9s linear infinite}"
           f"@keyframes scan{{from{{transform:translateX(0)}}to{{transform:translateX({x1-x0}px)}}}}")
    label = ("Experience: Machine Learning Engineer at Mac-AI (2026 to now), Calibration and Test Engineering Intern "
             "at Hoskin Scientific (2026), Full Stack Developer at Simcoe CC (2026), Operations and Technical Assistant at BS Transportation (2024)")
    return svg(W, H, label, body, css)


# ---------------------------------------------------------------- stack
def stack():
    W = 1000
    layers = [
        ("4", "PRODUCT", ["TypeScript", "React", "Next.js", "FastAPI", "Socket.IO"], "→ HousingHub · Simcoe CC · Aero UI"),
        ("3", "ML", ["Python", "PyTorch", "scikit-learn", "pandas"], "→ Attune · Aero Surrogate · Mac-AI"),
        ("2", "EMBEDDED", ["C", "Cortex-M4F", "UART", "I²C", "PCB debug"], "→ LIDAR · Baggage Sorter"),
        ("1", "SILICON", ["SystemVerilog", "FPGA", "DE2-115", "Quartus"], "→ JPEG Decompressor"),
    ]
    b = [T(24, 30, "cross-section · signal enters at silicon, leaves as a product", 11, "$dim")]
    y0, step, h = 48, 72, 58
    bottom = y0 + 3 * step + h
    d = f"M44 {bottom} V{y0}"
    b.append(f'<path d="{d}" stroke="$faint" stroke-width="3"/>')
    b.append(f'<path class="pulse" d="{d}" pathLength="100" fill="none" stroke="$l4" stroke-width="3" '
             f'style="animation-duration:3s"/>')
    for k, (n, name, tools, used) in enumerate(layers):
        y = y0 + k * step
        c = LAYER[n]
        poly = f"98,{y} 976,{y} 958,{y+h} 80,{y+h}"
        b.append(f'<line x1="44" y1="{y+h/2}" x2="86" y2="{y+h/2}" stroke="$faint" stroke-width="2"/>')
        b.append(f'<circle cx="44" cy="{y+h/2}" r="5" fill="$panel" stroke="{c}" stroke-width="2"/>')
        b.append(f'<polygon points="{poly}" fill="$panel2" stroke="$faint"/>')
        b.append(f'<polygon class="hl" points="{poly}" fill="{c}" fill-opacity=".06" stroke="{c}" stroke-width="1.5" '
                 f'style="animation-delay:{(3-k)*0.75:.2f}s"/>')
        b.append(T(110, y + 34, f"L{n}", 13, c, weight=700))
        b.append(T(142, y + 34, name, 12, "$fg", extra='letter-spacing="2"'))
        x = 262
        for t in tools:
            w = len(t) * 7.4 + 20
            b.append(f'<rect x="{x:.0f}" y="{y+18}" width="{w:.0f}" height="22" rx="4" fill="{c}" fill-opacity=".1" stroke="{c}" stroke-opacity=".6"/>')
            b.append(T(x + w / 2, y + 33, e(t), 11.5, "$fg", "middle"))
            x += w + 8
        b.append(T(944, y + 34, e(used), 11, "$dim", "end"))
    H = bottom + 20
    body = panel(W, H) + "".join(b)
    css = ".hl{opacity:0;animation:hl 3s infinite}@keyframes hl{0%{opacity:0}6%{opacity:1}32%{opacity:0}}"
    label = ("Tech stack by layer. Product: TypeScript, React, Next.js, FastAPI, Socket.IO. ML: Python, PyTorch, "
             "scikit-learn, pandas. Embedded: C, Cortex-M4F, UART, I2C. Silicon: SystemVerilog, FPGA, Quartus.")
    # pulse should travel upward: path drawn bottom to top already
    return svg(W, H, label, body, css)


def main(out):
    os.makedirs(out, exist_ok=True)
    items = {"header": header, "experience": experience, "stack": stack}
    items.update({f"card-{k}": v for k, v in CARDS.items()})
    items["footer"] = footer
    for k, (t, n) in SECTIONS.items():
        items[f"section-{k}"] = (lambda t=t, n=n: section(t, n))
    for name, fn in items.items():
        tpl = Template(fn())
        for th, vals in THEMES.items():
            with open(os.path.join(out, f"{name}-{th}.svg"), "w") as f:
                f.write(tpl.substitute(vals))


if __name__ == "__main__":
    main(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets"))
