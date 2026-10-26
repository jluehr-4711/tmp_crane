# 03 Hardware reference

Facts from the manual and photos. Items marked **[assumption]** are not yet verified by measurement.

## 1. Identification
| Item | Value |
|------|-------|
| Name | Power X6 Crosstrainer-Ergometer (Crane Sports branding, Aldi Süd, autumn 2006) |
| Manufacturer / service | Royalbeach, Watzmannstraße 1, D-83417 Kirchanschöring; RC Sportgeräte Service |
| Article number | 33821 (console label RB-33821-06605-B) |
| Standard | DIN EN 957-1/9 class HA, 150 kg, CE (EMC 89/336/EWG, EN 55081-1) |
| Weight / flywheel | ca. 59 kg / ca. 8 kg flywheel, V-belt drive (belt 1168.J6, pulley Ø280) |

## 2. Electrical system (overview)
| Part no. | Name in manual | Role |
|---|---|---|
| 104 | Adapter | AC-AC wall adapter, Yunyong AYY66-2602500: 230 V~ in, **26 V~ / 2.5 A out** (~65 VA). Cable is not user-replaceable. |
| 61 | Anschlußbuchse und Kabel für Adapter | DC-style barrel socket at the rear of the frame + lead to the brake board. (26 V AC on a barrel plug, so there is **no polarity**; rectification is inside the machine.) |
| 91 | Steuerplatine für Wirbelstrombremse | Brake control board, mounted inside the main frame (25) near the flywheel (exploded view shows it beside part 82/90). Receives 26 V~, drives the brake coil, **[assumption]** also rectifies/regulates the console supply and passes the speed-sensor signal upward. |
| 60 | Schwingscheiben-Set mit Bremssystem | Flywheel assembly incl. eddy-current brake ("Wirbelstrombremse, Feldspulenprinzip"): a field coil on a yoke, flywheel rim acts as the conductor. Max 400 W, 16 steps. |
| 92 | Sensor mit Kabeln (700 mm) | Speed/cadence sensor at the flywheel, with 700 mm cable. **[assumption]** reed switch or Hall sensor plus magnet (54 "Magnet mit Fixierung"). Gives 1 pulse per flywheel revolution (or per crank revolution if the magnet sits on the belt wheel), to be measured. |
| 54 | Magnet mit Fixierung | Magnet for the speed sensor. |
| 90 | Computerkabel, unten | Lower computer cable: from brake board (91) up through the main frame to the column joint. |
| 89 | Computerkabel, oben | Upper computer cable: from the column joint up to the console; manual calls the console-end plug "Klinkenstecker" (jack plug). |
| 1 | Computer | Console "Easy Control", blue backlit LCD, German text, keys as on photo p3. |
| 93, 94, 95 | Handpulskabel / Handpulssensoren | Hand-pulse contacts in the swing arms (2x) + column cable; 2-pin "PULS" plugs. **Not needed** for this project. |
| 67 | Computerhals | Console neck / plastic mount on the column. |

Manual quote (p.9): *"Die Computerkabel (89+90) dienen der Steuerung des Widerstandes und der
Übermittlung von Funktionswerten, wie z. B. Geschwindigkeit oder Trittfrequenz, an den Computer."*
So the console cable carries: **brake control (down), speed/cadence (up), and console power**.

## 3. Behaviour of the original system (from the manual)
- Console turns on with mains; no battery. "Computer stoppt automatisch, wenn die Pedale nicht bewegt werden" (auto standby when no pedal movement).
- Resistance adjustable in 16 steps via keys, displayed in **watts**; the watt program is cadence-independent (the console regulates the coil current against measured cadence to hold a watt target).
- Watt-measurement test points (p.17): 50 rpm → 50 W, 100 W; 60 rpm → 150, 200, 250 W; 70 rpm → 300, 350, 400 W. Useful later for calibrating our own level→watt table.
- Static discharge can crash the console; fix is power-cycle (1 min off). Suggests the console MCU has no watchdog; irrelevant for us but shows the logic lives in the console.
- Troubleshooting: "Tretwiderstand nicht regelbar → keine Kabelverbindung" confirms the brake level is commanded over cable 89/90.

## 4. Console internals (photos IMG_0619 / IMG_0621 / IMG_0629 / IMG_0630)
- Connectors on the main PCB: JK2 "HR" (3-pin, pulse daughterboard), JK4 and JK5 "Backlight" (3-pin each,
  LCD backlight), "CONNECTOR" (4-pin, the tube cable = console link), JK7 (~8-pin ribbon to the LCD board).
- Power parts: U2 HT7133 (3.3 V, 30 mA LDO) + C4, U7 HT7033 (3.3 V detector/reset). The MCU is a **Holtek HT46R24-DP28**
  (owner read the marking; DP28 = 28-pin DIP): 8-bit "A/D type" MCU, 28-pin SKDIP, 8-channel 10-bit ADC, **hardware PWM outputs
  (8-bit, shared with I/O pins)**, two 16-bit timer/event counters, one external interrupt pin, I²C slave only,
  **no UART**, 2.2–5.5 V at 4 MHz. The 8-pin DIP near SW12 is nearly unreadable (owner: "KD363b?"), function unknown, not on the console link path.
- What the HT46R24 implies for the console link **[assumption until measured]**:
  - "DOUT" is most likely one of the MCU's **hardware PWM outputs**, so the brake command is a PWM duty
    cycle, 8-bit resolution, frequency f_SYS/64 or f_SYS/128 (Holtek 6+2 / 7+1 modes) → tens of kHz with a
    4–8 MHz crystal. A bit-banged serial protocol is possible but unlikely on a part without UART.
  - The speed pulse goes into the external-interrupt pin or a timer/event-counter input.
  - The 20 Ω R9 next to the header is probably in series with DOUT or the speed line as protection.
  - The ADC may read a coil-current or supply feedback line, but with only 4 wires (5V, GND, DOUT, speed)
    there is no room for one; the watt program then runs open-loop from a level table.
- Q2/Q3 C945 NPN transistors near JK2/HR; R8/R9 20 Ω 1/4 W (one next to the buzzer, one next to "CONNECTOR",
  probably series protection on a connector line **[assumption]**); D1–D7 1N4148 key-matrix diodes; 15 keys.
- Main PCB: single-sided-looking FR4 with large ground pours, marked **TC5228 / 6706 / 3BC0U019G21200 By:WH_Hsieh**. Date code 6706 ≈ 2006 **[assumption]**. The OEM board maker is unknown; "TC5228" is the board, not an IC.
- Daughterboard "0526": hand-pulse amplifier **[assumption]**, 3-wire link (red = VCC, black = GND, yellow = signal **[assumption]**).
- Connectors at the top of the column (confirmed by owner, 2026-10-26): exactly three plugs.
  - 2x 2-pin **"PULS"** (JST SM style, latching) = hand-pulse lines, ignored.
  - 1x 4-pin **"SENSOR"** (JST SM style, latching, 2.5 mm pitch **[assumption]**) = the console link,
    i.e. the upper end of cable 89/90. Wire colours seen in photo p2: **red, yellow, green, black/brown** (to confirm).
  - The manual's word "Klinkenstecker" is loose; there is no jack plug.
- Console end (photos IMG_0629/0630): the cable lands on a 4-pin header labelled **"CONNECTOR"** on the
  main PCB, with silkscreen **"5V"** and **"DOUT"** beside it. The other two pins carry **no label** (owner checked);
  "20R 1/4W" above the header is resistor R9's value. Wire order at the header: green, yellow, red, black.
- Pin assignment from the silkscreen (owner, 2026-10-26): the two labelled pins are at the two ends of the
  header. **green = 5V**, **red = DOUT**. The two middle pins, **yellow and black**, are unlabelled and must be
  **GND and the speed pulse** in some order **[assumption]**. Note: wire colours do *not* follow the usual
  red-plus / black-minus convention here, so never wire anything by colour alone.
- Direction **[assumption]**: 5 V is supplied *from the brake board to the console*; DOUT is the command
  *out of the console* to the brake board (brake level, PWM from the HT46R24); the speed pulse comes *in*.
- Consequence if confirmed: the brake board already provides a regulated 5 V rail. The ESP32 DevKit can
  be fed from it (check current budget: ESP32 with BLE draws 80–150 mA, peaks higher), and the console
  logic is 5 V or 3.3 V (U2 HT7133 is a 3.3 V LDO), so signal levels are ESP32-friendly after at most a
  divider on the speed line.

## 5. What the ESP32 must interface with (target)
| Signal | Direction | Status |
|---|---|---|
| Console supply | board 91 → console | Unknown: voltage (DC after rectification? raw 26 V~?), current. **Measure first.** |
| Brake command | console → board 91 | Unknown: PWM? analog 0–5 V? serial? 16 discrete levels? **Measure with original console attached.** |
| Brake feedback | board 91 → console | Possibly a coil-current sense line (watt program needs it) **[assumption]**. |
| Speed pulses | sensor 92 → (board 91) → console | Unknown waveform; likely open-collector / reed to GND, pulled up in console. |
| Hand pulse | sensors → console | Ignored. |

## 6. Available tools
- AstroAI AM33D: AC/DC voltage, DC current, resistance, diode, continuity. No frequency, duty, capacitance or hFE. Its "square wave output" is a test-signal output, not a measurement. Consequence: DC averages and AC levels come from the meter, everything time-based (pulses, PWM, serial) from the classic ESP32 with a voltage divider.
- Classic ESP32 DevKit (3.3 V I/O, ADC 0–3.3 V with poor linearity at the ends, PCNT/RMT peripherals for pulse capture).

## 7. Safety notes for the measurement sessions
- 26 V AC from a class-II adapter is low voltage but the brake coil is inductive: never unplug the coil under current, expect flyback spikes on the board. Measure only at the console cable, not at the coil, unless the board is understood.
- Rectified 26 V~ gives ≈ 35 V DC. **ESP32 inputs are 3.3 V tolerant only**: any probing with the ESP32 needs a divider (≥ 12:1) or a scope first.
- Keep the original console connected during the first measurements so the real signals can be observed.

## 8. Reference images
- `img/console-mainboard-label.png` – PCB markings
- `img/console-pulse-daughterboard.png` – daughterboard
- `img/manual-p08-column-cable.png`, `img/manual-p09-console-mounting.png` – cable 89/90 routing
- `img/manual-p18-exploded-view.png`, `img/manual-p19-parts-list.png`
