# 06 Photo guide for the next session

Goal: find out what the console is connected to, pin by pin. Nothing gets cut or desoldered.

## Where the cables are (plain words)

The **console** is the display unit with the buttons on top of the handlebar column (the vertical
tube in front of you while training). The manual calls it "Computer (1)".

- **Cable 89 ("Computerkabel, oben")** is the cable that comes out of the **bottom of the console**.
  It was attached to the console at the factory. At its end is a plug. When the machine was
  assembled, this plug was pushed onto the mating plug that sticks out of the **top of the column
  tube** (manual page 9, picture 3). The cable then runs down **inside** the column tube.
- **Cable 90 ("Computerkabel, unten")** comes up from the main frame (the big grey base with the
  flywheel). It was plugged into the lower end of cable 89 when the column was mounted on the base
  (manual page 8, pictures 3 and 4). That joint sits behind the plastic sleeve (105) at the foot of
  the column.
- Cable 90 continues down inside the base to the **brake control board (91)**, which is hidden
  under the big plastic side covers next to the flywheel.
- So: console → (plug A, top of column) → cable 89 → (plug B, foot of column) → cable 90 → brake board.
  We want to attach the ESP32 at **plug A**. Plug B and the brake board are "nice to know".
- **Settled 2026-10-26:** at the top of the column there are exactly three plugs: two 2-pin "PULS"
  (hand pulse, ignored) and one 4-pin "SENSOR". The 4-pin SENSOR plug **is plug A**, the console link.
  Everything below is about that one plug.

## Before you start
1. Pull the wall adapter out of the mains socket.
2. Remove the three screws (6) on the console neck (manual page 9, picture 2) and lift the console
   off the column. The cable(s) will follow; pull gently until the plug(s) appear.
3. Do not pull on wires, only on plug bodies. Latching plugs (like the "PULS" ones) have a small
   tab to press.

## Photos, in order of importance
Take every photo in good light, close enough that the pins are countable, and in focus.
Two photos per plug: face-on (pins visible) and from the side (wire colours visible).

| # | Photo | Why |
|---|-------|-----|
| 1 | The 4-pin SENSOR plug **unplugged**, both halves face-on so the 4 metal contacts and the latch are visible, plus a side view showing which colour sits in which position. Write it down: "latch side, left to right: red, yellow, green, black" or whatever you see. | Pin order for the adapter harness. |
| 2 | **Console PCB, component side, where the 4 wires (red/yellow/green/black) are soldered or plugged in.** Any printed text next to the pads (VCC, GND, SPD, PWM, TX…) is gold. | Function of each wire without measuring. |
| 3 | **Console PCB, the big ICs** close enough to read part numbers. | Signal levels (5 V or 3.3 V). |
| 4 | Optional: slide the sleeve (105) at the foot of the column up and photograph the **cable 89/90 joint (plug B)**. | Second place to tap in, if plug A is awkward. |
| 5 | Optional, later: remove one big side cover (left 118 or right 64, ten screws each) and photograph the **brake board (91)** with all its connectors and labels, plus the **speed sensor (92)** and its magnet. | Needed only if we end up at the brake-board route or for the watt model. |
| 6 | Optional: the adapter socket (61) at the rear of the base. | Minor. |

## Also useful (no photo, just write it down)
- The exact text on the console keys (the p3 photo is too dark to read the lower row).
- Whether the console shows anything right after plugging the mains adapter in, without pedalling.

## Multimeter procedure (AM33D), can be done right away
Safe as long as the meter is in **V DC** (10 MΩ load, cannot harm either board) and a probe never
bridges two neighbouring contacts. Never use the A (current) or Ω/continuity ranges on a live circuit.
Cleanest: **unplug the console** and measure on the **column-side** plug; the 5 V comes from the base
and is present without the console, so nothing on the console can be damaged. Clip the black lead to
one wire (needle or bent paper clip into the contact), probe one contact at a time with the red lead.
Known from the board labels: green = 5V, red = DOUT; yellow/black = GND and speed in unknown order.

1. Mains adapter in, console unplugged. Meter on **DC V, 20 V range**.
2. Black lead clipped to **yellow**, red lead on **green**. About **+5 V** → yellow is **GND**, black is speed.
   About 0 V or a strange value → move the black lead to the **black** wire and repeat; +5 V → black is GND.
   Write down the exact supply voltage.
3. Black lead on GND, red lead on the remaining (speed) wire. Turn the pedals slowly by hand: the reading
   should jump between ~0 V and ~5 V once per revolution (or sit at one level and blip). Note which.
4. Black lead on GND, red lead on **red (DOUT)** with the console unplugged: this shows the idle level the
   brake board sees without a console (pull-up/pull-down on the board).
5. Optional, console plugged in again (back-probe at the wire entry): red lead on DOUT, step the console
   through levels 1 → 8 → 16 and pedal. A DC reading that changes with the level is the PWM average.
6. Mains out, console unplugged: meter on **Ω**, speed wire to GND on the column side while turning the
   pedals. A reed switch shows ∞ most of the time and ~0 Ω briefly once per revolution.

Result table goes into `03-hardware-reference.md` section 5.
