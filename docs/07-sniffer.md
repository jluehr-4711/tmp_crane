# 07 Sniffer firmware (session 2 deliverable)

Replaces the oscilloscope we do not have. Runs on the classic ESP32 DevKit, built with ESP-IDF v5.5,
source in `firmware/sniffer/`. Once per second it prints one line with everything it sees on its
probe pins, and a serial console lets you change settings or start the PWM replay output.

## Pin map
| ESP32 pin | Role | Connect to | Protection |
|-----------|------|-----------|------------|
| GPIO34 | ADC probe A | unknown voltage line, e.g. the "5V" wire (green) | 100 kΩ series + 10 kΩ to GND (÷11) |
| GPIO35 | ADC probe B | second line | same divider |
| GPIO32 | ADC probe C | third line | same divider |
| GPIO33 | ADC probe D | fourth line | same divider |
| GPIO25 | DOUT capture (PWM/logic timing) | DOUT wire (red) | 10 kΩ series + 15 kΩ to GND (5 V → 3 V) |
| GPIO26 | speed pulse input | speed wire (yellow or black, after identification) | 10 kΩ series + 15 kΩ to GND; internal pull-up switchable |
| GPIO16 | UART RX sniff (only if DOUT is serial) | DOUT wire | 10 kΩ / 15 kΩ |
| GPIO27 | PWM output (replay test, session 6) | brake board DOUT input | direct (3.3 V logic) or via transistor if 5 V needed |
| GPIO2 | heartbeat LED | on-board | – |
| GND | ground | machine GND (one of yellow/black) | always connect first |

Rules: **the ESP32 is not 5 V tolerant.** Every machine line goes through a divider until its voltage is
known. GND of the ESP32 and GND of the machine must be joined. Power the ESP32 from USB during sniffing.

The ÷11 divider reads a 5 V line as 0.45 V at the pin, which the 12-bit ADC still resolves well, and keeps a
35 V line at 3.2 V. The 10k/15k divider keeps 5 V logic at 3 V for the digital inputs. If the "5V" wire
is confirmed as 5 V, the ADC divider can be changed to 10k/15k (ratio 1.667) with the `div 1.667` command.

## One adapter board for sniffing *and* the final device
The same ESP32 DevKit and the same pin plan serve both roles; only a jumper changes. Build it on a
small perfboard that sits next to the DevKit:

```
column plug (4-pin JST SM female) ──┬── console pass-through (4-pin JST SM male)   [console plugged in only while sniffing]
   green  5V  ──┬── Schottky (e.g. 1N5819) ──► ESP32 "5V"/VIN pin
                └── 100k ─┬─► GPIO34 (ADC A, supply monitor)          10k to GND
   yellow/black GND ───── ESP32 GND  (which one is GND: measured in session 3)
   speed ──── 10k ─┬─► GPIO26 (speed input, internal pull-up on)      15k to GND
   red    DOUT ─── 10k ─┬─► GPIO25 (capture; listens to the console or to our own output)   15k to GND
          DOUT ◄── [JUMPER J1] ◄── collector of NPN (BC547/2N3904), 4.7k pull-up from collector to 5V,
                                   base ◄── 1k ◄── GPIO27 (PWM out; inverted in software)
```
- **Sniff mode:** J1 open, console plugged into the pass-through, ESP32 on USB or machine 5 V. The ESP32 only
  listens (GPIO25/26/34).
- **Drive mode (final):** console unplugged, J1 closed, ESP32 powered from the machine 5 V. GPIO27 drives
  DOUT through the transistor; GPIO25 still captures what is on the line, giving a built-in self-check.
- Never close J1 with the console attached: two drivers on one line.
- The NPN stage inverts: 100 % duty at GPIO27 = DOUT low. The firmware's `pwm` command gets an `inv`
  option for this; the final firmware does the inversion internally.
- If session 4 shows the brake board is happy with 3.3 V logic, the transistor stage can be replaced by a
  direct 100 Ω series link; keep the jumper either way.
- 5 V budget: measure the current the ESP32 draws (≈ 100–150 mA with BLE) against what the 5 V line can
  supply (session 4, with a 1 Ω shunt or the AM33D in mA mode in series on the green wire).

## Probe harness (what to build or order)
Concrete shop list with article numbers: `09-shopping-list.md`.
- 2 pairs 4-pin **JST SM 2.5 mm** connector pigtails (male + female). One pair makes the **Y-probe lead**:
  female ↔ male pass-through for the console, plus a 4-wire tap to a breadboard. The second pair is for the
  later ESP32 adapter lead.
- Resistors: 4× 100 kΩ, 8× 10 kΩ, 4× 15 kΩ, 1× 4.7 kΩ, 1× 1 kΩ (1/4 W, any tolerance).
- 1× NPN transistor BC547 or 2N3904, 1× Schottky diode 1N5819, 1× 2-pin header + jumper.
- Small perfboard, breadboard for the first tests, Dupont wires, a USB cable for the ESP32.
- Optional but recommended: a cheap 8-channel USB logic analyzer (Saleae-clone, ~10 €) as a cross-check.

## Report line
```
ADC A=5.02V B=0.00V C=0.01V D=3.29V (pin mV min..max A 455..459) | DOUT 15625.0 Hz duty 37.50% per 64.0..64.0 us hi 24.0..24.0 us (31250 edges) | SPD total 12 +1 last 843 ms mean 843 ms lvl 1
```
- `ADC` values are already multiplied by the divider ratio (input voltage). `min..max` on the pin shows ripple.
- `DOUT` gives frequency, duty and the min/max of period and high time. A clean PWM shows constant
  period and a high time that changes with the resistance level. `static HIGH/LOW` means no edges.
- `SPD` counts falling edges on the speed input, with the interval between pulses.
- `UART@baud` appears when the sniff is on and lists received bytes in hex.

## Console commands (115200 baud, type `help`)
| Command | Effect |
|---------|--------|
| `report on\|off\|<ms>` | periodic report on/off or interval |
| `div [ratio]` | ADC divider ratio (default 11) |
| `pullup on\|off` | internal pull-up on the speed input (for a reed switch to GND) |
| `uart <baud>\|off` | serial sniff on GPIO16, try 9600 / 19200 / 38400 / 57600 / 115200 |
| `pwm <freq> <duty%>` / `pwm off` | PWM output on GPIO27 for the replay test |
| `pins` | pin map |

## Session 4 procedure with the sniffer
1. Y-probe lead between console and column, console in control, machine powered.
2. ESP32 GND to machine GND. ADC A → "5V" wire via ÷11, GPIO25 → DOUT via 10k/15k, GPIO26 → speed via 10k/15k.
3. `idf.py monitor`, read the report: supply voltage, DOUT static or PWM, speed interval while pedalling.
4. Step the console through levels 1…16; write down DOUT frequency and duty for every level
   (table in `03-hardware-reference.md`). Pedal at a steady cadence if the console only applies the
   level while moving.
5. Pedal at a known cadence and count: pulses per crank revolution.
6. If DOUT shows no clean PWM: `uart 9600` and so on, watch for bytes that change with the level.
