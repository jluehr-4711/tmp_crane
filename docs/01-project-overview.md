# 01 Project overview

## Goal
Use an ESP32 to control the fitness trainer: set the pedal resistance (brake) and read speed /
power, exposed to a smartphone client. The user interface itself is out of scope.

## Deliverables (from CLAUDE.md)
1. Wiring instructions (how to connect the ESP32 to the machine)
2. ESP32 software

Order: **wiring first, then software.**

## Rules (from CLAUDE.md, with interpretation)
| Rule | Interpretation for this project |
|------|-------------------------------|
| Replacement must be swappable; old control unit stays operational | Plug swap (owner's choice): either the console or the ESP32 is plugged into the 4-pin SENSOR plug at the top of the column. No cut wires, no modified original boards. |
| Pulse not needed; resistance and power must be pickable | Hand-pulse sensors are ignored. Must have: set brake level (16 steps like the original), read cadence/speed, compute watts from level and cadence (owner's choice, no closed-loop watt control). |
| UI out of scope, assume smartphone client | ESP32 exposes Bluetooth LE FTMS (owner's choice). Firmware in ESP-IDF. |
| Document every session | `docs/sessions/`, see README conventions. |
| Plan-based | `04-plan.md` holds the big picture; each session states which plan step it serves. |
| Use the ESP32 for debugging/measuring | Where a scope is not available, the ESP32 ADC/logic inputs (with proper dividers) log the signals. |
| Hobby project, working result matters | Prefer simple, robust solutions over elegant ones. |

## Big picture
```
 230 V~ ──► AC-AC adapter (104)  26 V~ / 2.5 A
                 │
                 ▼ socket (61) at rear of frame
        ┌──────────────────────────────┐
        │ Brake control board (91)      │◄── speed sensor (92), near flywheel
        │ in the main frame (25)        │──► eddy-current brake coil (part of 60)
        └──────────────┬───────────────┘
                       │ lower computer cable (90)
                       ╪ plug pair inside the column (10)
                       │ upper computer cable (89), "Klinkenstecker" at the console
        ┌──────────────▼───────────────┐
        │ Console (1) "Easy Control"    │◄── hand-pulse sensors (93/94/95), 2x "PULS" plugs
        └──────────────────────────────┘
```
The ESP32 replaces the console at the cable-89 interface **[assumption, to be verified]**. Everything
below that interface (power, brake driver, speed sensor) stays original.

## Machine facts (short)
- Crane Sports "Power X6 Crosstrainer-Ergometer", Royalbeach, Art.-Nr. 33821, console label RB-33821-06605-B.
- Electromagnetic eddy-current brake ("Wirbelstrombremse, Feldspulenprinzip"), up to 400 W, 16 resistance steps, speed-independent watt program.
- Supply: AC-AC wall adapter, 26 V~ 2.5 A.
- Full details in `03-hardware-reference.md`.
