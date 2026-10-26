Project Goal: Use an ESP32 to control a fitness trainer (Crane Sports Power X6 Crosstrainer-Ergometer, Royalbeach Art.-Nr. 33821).

Result:
1. Instructions, how to wire
2. Software, for the ESP32

First, wiring, then software

Rules:
- Replacement must be swappable: the old control unit (console) must still be operational, by plugging it back into the same connector (plug swap, never both at once).
- Pulse is not needed, but resistance and power should be pickable (resistance as level 1–16, power computed from level and cadence).
- User interface is out of scope, assume a smartphone client (Bluetooth LE FTMS).
- Every session / step / tour requires documentation: document the result.
- Plan-based approach: plan before executing. Have the big picture in mind.
- Use the ESP32 for debugging / measuring when possible / reasonable (no oscilloscope available, only a multimeter).
- Hobby project, but a working result is important.

Decisions (2026-10-26):
- Interface point: the 4-pin "SENSOR"/"CONNECTOR" plug at the top of the handlebar column (console link).
- Hardware: classic ESP32 DevKit. Multimeter: AstroAI AM33D (no frequency mode).
- Firmware: ESP-IDF, in firmware/. Docs language: English.

Documentation:
- Index: docs/README.md. Plan: docs/04-plan.md. Hardware facts: docs/03-hardware-reference.md. Open questions: docs/05-open-questions.md.
- Each session writes docs/sessions/YYYY-MM-DD-session-NN.md and updates the plan checkboxes.
- Mark unverified statements [assumption]; remove the tag only after measurement.
- Original material (photos, manual) lives in material/ and is never modified.
