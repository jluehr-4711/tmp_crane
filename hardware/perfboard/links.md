# Bottom-side links (bare wire / solder bridges)

| from | to | net |
|---|---|---|
| (2,2) | (2,18) | 5V_MACH |
| (3,4) | (3,22) | DOUT |
| (4,5) | (4,20) | SPEED |
| (5,6) | (5,14) | GND |
| (2,2) | (7,2) | 5V_MACH |
| (7,2) | (7,3) | 5V_MACH |
| (7,2) | (9,2) | 5V_MACH |
| (14,2) | (17,2) | ESP_5V |
| (17,2) | (17,3) | ESP_5V |
| (3,4) | (10,4) | DOUT |
| (4,5) | (13,5) | SPEED |
| (7,7) | (17,7) | ADC_A |
| (10,8) | (17,8) | CAPTURE |
| (13,9) | (17,9) | SPEED_IN |
| (5,14) | (17,14) | GND |
| (7,11) | (7,14) | GND |
| (10,12) | (10,14) | GND |
| (13,13) | (13,14) | GND |
| (17,10) | (17,14) | GND |
| (9,17) | (9,14) | GND |
| (6,16) | (7,16) | Q_C |
| (7,16) | (7,17) | Q_C |
| (7,17) | (7,20) | Q_C |
| (3,21) | (7,21) | DOUT |
| (8,17) | (8,19) | Q_B |

# Top-side insulated jumpers

| from | to | net |
|---|---|---|
| (17,6) | (12,19) | PWM_OUT |

# Component holes

| ref | value | holes |
|---|---|---|
| H1 | 1x8 pin header, Dupont to ESP32 | (17,3) 1 5V, (17,4) 2 G16, (17,5) 3 G2, (17,6) 4 G27, (17,7) 5 G34, (17,8) 6 G25, (17,9) 7 G26, (17,10) 8 GND |
| D1 | 1N5819 (band = cathode, right) | (9,2) A, (14,2) K |
| R1 | 100k | (7,3) 1, (7,7) 2 |
| R2 | 10k | (7,7) 1, (7,11) 2 |
| R3 | 10k | (10,4) 1, (10,8) 2 |
| R4 | 15k | (10,8) 1, (10,12) 2 |
| R5 | 10k | (13,5) 1, (13,9) 2 |
| R6 | 15k | (13,9) 1, (13,13) 2 |
| R8 | 4k7 | (2,16) 1, (6,16) 2 |
| Q1 | BC547, flat side towards the bottom edge (pins C B E left->right) | (7,17) C, (8,17) B, (9,17) E |
| R7 | 1k | (8,19) 1, (12,19) 2 |
| JP1 | 2-pin header + jumper cap (DRIVE enable) | (7,20) 1, (7,21) 2 |
| J1 | plug A pigtail (JST SM 4p female) | (2,17) green 5V, (3,21) red DOUT, (4,19) yellow, (5,13) black |
| J2 | console pass-through pigtail (JST SM 4p male) | (2,18) green, (3,22) red, (4,20) yellow, (5,14) black |
