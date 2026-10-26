# 09 Shopping list (checked 2026-10-26)

Prices are what the shops showed on 2026-10-26, net of shipping; Reichelt article numbers are exact,
Amazon entries are listings found by search (check the price on the page). You already have the
classic ESP32 DevKit, the AM33D multimeter and a USB cable.

## Reichelt (reichelt.de, search for the article number)
| Qty | Article no. | Item | Unit € | Use |
|----:|-------------|------|-------:|-----|
| 2 | `BC 547B` | NPN transistor TO-92 | 0.04 | DOUT driver stage (one spare) |
| 2 | `1N 5819` | Schottky diode 40 V 1 A DO-41 | 0.04 | 5 V feed into the ESP32 |
| 5 | `1/4W 100K` | carbon film resistor 100 kΩ 0.25 W | 0.09 | ADC dividers (top) |
| 10 | `1/4W 10K` | 10 kΩ | 0.10 | dividers (bottom / series) |
| 5 | `1/4W 15K` | 15 kΩ | 0.09 | logic-input dividers |
| 2 | `1/4W 4,7K` | 4.7 kΩ | 0.11 | pull-up at the transistor collector |
| 2 | `1/4W 1,0K` | 1 kΩ | 0.09 | base resistor |
| 1 | `SL 1X36G 2,54` | 36-pin header strip | 0.25 | jumper J1, test points |
| 5 | `JUMPER 2,54 SW` | jumper cap | 0.02 | J1 |
| 2 | `H25PR050` | perfboard 50 × 100 mm, 2.54 mm | 1.11 | the adapter board |
| 1 | `STECKBOARD 1K2V` | breadboard 640 + 200 contacts | 3.35 | first tests, the DevKit plugs in |
| 1 | `STECKBOARD DBS` | 140-piece wire-bridge set | 4.12 | breadboard wiring |

Subtotal ≈ 13 €, plus shipping (≈ 6 €). Alternative to the single resistors: `K/RES-E12`,
610-piece E12 assortment, 7.27 €, if you want a stock for later.
Reichelt has **no** JST SM connectors (its "JST SM02B" hit is a different 3.5 mm series) and no cheap
logic analyzer (only a 108 € USB scope), so those come from Amazon.

## Amazon.de
| Qty | Item | Listing | Price |
|----:|------|---------|-------|
| 1 set | **JST SM 4-pin male + female pigtail pairs, 2.5 mm pitch, 22 AWG, ~15 cm** (sets of 10–15 pairs; we need 2 pairs, the rest are spares/for a second lead) | search "JST SM 4 Pin Stecker Buchse Kabel"; e.g. "Lyeteung 15 Paar JST SM 4 Pin Steckverbinder 150 mm 22AWG", or the 2/3/4-pin selectable set https://www.amazon.de/dp/B0GYJWPB7P (choose 4p) | ≈ 7–10 € |
| 1 | **USB logic analyzer 8 ch 24 MHz** (fx2lafw / Saleae-clone, works with PulseView) | https://www.amazon.de/dp/B08MXZYMJ5 | 13.35 € |
| 1 | Dupont jumper wire set, 120 pcs, 20 cm, M-M / M-F / F-F | search "Dupont Kabel 120 Stück 20cm"; any 4+ star set | ≈ 6–8 € |

Alternative for the analyzer: AZ-Delivery "Logic Analyzer 8 CH 24 MHz", 13.99 €, same hardware.

## Conrad (conrad.de) – only useful locally if you are near Wernberg-Köblitz (DE) or Linz (AT)
Conrad closed its other retail stores (2022/23); everything else is online with parcel delivery.
Found by search on 2026-10-26; Conrad's site blocks automated access, so prices and in-store stock
could not be checked. Order numbers are from the product URLs.
| Qty | Order no. | Item |
|----:|-----------|------|
| 2 | 1581828 | TRU Components TC-BC547B, NPN TO-92 |
| 2 | 155460 | STMicroelectronics 1N5819, Schottky 40 V 1 A, DO-41 |
| 1 | 84518 | Whadda/Velleman K/RES-E12, 610-piece carbon-film 1/4 W assortment (covers all five values) |
| 1 | 2574925 | Velleman breadboard, 400 contacts |
| 1 | 2899209 | TRU Components wire-bridge set, 350 pieces |
| – | – | pin header 2.54 mm and jumper caps: search "Stiftleiste 2,54 36-polig" / "Kurzschlussbrücke 2,54" |
| – | – | perfboard: search "Lochrasterplatine Hartpapier 100 x 50" |
Not at Conrad: JST SM connectors (only PH/XH/ZH series) and the cheap 24 MHz logic analyzer.

## Local shops in general
Resistors, BC547, 1N5819, pin headers, perfboard and a breadboard are stock items in any electronics
shop (Pollin in Pförring, Segor in Berlin, Bürklin in Munich, Reichelt in Sande, Conrad Wernberg/Linz).
The JST SM pigtails and the logic analyzer are practically online-only.

## Caveats
- **Connector family:** the machine's plug looks like JST SM (2.5 mm, wire-to-wire, latch) in photo p2,
  but that is a visual guess **[assumption]**. The set is cheap; if it does not mate in session 3, we
  measure the pitch and housing with a caliper and reorder (SM is the common choice on fitness consoles).
  Listings that say "2.54 mm" for SM are usually the same part.
- Resistor values are not critical; 5 % carbon film is fine. Any NPN small-signal transistor (BC547/548,
  2N3904) and any 1 A Schottky work.

Total ≈ 45 € with shipping, ≈ 30 € without the logic analyzer.
