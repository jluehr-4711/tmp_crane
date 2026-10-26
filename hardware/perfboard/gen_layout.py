#!/usr/bin/env python3
"""Perfboard layout for the crosstrainer adapter board (5x7 cm proto board, 18 x 24 holes, 2.54 mm).
Columns x = 1..18 (left -> right), rows y = 1..24 (top -> bottom), seen from the component side.
Every hole is assigned to a net; links (bottom side, bare wire / solder bridge) and jumpers (top side,
insulated wire) are listed explicitly. The script checks that each net is one connected graph and that
no hole carries two nets, then renders an SVG (top view, bottom links drawn as seen through the board).
"""
import sys, os
from collections import defaultdict

COLS, ROWS = 18, 24

# ---- components: name -> (value, [(hole, pin_label, net), ...], body description) ----
components = {
 "H1": ("1x8 pin header, Dupont to ESP32", [((17,3),"1 5V","ESP_5V"),((17,4),"2 G16","UART_RX"),((17,5),"3 G2","LED"),
         ((17,6),"4 G27","PWM_OUT"),((17,7),"5 G34","ADC_A"),((17,8),"6 G25","CAPTURE"),((17,9),"7 G26","SPEED_IN"),((17,10),"8 GND","GND")], "header"),
 "D1": ("1N5819 (band = cathode, right)", [((9,2),"A","5V_MACH"),((14,2),"K","ESP_5V")], "axial"),
 "R1": ("100k", [((7,3),"1","5V_MACH"),((7,7),"2","ADC_A")], "axial"),
 "R2": ("10k",  [((7,7),"1","ADC_A"),((7,11),"2","GND")], "axial"),
 "R3": ("10k",  [((10,4),"1","DOUT"),((10,8),"2","CAPTURE")], "axial"),
 "R4": ("15k",  [((10,8),"1","CAPTURE"),((10,12),"2","GND")], "axial"),
 "R5": ("10k",  [((13,5),"1","SPEED"),((13,9),"2","SPEED_IN")], "axial"),
 "R6": ("15k",  [((13,9),"1","SPEED_IN"),((13,13),"2","GND")], "axial"),
 "R8": ("4k7",  [((2,16),"1","5V_MACH"),((6,16),"2","Q_C")], "axial"),
 "Q1": ("BC547, flat side towards the bottom edge (pins C B E left->right)", [((7,17),"C","Q_C"),((8,17),"B","Q_B"),((9,17),"E","GND")], "to92"),
 "R7": ("1k",   [((8,19),"1","Q_B"),((12,19),"2","PWM_OUT")], "axial"),
 "JP1": ("2-pin header + jumper cap (DRIVE enable)", [((7,20),"1","Q_C"),((7,21),"2","DOUT")], "header"),
 # pigtail wires soldered from the top (JST SM cables)
 "J1": ("plug A pigtail (JST SM 4p female)", [((2,17),"green 5V","5V_MACH"),((3,21),"red DOUT","DOUT"),((4,19),"yellow","SPEED"),((5,13),"black","GND")], "wire"),
 "J2": ("console pass-through pigtail (JST SM 4p male)", [((2,18),"green","5V_MACH"),((3,22),"red","DOUT"),((4,20),"yellow","SPEED"),((5,14),"black","GND")], "wire"),
}
# NOTE on J1/J2 pins 3/4: the schematic calls the yellow wire SPEED and black GND as a working assumption.
# If session 3 shows it the other way round, swap the yellow and black pigtail wires at (4,19)/(4,20) <-> (5,13)/(5,14).

# ---- bottom-side links: straight runs of bare wire or chained solder bridges, (from, to, net) ----
links = [
 # rails on the left
 ((2,2),(2,18),"5V_MACH"), ((3,4),(3,22),"DOUT"), ((4,5),(4,20),"SPEED"), ((5,6),(5,14),"GND"),
 # 5V to R1 top and D1 anode
 ((2,2),(7,2),"5V_MACH"), ((7,2),(7,3),"5V_MACH"), ((7,2),(9,2),"5V_MACH"),
 # D1 cathode to header 5V
 ((14,2),(17,2),"ESP_5V"), ((17,2),(17,3),"ESP_5V"),
 # DOUT and SPEED to divider tops
 ((3,4),(10,4),"DOUT"), ((4,5),(13,5),"SPEED"),
 # divider taps to header
 ((7,7),(17,7),"ADC_A"), ((10,8),(17,8),"CAPTURE"), ((13,9),(17,9),"SPEED_IN"),
 # GND bus (row 14) and drops
 ((5,14),(17,14),"GND"), ((7,11),(7,14),"GND"), ((10,12),(10,14),"GND"), ((13,13),(13,14),"GND"),
 ((17,10),(17,14),"GND"), ((9,17),(9,14),"GND"),
 # driver
 ((6,16),(7,16),"Q_C"), ((7,16),(7,17),"Q_C"), ((7,17),(7,20),"Q_C"), ((3,21),(7,21),"DOUT"),
 ((8,17),(8,19),"Q_B"),
]
# ---- top-side insulated jumpers ----
jumpers = [ ((17,6),(12,19),"PWM_OUT") ]

# ---------------- validation ----------------
def run(a, b):
    (x1,y1),(x2,y2) = a, b
    assert x1 == x2 or y1 == y2, f"link {a}-{b} is not straight"
    if x1 == x2: return [(x1, y) for y in range(min(y1,y2), max(y1,y2)+1)]
    return [(x, y1) for x in range(min(x1,x2), max(x1,x2)+1)]

owner = {}   # hole -> net  (holes electrically used: pins, link ends, link interior = also that net!)
def claim(h, net, what):
    assert 1 <= h[0] <= COLS and 1 <= h[1] <= ROWS, f"{what}: hole {h} off board"
    if h in owner and owner[h] != net:
        raise SystemExit(f"CONFLICT at hole {h}: {owner[h]} vs {net} ({what})")
    owner[h] = net

pins = defaultdict(list)       # hole -> [(comp, pin)]
for c, (val, plist, kind) in components.items():
    for h, p, net in plist:
        claim(h, net, f"{c}.{p}"); pins[h].append((c, p))
for a, b, net in links:
    for h in run(a, b): claim(h, net, f"link {a}-{b}")   # a bare bottom wire touches every pad it crosses
for a, b, net in jumpers:
    claim(a, net, "jumper"); claim(b, net, "jumper")

# bodies: holes under an axial body must not carry a *different* net's used pad (a wire soldered there)
def body_holes(plist):
    (x1,y1),(x2,y2) = plist[0][0], plist[1][0]
    return [h for h in run((x1,y1),(x2,y2)) if h not in ((x1,y1),(x2,y2))]
for c, (val, plist, kind) in components.items():
    if kind == "axial":
        for h in body_holes(plist):
            if h in pins: raise SystemExit(f"{c} body covers a used pad {h} ({pins[h]})")

# connectivity per net (union-find over holes)
parent = {}
def find(h):
    parent.setdefault(h, h)
    while parent[h] != h: parent[h] = parent[parent[h]]; h = parent[h]
    return h
def union(a, b): parent[find(a)] = find(b)
for a, b, net in links:
    hs = run(a, b)
    for h1, h2 in zip(hs, hs[1:]): union(h1, h2)
for a, b, net in jumpers: union(a, b)
nets = defaultdict(set)
for h, n in owner.items(): nets[n].add(h)
problems = []
for n, hs in nets.items():
    roots = {find(h) for h in hs}
    if len(roots) > 1: problems.append(f"net {n} is split into {len(roots)} islands: {sorted(hs)}")
if problems: raise SystemExit("\n".join(problems))

# compare with the schematic's intent: pins per net
expected = {
 "5V_MACH": {"J1.green 5V","J2.green","D1.A","R1.1","R8.1"}, "ESP_5V": {"D1.K","H1.1 5V"},
 "DOUT": {"J1.red DOUT","J2.red","R3.1","JP1.2"}, "SPEED": {"J1.yellow","J2.yellow","R5.1"},
 "GND": {"J1.black","J2.black","R2.2","R4.2","R6.2","Q1.E","H1.8 GND"},
 "ADC_A": {"R1.2","R2.1","H1.5 G34"}, "CAPTURE": {"R3.2","R4.1","H1.6 G25"}, "SPEED_IN": {"R5.2","R6.1","H1.7 G26"},
 "PWM_OUT": {"H1.4 G27","R7.2"}, "Q_B": {"R7.1","Q1.B"}, "Q_C": {"R8.2","Q1.C","JP1.1"}, "UART_RX": {"H1.2 G16"}, "LED": {"H1.3 G2"},
}
actual = defaultdict(set)
for h, lst in pins.items():
    for c, p in lst: actual[owner[h]].add(f"{c}.{p}")
for n in sorted(set(expected) | set(actual)):
    if expected.get(n, set()) != actual.get(n, set()):
        raise SystemExit(f"net {n}: expected {sorted(expected.get(n,[]))}, layout has {sorted(actual.get(n,[]))}")
print("layout OK:", len(components), "components,", len(links), "bottom links,", len(jumpers), "top jumpers,", len(nets), "nets")

# ---------------- render ----------------
P = 22            # px per 2.54 mm
OX, OY = 150, 90   # origin
def X(x): return OX + (x - 1) * P
def Y(y): return OY + (y - 1) * P
netcol = {"5V_MACH":"#2e8b57","ESP_5V":"#1f77b4","DOUT":"#d62728","SPEED":"#e0b000","GND":"#222","ADC_A":"#17becf",
          "CAPTURE":"#9467bd","SPEED_IN":"#8c564b","PWM_OUT":"#ff7f0e","Q_B":"#e377c2","Q_C":"#7f7f7f","UART_RX":"#aaa","LED":"#aaa"}
W = OX + COLS * P + 300; H = OY + ROWS * P + 40
out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif" font-size="11">',
       f'<rect width="{W}" height="{H}" fill="#fff"/>',
       f'<text x="20" y="24" font-size="16" font-weight="bold">Crosstrainer adapter board – perfboard layout, component side view (5 x 7 cm, 18 x 24 holes)</text>',
       f'<text x="20" y="42" fill="#444">Solid coloured lines = bare wire / solder bridges on the BOTTOM side (seen through the board). Dashed = insulated wire on the TOP side. Hole (1,1) is top-left.</text>',
       f'<rect x="{OX-14}" y="{OY-14}" width="{COLS*P+6}" height="{ROWS*P+6}" fill="#d9c9a3" stroke="#7a6a45" stroke-width="2" rx="4"/>']
for x in range(1, COLS+1):
    out.append(f'<text x="{X(x)}" y="{OY-18}" text-anchor="middle" font-size="9" fill="#555">{x}</text>')
for y in range(1, ROWS+1):
    out.append(f'<text x="{OX-20}" y="{Y(y)+3}" text-anchor="end" font-size="9" fill="#555">{y}</text>')
for x in range(1, COLS+1):
    for y in range(1, ROWS+1):
        out.append(f'<circle cx="{X(x)}" cy="{Y(y)}" r="3.2" fill="#fff" stroke="#8a7a55" stroke-width="1"/>')
# bottom links
for a, b, net in links:
    out.append(f'<line x1="{X(a[0])}" y1="{Y(a[1])}" x2="{X(b[0])}" y2="{Y(b[1])}" stroke="{netcol[net]}" stroke-width="4" stroke-linecap="round" opacity="0.85"/>')
# components
for c, (val, plist, kind) in components.items():
    hs = [p[0] for p in plist]
    if kind == "axial":
        (x1,y1),(x2,y2) = hs
        cx, cy = (X(x1)+X(x2))/2, (Y(y1)+Y(y2))/2
        horiz = y1 == y2
        bw, bh = (2.6*P, 0.7*P) if horiz else (0.7*P, 2.6*P)
        out.append(f'<line x1="{X(x1)}" y1="{Y(y1)}" x2="{X(x2)}" y2="{Y(y2)}" stroke="#333" stroke-width="2"/>')
        fill = "#f6e7a1" if c.startswith("R") else "#333"
        out.append(f'<rect x="{cx-bw/2}" y="{cy-bh/2}" width="{bw}" height="{bh}" fill="{fill}" stroke="#333" rx="3"/>')
        if c == "D1": out.append(f'<rect x="{cx+bw/2-8}" y="{cy-bh/2}" width="5" height="{bh}" fill="#ddd"/>')
        tcol = "#fff" if c == "D1" else "#222"
        out.append(f'<text x="{cx}" y="{cy+4 if horiz else cy+4}" text-anchor="middle" font-size="10" font-weight="bold" fill="{tcol}" {"" if horiz else f"transform=\'rotate(-90 {cx} {cy})\'"}>{c} {val.split()[0]}</text>')
    elif kind == "to92":
        xs = [h[0] for h in hs]; y = hs[0][1]
        cx = (X(min(xs))+X(max(xs)))/2
        out.append(f'<path d="M{X(min(xs))-10} {Y(y)+9} L{X(max(xs))+10} {Y(y)+9} A{1.25*P} {1.25*P} 0 0 0 {X(min(xs))-10} {Y(y)+9} z" fill="#444" stroke="#111"/>')
        out.append(f'<text x="{cx}" y="{Y(y)-8}" text-anchor="middle" font-size="10" font-weight="bold" fill="#fff">Q1 BC547</text>')
        for h, p, net in plist: out.append(f'<text x="{X(h[0])}" y="{Y(h[1])+22}" text-anchor="middle" font-size="9" fill="#222">{p}</text>')
    elif kind == "header":
        for h, p, net in plist:
            out.append(f'<rect x="{X(h[0])-9}" y="{Y(h[1])-9}" width="18" height="18" fill="#2b2b2b" stroke="#000"/>')
            out.append(f'<rect x="{X(h[0])-2.5}" y="{Y(h[1])-2.5}" width="5" height="5" fill="#d4af37"/>')
            if c == "H1": out.append(f'<text x="{X(h[0])+14}" y="{Y(h[1])+4}" font-size="10" fill="#222">{p}</text>')
        if c == "JP1":
            out.append(f'<text x="{X(hs[0][0])+14}" y="{Y(hs[0][1])+12}" font-size="10" font-weight="bold" fill="#222">JP1 DRIVE enable</text>')
        if c == "H1":
            out.append(f'<text x="{X(17)-14}" y="{Y(2)-6}" font-size="10" font-weight="bold" fill="#222">H1 → ESP32 (Dupont)</text>')
    elif kind == "wire":
        for h, p, net in plist:
            out.append(f'<path d="M{X(h[0])} {Y(h[1])} C {X(h[0])-30} {Y(h[1])}, {OX-40} {Y(h[1])}, {OX-50} {Y(h[1])}" stroke="{netcol[net]}" stroke-width="3" fill="none" stroke-dasharray="6 3"/>')
            out.append(f'<text x="{OX-52}" y="{Y(h[1])+4}" text-anchor="end" font-size="9" fill="#222">{c} {p}</text>')
# jumpers (top)
for a, b, net in jumpers:
    out.append(f'<path d="M{X(a[0])} {Y(a[1])} C {X(a[0])-40} {Y(a[1])+40}, {X(b[0])+40} {Y(b[1])-60}, {X(b[0])} {Y(b[1])}" stroke="{netcol[net]}" stroke-width="3" fill="none" stroke-dasharray="7 4"/>')
    out.append(f'<text x="{(X(a[0])+X(b[0]))/2+20}" y="{(Y(a[1])+Y(b[1]))/2}" font-size="10" fill="{netcol[net]}">top jumper {net}</text>')
# pads with pins: mark
for h, lst in pins.items():
    out.append(f'<circle cx="{X(h[0])}" cy="{Y(h[1])}" r="4.5" fill="none" stroke="#000" stroke-width="1.5"/>')
# legend
lx, ly = OX + COLS*P + 30, OY
out.append(f'<text x="{lx}" y="{ly}" font-size="12" font-weight="bold">Nets</text>')
for i, (n, col) in enumerate(netcol.items()):
    out.append(f'<line x1="{lx}" y1="{ly+18+i*16}" x2="{lx+30}" y2="{ly+18+i*16}" stroke="{col}" stroke-width="4"/>')
    out.append(f'<text x="{lx+38}" y="{ly+22+i*16}">{n}</text>')
ly2 = ly + 18 + len(netcol)*16 + 20
notes = ["Build order:", "1. bottom rails cols 2-5 and GND bus row 14 (bare wire)", "2. resistors, diode (band right), Q1 (flat side down)",
         "3. headers H1 (col 17) and JP1 (col 7)", "4. remaining bottom links, then the top jumper", "5. pigtail wires J1/J2 from the top",
         "6. check with meter: no short 5V_MACH-GND, DOUT-GND", "", "Pins 3/4 of J1/J2 (yellow/black):", "swap the two pigtail pairs if", "session 3 shows yellow = GND."]
for i, t in enumerate(notes):
    out.append(f'<text x="{lx}" y="{ly2+i*15}" font-size="11" {"font-weight=\'bold\'" if t.endswith(":") else ""}>{t}</text>')
out.append('</svg>')
d = os.path.dirname(__file__) or "."
open(os.path.join(d, "layout.svg"), "w").write("\n".join(out))
# link table
with open(os.path.join(d, "links.md"), "w") as f:
    f.write("# Bottom-side links (bare wire / solder bridges)\n\n| from | to | net |\n|---|---|---|\n")
    for a, b, net in links: f.write(f"| ({a[0]},{a[1]}) | ({b[0]},{b[1]}) | {net} |\n")
    f.write("\n# Top-side insulated jumpers\n\n| from | to | net |\n|---|---|---|\n")
    for a, b, net in jumpers: f.write(f"| ({a[0]},{a[1]}) | ({b[0]},{b[1]}) | {net} |\n")
    f.write("\n# Component holes\n\n| ref | value | holes |\n|---|---|---|\n")
    for c, (val, plist, kind) in components.items():
        f.write(f"| {c} | {val} | " + ", ".join(f"({h[0]},{h[1]}) {p}" for h, p, net in plist) + " |\n")
print("wrote layout.svg, links.md")
