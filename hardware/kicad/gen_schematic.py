#!/usr/bin/env python3
"""Generate adapter-board schematic (KiCad 9 .kicad_sch) for the crosstrainer ESP32 project.
Symbols are pulled from the installed KiCad libraries; the ESP32 DevKit symbol is defined here.
Run: python3 gen_schematic.py && kicad-cli sch erc adapter.kicad_sch && kicad-cli sch export svg ...
"""
import re, uuid, os, sys

LIB = "/usr/share/kicad/symbols"

# ---------- minimal s-expression helpers ----------
def extract_symbol(libfile, name):
    """Return the full text of (symbol "name" ...) incl. sub-units, from a .kicad_sym file."""
    s = open(os.path.join(LIB, libfile), encoding="utf-8").read()
    key = f'(symbol "{name}"'
    i = s.find(key + " ")
    if i < 0: i = s.find(key + "\n")
    if i < 0: raise SystemExit(f"symbol {name} not in {libfile}")
    depth = 0; j = i; instr = False
    while True:
        c = s[j]
        if c == '"' and s[j-1] != '\\': instr = not instr
        elif not instr:
            if c == '(': depth += 1
            elif c == ')':
                depth -= 1
                if depth == 0: return s[i:j+1]
        j += 1

def pins_of(symtext):
    """pin number -> (x, y) connection point in library coords (y up)."""
    out = {}
    for m in re.finditer(r'\(pin\s+\w+\s+\w+\s*\(at\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\).*?\(number\s+"([^"]+)"', symtext, re.S):
        out[m.group(4)] = (float(m.group(1)), float(m.group(2)))
    return out

def U(): return str(uuid.uuid4())

# ---------- library symbols ----------
lib_symbols = {}
def use(libfile, name):
    txt = extract_symbol(libfile, name)
    lid = f"{libfile[:-10]}:{name}"
    txt = txt.replace(f'(symbol "{name}"', f'(symbol "{lid}"', 1)
    lib_symbols[lid] = txt
    return lid, pins_of(txt)

R_ID, R_PINS = use("Device.kicad_sym", "R")
D_ID, D_PINS = use("Device.kicad_sym", "D_Schottky")
Q_ID, Q_PINS = use("Device.kicad_sym", "Q_NPN")
JP_ID, JP_PINS = use("Jumper.kicad_sym", "Jumper_2_Open")
C4_ID, C4_PINS = use("Connector_Generic.kicad_sym", "Conn_01x04")
GND_ID, GND_PINS = use("power.kicad_sym", "GND")
FLG_ID, FLG_PINS = use("power.kicad_sym", "PWR_FLAG")

# custom ESP32 DevKit symbol: pins on the left, 2.54 pitch
ESP_PINS_DEF = [("5V", "5V/VIN", "power_in"), ("GND", "GND", "power_in"), ("34", "GPIO34 (ADC A)", "bidirectional"),
                ("26", "GPIO26 (speed)", "bidirectional"), ("25", "GPIO25 (capture)", "bidirectional"),
                ("27", "GPIO27 (PWM out)", "bidirectional"), ("16", "GPIO16 (UART2 RX)", "bidirectional"), ("2", "GPIO2 (LED)", "bidirectional")]
ESP_ID = "Local:ESP32_DevKit"
def esp_symbol():
    n = len(ESP_PINS_DEF); h = (n + 1) * 2.54
    body = f'''(symbol "{ESP_ID}" (pin_names (offset 1.016)) (exclude_from_sim no) (in_bom yes) (on_board yes)
  (property "Reference" "U" (at 0 {h/2+1.27:.2f} 0) (effects (font (size 1.27 1.27))))
  (property "Value" "ESP32 DevKit (classic)" (at 0 {-h/2-1.27:.2f} 0) (effects (font (size 1.27 1.27))))
  (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
  (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
  (symbol "ESP32_DevKit_0_1" (rectangle (start -7.62 {h/2:.2f}) (end 20.32 {-h/2:.2f}) (stroke (width 0.254) (type default)) (fill (type background))))
  (symbol "ESP32_DevKit_1_1"
'''
    pins = {}
    for i, (num, name, typ) in enumerate(ESP_PINS_DEF):
        y = h/2 - (i + 1) * 2.54
        body += f'    (pin {typ} line (at -12.7 {y:.2f} 0) (length 5.08) (name "{name}" (effects (font (size 1.27 1.27)))) (number "{num}" (effects (font (size 1.27 1.27)))))\n'
        pins[num] = (-12.7, y)
    body += "  )\n)"
    return body, pins
esp_txt, ESP_PINS = esp_symbol()
lib_symbols[ESP_ID] = esp_txt

# ---------- placement ----------
items = []   # schematic body text pieces
def place(lid, pins, ref, value, x, y, rot=0, props=None, value_off=(2.54, 0), ref_off=(2.54, -2.54), hide_value=False, hide_ref=False):
    """Place symbol; returns pin number -> schematic (X, Y). Only rot 0/180 supported."""
    props = props or {}
    p = f'''(symbol (lib_id "{lid}") (at {x:.2f} {y:.2f} {rot}) (unit 1) (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{U()}")
  (property "Reference" "{ref}" (at {x+ref_off[0]:.2f} {y+ref_off[1]:.2f} 0) (effects (font (size 1.27 1.27)) (justify left){" (hide yes)" if hide_ref else ""}))
  (property "Value" "{value}" (at {x+value_off[0]:.2f} {y+value_off[1]:.2f} 0) (effects (font (size 1.27 1.27)) (justify left){" (hide yes)" if hide_value else ""}))
  (property "Footprint" "" (at {x:.2f} {y:.2f} 0) (effects (font (size 1.27 1.27)) (hide yes)))
  (property "Datasheet" "" (at {x:.2f} {y:.2f} 0) (effects (font (size 1.27 1.27)) (hide yes)))
'''
    for k, v in props.items():
        p += f'  (property "{k}" "{v}" (at {x:.2f} {y:.2f} 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
    for num in pins:
        p += f'  (pin "{num}" (uuid "{U()}"))\n'
    p += f'  (instances (project "adapter" (path "/{ROOT}" (reference "{ref}") (unit 1))))\n)'
    items.append(p)
    out = {}
    for num, (px, py) in pins.items():
        if rot == 0:   out[num] = (round(x + px, 2), round(y - py, 2))
        elif rot == 180: out[num] = (round(x - px, 2), round(y + py, 2))
        elif rot == 90:  out[num] = (round(x - py, 2), round(y - px, 2))
        elif rot == 270: out[num] = (round(x + py, 2), round(y + px, 2))
    return out

def wire(a, b):
    items.append(f'(wire (pts (xy {a[0]:.2f} {a[1]:.2f}) (xy {b[0]:.2f} {b[1]:.2f})) (stroke (width 0) (type default)) (uuid "{U()}"))')
def wires(*pts):
    for a, b in zip(pts, pts[1:]): wire(a, b)
def label(name, at, rot=0, just="left"):
    items.append(f'(label "{name}" (at {at[0]:.2f} {at[1]:.2f} {rot}) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify {just} bottom)) (uuid "{U()}"))')
def text(s, at, size=1.27, bold=False):
    s = s.replace('"', "'")
    items.append(f'(text "{s}" (exclude_from_sim no) (at {at[0]:.2f} {at[1]:.2f} 0) (effects (font (size {size} {size}){" (bold yes)" if bold else ""}) (justify left bottom)) (uuid "{U()}"))')
def gnd(at, ref):
    """GND power symbol with its pin at 'at' (pin points up, symbol hangs below)."""
    px, py = GND_PINS["1"]
    place(GND_ID, GND_PINS, ref, "GND", at[0] - px, at[1] + py, value_off=(0, 3.5), ref_off=(0, 0), hide_value=False, hide_ref=True)
def junction(at):
    items.append(f'(junction (at {at[0]:.2f} {at[1]:.2f}) (diameter 0) (color 0 0 0 0) (uuid "{U()}"))')
def stub(pin_xy, dx, name, just="left"):
    """short horizontal wire from a pin plus a net label at its end."""
    end = (pin_xy[0] + dx, pin_xy[1]); wire(pin_xy, end); label(name, end, just=just)
    return end

ROOT = U()

# ---- title / notes ----
text("Crosstrainer adapter board: ESP32 <-> console link (4-pin SENSOR plug at the top of the column)", (15, 15), 2.0, True)
text("SNIFF mode: console plugged into J2, JP1 open, ESP32 listens (GPIO25/26/34). DRIVE mode: console unplugged, JP1 closed, ESP32 drives DOUT via Q1.", (15, 19))
text("Wire colours at plug A: pin1 green = 5V (from brake board), pin2 red = DOUT (brake command), pin3/pin4 yellow+black = GND and speed pulse, order to be measured (session 3).", (15, 23))
text("Never close JP1 while the console is plugged in. All machine lines reach the ESP32 only through dividers (max 3.3 V).", (15, 27))

# ---- connectors on the left (pins point to the right after rot 180) ----
# Conn_01x04 pins are on the left side in the lib (x=-5.08). rot 180 flips them to the right side.
J1 = place(C4_ID, C4_PINS, "J1", "Plug A", 25.4, 50.8, rot=180, value_off=(0, 0), ref_off=(0, 0), hide_value=True, hide_ref=True)
text("J1  Plug A = column side (JST SM 4p female)", (18, 44), 1.27, True)
J2 = place(C4_ID, C4_PINS, "J2", "Pass-through", 25.4, 91.44, rot=180, value_off=(0, 0), ref_off=(0, 0), hide_value=True, hide_ref=True)
text("J2  console pass-through (JST SM 4p male), SNIFF mode only", (18, 84.6), 1.27, True)
for J in (J1, J2):
    stub(J["1"], 10.16, "5V_MACH")
    stub(J["2"], 10.16, "DOUT")
    stub(J["3"], 10.16, "SPEED")
    e = (J["4"][0] + 10.16, J["4"][1]); wire(J["4"], e); gnd(e, "#PWR" + str(len(items)))
text("pin1 green", (J1["1"][0]+30, J1["1"][1]+1), 1.0); text("pin2 red", (J1["2"][0]+30, J1["2"][1]+1), 1.0)
text("pin3 yellow/black", (J1["3"][0]+30, J1["3"][1]+1), 1.0); text("pin4 black/yellow", (J1["4"][0]+30, J1["4"][1]+1), 1.0)

# ---- D1: 5V_MACH -> ESP 5V ----
D1 = place(D_ID, D_PINS, "D1", "1N5819", 81.28, 45.72, value_off=(-4, 4), ref_off=(-2, -4))
# D_Schottky: pin 1 = K (cathode), pin 2 = A (anode); anode at +x
stub(D1["2"], 7.62, "5V_MACH")           # anode <- machine 5V
stub(D1["1"], -7.62, "ESP_5V", just="right")  # cathode -> ESP32 5V
text("D1: machine 5 V -> ESP32 5V/VIN (~4.7 V). USB may stay connected during sniffing.", (66, 40), 1.0)

# ---- dividers: top R from signal, bottom R to GND, tap to ESP32 ----
def divider(xc, ytop, ref_top, val_top, ref_bot, val_bot, net_in, net_out, note):
    Rt = place(R_ID, R_PINS, ref_top, val_top, xc, ytop, value_off=(2.0, 1.0), ref_off=(2.0, -1.5))
    Rb = place(R_ID, R_PINS, ref_bot, val_bot, xc, ytop + 10.16, value_off=(2.0, 1.0), ref_off=(2.0, -1.5))
    # R pins: "1" at (0, 3.81) top, "2" at (0, -3.81) bottom in lib -> schematic top = y-3.81
    top = Rt["1"]; mid_t = Rt["2"]; mid_b = Rb["1"]; bot = Rb["2"]
    stub(top, 0, net_in); wire(top, (top[0], top[1]-2.54)); label(net_in, (top[0], top[1]-2.54), rot=90, just="left")
    tap = ((mid_t[0] + mid_b[0]) / 2, (mid_t[1] + mid_b[1]) / 2)
    wire(mid_t, tap); wire(tap, mid_b)
    junction(tap)
    tap_end = (tap[0] + 7.62, tap[1]); wire(tap, tap_end); label(net_out, tap_end)
    wire(bot, (bot[0], bot[1] + 2.54)); gnd((bot[0], bot[1] + 2.54), "#PWR" + str(len(items)))
    text(note, (xc - 6, ytop - 15), 1.0)

divider(81.28, 71.12, "R1", "100k", "R2", "10k", "5V_MACH", "ADC_A", "supply monitor: 5V_MACH / 11 -> GPIO34")
divider(116.84, 71.12, "R3", "10k", "R4", "15k", "DOUT", "CAPTURE", "DOUT 5 V -> 3 V -> GPIO25 (MCPWM capture)")
divider(152.4, 71.12, "R5", "10k", "R6", "15k", "SPEED", "SPEED_IN", "speed pulse 5 V -> 3 V -> GPIO26")

# ---- driver stage: GPIO27 -> R7 1k -> Q1 base; collector -> JP1 -> DOUT; R8 4k7 collector -> 5V_MACH; emitter -> GND ----
Q1 = place(Q_ID, Q_PINS, "Q1", "BC547", 116.84, 132.08, value_off=(4, 1), ref_off=(4, -1.5))
# Q_NPN pins: E (2.54,-5.08), B (-5.08,0), C (2.54,5.08)
B, E, C = Q1["B"], Q1["E"], Q1["C"]
R7 = place(R_ID, R_PINS, "R7", "1k", B[0] - 10.16, B[1], rot=90, value_off=(-2, 3.5), ref_off=(-2, -2.5))
# rot 90: pin1 at (x+3.81, y)?? computed by place(); connect whichever end is nearer
r7a, r7b = R7["1"], R7["2"]
near, far = (r7a, r7b) if abs(r7a[0] - B[0]) < abs(r7b[0] - B[0]) else (r7b, r7a)
wire(near, B)
stub(far, -7.62, "PWM_OUT", just="right")
R8 = place(R_ID, R_PINS, "R8", "4k7", C[0], C[1] - 10.16, value_off=(2.0, 1.0), ref_off=(2.0, -1.5))
wire(R8["2"], C)
wire(R8["1"], (R8["1"][0], R8["1"][1] - 2.54)); label("5V_MACH", (R8["1"][0], R8["1"][1] - 2.54), rot=90)
# jumper from collector node to DOUT
junction(C)
JP = place(JP_ID, JP_PINS, "JP1", "DRIVE enable", C[0] + 15.24, C[1], value_off=(-6, 4.5), ref_off=(-3, -3))
jl, jr = (JP["1"], JP["2"]) if JP["1"][0] < JP["2"][0] else (JP["2"], JP["1"])
wire(C, jl)
stub(jr, 7.62, "DOUT")
wire(E, (E[0], E[1] + 2.54)); gnd((E[0], E[1] + 2.54), "#PWR" + str(len(items)))
text("Driver (DRIVE mode only): GPIO27 PWM is inverted by Q1; firmware uses 'pwm inv on'.", (140, 145), 1.0)
text("If the brake board accepts 3.3 V logic (session 4), Q1/R7/R8 may be replaced by a 100R series link; keep JP1.", (140, 148), 1.0)
text("BC547 TO-92, flat side facing you: C B E", (140, 151), 1.0)

# ---- ESP32 DevKit on the right ----
ESP = place(ESP_ID, ESP_PINS, "U1", "ESP32 DevKit (classic)", 226.06, 76.2, value_off=(-7, 16), ref_off=(-7, -16))
m = {"5V": "ESP_5V", "GND": "GND", "34": "ADC_A", "26": "SPEED_IN", "25": "CAPTURE", "27": "PWM_OUT", "16": "UART_RX", "2": "LED"}
for num, net in m.items():
    if net == "GND":
        e = (ESP[num][0] - 10.16, ESP[num][1]); wire(ESP[num], e); gnd(e, "#PWR" + str(len(items)))
    else:
        stub(ESP[num], -10.16, net, just="right")
text("GPIO16 (UART2 RX) only if DOUT turns out to be serial: connect to CAPTURE node.", (190, 100), 1.0)
text("GPIO2: on-board LED, heartbeat. USB: serial console 115200, flashing.", (190, 103), 1.0)
text("Common ground: machine GND (plug A pin 3 or 4) = ESP32 GND = divider returns = Q1 emitter.", (190, 106), 1.0)

# ---- power flags (tell ERC where power comes from) ----
text("Power flags (ERC bookkeeping only)", (40, 120), 1.0)
def flag(at, ref):
    px, py = FLG_PINS["1"]
    place(FLG_ID, FLG_PINS, ref, "PWR_FLAG", at[0] - px, at[1] + py, value_off=(0, -5), ref_off=(0, 0), hide_value=True, hide_ref=True)
f1 = (45.72, 124.46); wire(f1, (f1[0], f1[1] + 2.54)); label("5V_MACH", (f1[0], f1[1] + 2.54), rot=270); flag(f1, "#FLG1")
f2 = (55.88, 124.46); wire(f2, (f2[0], f2[1] + 2.54)); gnd((f2[0], f2[1] + 2.54), "#PWR0"); flag(f2, "#FLG2")
f3 = (66.04, 124.46); wire(f3, (f3[0], f3[1] + 2.54)); label("ESP_5V", (f3[0], f3[1] + 2.54), rot=270); flag(f3, "#FLG3")

# ---------- assemble ----------
out = f'''(kicad_sch (version 20250114) (generator "gen_schematic.py") (generator_version "9.0")
  (uuid "{ROOT}")
  (paper "A4" portrait no)
  (title_block (title "Crosstrainer ESP32 adapter board") (date "2026-10-26") (rev "0.1") (company "crosstrainer project")
    (comment 1 "Power X6 / Royalbeach 33821 console link") (comment 2 "yellow/black assignment: verify in session 3"))
  (lib_symbols
{chr(10).join(lib_symbols.values())}
  )
{chr(10).join(items)}
  (sheet_instances (path "/" (page "1")))
)
'''
# paper A4 landscape: KiCad writes (paper "A4") for landscape by default; portrait flag omitted
out = out.replace('(paper "A4" portrait no)', '(paper "A4")')
open(os.path.join(os.path.dirname(__file__) or ".", "adapter.kicad_sch"), "w").write(out)
print("wrote adapter.kicad_sch with", len(items), "items")
