# 08 Prior art and reusable work

Checked 2026-10-26. Searches for the board marking "TC5228", the MCU "HT46R24" in a fitness context,
"Royalbeach"/"Crane Sports"/"Christopeit" console pinouts and brake boards: **nothing published**. The
console is a white-label Taiwanese/Chinese design (board by "WH_Hsieh"), but no pinout or protocol
description for it is online. The measurement sessions stay necessary.

## Closest project: dbsqp/bluetooth-reebok-57e
https://github.com/dbsqp/bluetooth-reebok-57e (fork of esp32-ftms-server). Reebok 5.7e exercise bike,
ESP32 NodeMCU-32S, Arduino core. Same class of machine electronics as ours:
- **Brake:** electromagnet driven by a **5 V, 1 kHz PWM** from the console MCU, through an optocoupler
  into a power board that rectifies mains for the coil. The ESP32 taps the PWM line (level shift with an
  NPN transistor) and reads the duty cycle. → Our "DOUT" from an HT46R24 is almost certainly the same kind
  of signal; the capture part of our sniffer is designed for exactly this.
- **Cadence:** reed switch on the main board pulling an MCU GPIO to ground; ESP32 reads it through a PNP
  level shifter, edge-triggered with debounce. → Same as our planned speed input with pull-up.
- **Power:** no coil-current feedback; watts are an **empirical quadratic model P = f(duty, cadence)**
  fitted from measurements at several cadences and levels. → Matches our decision "level + computed
  watts"; our calibration points come from the manual's watt-measurement table (50/60/70 rpm).
- **Supply:** ESP32 powered from the console's always-on 5 V header. → Our green "5V" wire.
- **Limits:** that project only *reads* the brake PWM; it does not drive it. Ours must drive it (plug
  swap), which is the one part with no direct template. BLE: it uses CSC/Cycling Power for Apple Watch;
  its FTMS branch is untested.

## Other references
- eborchardt/BluetoothTreadmill: reverse-engineers a serial console↔drive protocol and bridges it to FTMS.
  Template only if DOUT turns out to be serial (unlikely, HT46R24 has no UART).
- ptx2/SmartSpin2k: mature ESP32 FTMS implementation (Arduino), useful as a reference for the FTMS
  control-point handling (target resistance / target power) even though it moves a knob with a stepper.
- avilleret/fdf-ftms-esp32: ESP-IDF based FTMS for a rower; closest to our chosen stack for the BLE part.

## What we reuse
1. The **architecture**: tap/drive PWM for the brake, reed pulses for cadence, 5 V from the machine,
   watts from a fitted model. No need to invent anything here.
2. The **FTMS service layout** (Fitness Machine Feature, Cross Trainer Data, Control Point, Status)
   from the projects above, re-implemented on ESP-IDF's NimBLE.
3. The **measurement method** (duty vs. cadence vs. displayed watts table) for the watt model.

## What stays specific to our machine and must be measured
- Which of yellow/black is GND vs. speed; whether the speed line needs a pull-up and its pulses per revolution.
- DOUT: frequency, duty per level, and whether the brake board expects 5 V or accepts 3.3 V logic.
- Whether the brake board applies the level without pedalling and whether it has a "no console" fail-safe.
- The 5 V line's current budget for the ESP32.
