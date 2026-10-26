# 04 Plan

Wiring first, then software. Each phase ends with a documented result.

## Phase 0 – Project setup (this session, 2026-10-26)
- [x] Read CLAUDE.md, material, create docs structure.
- [x] Owner answered the key questions (`05-open-questions.md`): console works, multimeter + ESP32 only, attach at console plug, BLE FTMS.
- [x] Owner: classic ESP32, AM33D meter. Column top = 2x PULS + 1x 4-pin SENSOR (the console link).
- [ ] Owner: pin order of the SENSOR plug, PCB photo at the cable entry; multimeter readings per `06-photo-guide.md`.
- [ ] Owner: order the parts in `09-shopping-list.md` (Reichelt + Amazon).
- [x] Session 2: sniffer firmware written and built (`firmware/sniffer/`, `07-sniffer.md`).
- [ ] Bench test of the sniffer (GPIO27 → GPIO25 loop) before session 4.

## Phase 1 – Discover the console interface (measurement, original console attached)
Goal: a verified pinout of the computer cable (89/90) and the signal types on every wire.
1. Photograph: console-side plug of cable 89 (both faces, count pins, note colours), the
   column joint plug 89/90, the brake board (91) with its connectors, the speed sensor (92).
2. With the machine powered and the console attached, measure on the cable-89 plug (back-probe or
   an extension harness): DC and AC voltage of every pin against the most negative pin.
   Identify GND, supply, and the signal pins.
3. Pedal and watch the speed pin: multimeter (Hz mode if present) and the ESP32 pulse counter
   through a divider. Note pulses per revolution.
4. Change the resistance level 1→16 on the console and watch the brake-command pin: multimeter DC
   average first (a PWM shows as a level-dependent average), then the ESP32 as capture device:
   edge timing with a GPIO interrupt / RMT for PWM, ADC sampling for analog, UART sniff at common
   baud rates if it looks like bursts. No scope is available, so a small "sniffer" firmware is the
   first software deliverable (serves Phase 1, see Phase 3 debug mode).
5. Result: table "pin → function → voltage range → waveform" in `03-hardware-reference.md`.

Fallback if the brake command turns out to be an undocumented serial protocol that is hard to
replay: move the interface one level down and let the ESP32 drive the coil through its own MOSFET
stage on the board-91 coil connector. Still swappable if done with a plug adapter, but less elegant.

## Phase 2 – Wiring design and adapter harness
- Choose ESP32 board (recommendation: ESP32-S3 or classic ESP32 DevKit, both have BLE and enough GPIO).
- Power: buck converter from the console supply line (whatever Phase 1 finds) to 5 V/3.3 V.
- Level shifting: dividers for inputs > 3.3 V; transistor or logic-level MOSFET / RC filter + op-amp for the
  brake command if the board expects 5 V logic or an analog level.
- The adapter board from `07-sniffer.md` is the final hardware: pass-through for the console while sniffing, jumper J1 for drive mode (plug swap, never both drivers).
- Deliverable: `docs/wiring.md` with a schematic, BOM and photos.

## Phase 3 – Software (ESP32)
- Framework: **ESP-IDF** (owner's choice).
- Modules: speed/cadence input (pulse counter), brake output (PWM/DAC) with 16 levels, watt model
  (level + cadence → watts, calibrated with the manual's test points; no closed-loop watt control), BLE **FTMS Cross Trainer**
  profile (standard, works with many apps) and optionally a plain WiFi/HTTP or MQTT endpoint.
- Debug/measure mode: the firmware can log raw ADC/pulse data over serial for Phase 1 style measurements.
- Deliverable: `firmware/` + `docs/software.md`.

## Phase 4 – Verification
- Side-by-side: original console level N vs ESP32 level N produce the same pedal feel / watts.
- Swap test: console back in, everything works as before.

## Session plan (agreed 2026-10-26)

| # | Where | Who | Does | Result |
|---|-------|-----|------|--------|
| 2 ✅ | Desk, no machine | Claude (owner orders parts) | ESP-IDF project skeleton + **sniffer firmware**: ADC logger, pulse counter, PWM frequency/duty capture, UART sniff at common baud rates, all printed over USB serial. Probing-harness design (dividers so nothing above 3.3 V reaches the ESP32). Owner orders: 4-pin JST SM 2.5 mm pigtail pairs, resistors (e.g. 100 kΩ / 10 kΩ), breadboard, Dupont wires; optional €10 USB logic analyzer. | Firmware flashed and tested on the bench with a known signal; parts on the way. |
| 3 | At the machine, ~1 h | Owner, Claude guiding | Photos per `06-photo-guide.md`; multimeter identification of GND, supply, speed and brake wires on the 4-pin SENSOR plug; pin order written down. | Pinout table in `03-hardware-reference.md`, assumptions removed. |
| 4 | At the machine, ~1–2 h | Owner + ESP32 | Y-probe lead between console and column (console stays in control, ESP32 only listens through dividers). Record speed pulses while pedalling and the brake command at every level 1–16. | Signal spec: waveform, voltage, frequency/duty or protocol per level. |
| 5 | Desk | Claude | Wiring design: adapter lead with mating connector, supply conversion (buck from the console supply line), level shifting for the brake output, pull-up for the speed input. `docs/wiring.md` with schematic + BOM. Owner builds it. | Wiring instructions = deliverable 1 (draft). |
| 6 | At the machine | Owner + ESP32 | **Plug swap**: ESP32 replaces the console. Test firmware sets levels 1–16 and reads cadence; compare pedal feel with the console at the same levels. Swap the console back, confirm it still works. | Wiring verified; `wiring.md` final. |
| 7 | Desk + machine | Claude, owner tests | Firmware: BLE FTMS Cross Trainer service, level control, cadence/speed, watt model calibrated with the manual's rpm/watt test points. Test with a phone app. | Software = deliverable 2. |
| 8 | Machine | Owner | Acceptance: real training session via phone; swap test again; final docs. | Project done. |

Fallback paths: if session 4 shows a serial protocol that cannot be replayed, session 5 moves the
interface to the brake board (91) and adds a side-cover-off photo session first.
