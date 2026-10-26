# 05 Open questions

## Answered 2026-10-26 (session 01)
| Question | Answer |
|---|---|
| Original console works? | **Yes, works fine.** Phase 1 observes the real signals. |
| Tools | **AstroAI AM33D** multimeter (AC/DC V, DC A, Ω, diode, continuity; **no frequency/duty mode**, the "square wave" item is an output) + **classic ESP32 DevKit**. The ESP32 is the waveform/pulse/serial capture tool. |
| Swappable | **Plug swap**: console or ESP32 plugged into the 4-pin SENSOR plug, never both. |
| Power | **Level + computed watts**: ESP32 sets level 1–16, estimates watts from level and cadence (calibrate with the manual's test points). |
| Software stack | **ESP-IDF**. |
| Documentation language | **English**. |
| Separate console manual | **Not available.** Key functions must be read off the console. |
| ESP32 attach point | **Console plug (cable 89)**, adapter harness, console re-pluggable. |
| Smartphone protocol | **Bluetooth LE FTMS** (Fitness Machine Service, Cross Trainer profile). |

## Still open for the owner
1. (answered, see above) Does the original console still work? (p3 shows it off.) Is the motivation "console dead" or
   "want app control"? If it is dead, Phase 1 cannot observe the original signals and we go the
   board-91 route.
2. (answered) Classic ESP32, AM33D multimeter without Hz mode.
3. (answered) Console plug.
4. (answered) BLE FTMS.
5. (answered) ESP-IDF.
6. (answered: no console manual) Photos: see `06-photo-guide.md`.
7. (answered) English.

## New, from the PCB photos (owner can answer by looking at the board)
8. (answered 2026-10-26) There are **no further labels** at the 4-pin "CONNECTOR"; only 5V and DOUT.
   The "20R 1/4W" above the header is the value of R9. Which label sits at which wire colour is still
   open; the two unnamed pins need tracing or measuring (GND check: continuity to the ground pour).
9. (answered) MCU = **Holtek HT46R24-DP28**. The 8-pin DIP near SW12 is unreadable ("KD363b?"); not needed.

**Photo material is complete.** What remains (ground pin, speed pin, DOUT waveform, 5 V current budget)
can only come from measurement at the machine (session 3/4 in `04-plan.md`).

## Technical unknowns (to be measured, see Phase 1)
- Pin count and pinout of cable 89/90.
- Console supply: AC or DC, voltage, current draw.
- Brake command signal type and level↔signal mapping.
- Any feedback line from the brake board (coil current).
- Speed sensor type and pulses per revolution; which wheel carries the magnet.
