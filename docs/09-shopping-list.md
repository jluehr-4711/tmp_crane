# 09 Shopping list (checked 2026-10-26)

Prices are what the shops showed on 2026-10-26, net of shipping; Reichelt article numbers are exact,
Amazon entries are listings found by search (check the price on the page). You already have the
classic ESP32 DevKit, the AM33D multimeter and a USB cable.

## Recommended: one order at Amazon.de (everything in one parcel, free shipping above 39 €)
Reichelt and Conrad lack the JST SM connectors and the logic analyzer, so a single order is only
possible at Amazon (or eBay with several sellers, which splits shipping again). Amazon sells the
passives as multipacks; the spares are harmless. Amazon blocks automated price checks, so these are
search terms with typical prices, not verified listings; pick well-rated sellers.
| # | Item | Link | ≈ € |
|---|------|------|----:|
| 1 | JST SM 4-pin male+female pigtail pairs, 2.5 mm, 22 AWG, ~15 cm, 10–15 pairs | product: https://www.amazon.de/dp/B0GYJWPB7P (choose the 4p variant) · search: https://www.amazon.de/s?k=JST+SM+4+Pin+Stecker+Buchse+Kabel+2%2C5mm | 8 |
| 2 | USB logic analyzer 8 ch 24 MHz (PulseView/fx2lafw) | product: https://www.amazon.de/dp/B08MXZYMJ5 (13.35 € on 2026-10-26) | 13 |
| 3 | Resistor assortment 1/4 W, must include 1k, 4.7k, 10k, 15k, 100k | search: https://www.amazon.de/s?k=Widerstand+Sortiment+1%2F4W+Metallschicht+Kit | 10 |
| 4 | BC547 NPN transistor, pack of 50 | search: https://www.amazon.de/s?k=BC547+Transistor+50+St%C3%BCck | 5 |
| 5 | 1N5819 Schottky diode, pack of 20–100 | search: https://www.amazon.de/s?k=1N5819+Schottky+Diode | 5 |
| 6 | Pin header 2.54 mm 40-pin (pack) + jumper caps | search: https://www.amazon.de/s?k=Stiftleiste+2%2C54mm+40+Pin+Jumper+Kappen+Set | 6 |
| 7 | Prototype PCB 5 × 7 cm, set of 10 | search: https://www.amazon.de/s?k=Lochrasterplatine+5x7+cm+10+St%C3%BCck | 6 |
| 8 | Breadboard 830 + 120 Dupont jumper wires (e.g. AZDelivery kit) | search: https://www.amazon.de/s?k=Breadboard+830+Jumper+Wire+Set+120 | 10 |

Only links 1 and 2 are verified product pages; Amazon blocks automated lookups, so 3–8 are search links
that open the result list (pick a well-rated seller, "Prime" or ≥ 39 € total for free shipping).
Total ≈ 60 €, one parcel, no shipping. Without the logic analyzer ≈ 47 €.

## Alternative A: Reichelt (reichelt.de; article numbers are links to the product pages)
| Qty | Article no. | Item | Unit € | Use |
|----:|-------------|------|-------:|-----|
| 2 | [`BC 547B`](https://www.reichelt.de/index.html?ACTION=3&ARTICLE=5006) | NPN transistor TO-92 | 0.04 | DOUT driver stage (one spare) |
| 2 | [`1N 5819`](https://www.reichelt.de/index.html?ACTION=3&ARTICLE=41850) | Schottky diode 40 V 1 A DO-41 | 0.04 | 5 V feed into the ESP32 |
| 5 | [`1/4W 100K`](https://www.reichelt.de/index.html?ACTION=3&ARTICLE=1337) | carbon film resistor 100 kΩ 0.25 W | 0.09 | ADC dividers (top) |
| 10 | [`1/4W 10K`](https://www.reichelt.de/index.html?ACTION=3&ARTICLE=1338) | 10 kΩ | 0.10 | dividers (bottom / series) |
| 5 | [`1/4W 15K`](https://www.reichelt.de/index.html?ACTION=3&ARTICLE=1356) | 15 kΩ | 0.09 | logic-input dividers |
| 2 | [`1/4W 4,7K`](https://www.reichelt.de/index.html?ACTION=3&ARTICLE=1425) | 4.7 kΩ | 0.11 | pull-up at the transistor collector |
| 2 | [`1/4W 1,0K`](https://www.reichelt.de/index.html?ACTION=3&ARTICLE=1315) | 1 kΩ | 0.09 | base resistor |
| 1 | [`SL 1X36G 2,54`](https://www.reichelt.de/index.html?ACTION=3&ARTICLE=19504) | 36-pin header strip | 0.25 | jumper J1, test points |
| 5 | [`JUMPER 2,54 SW`](https://www.reichelt.de/index.html?ACTION=3&ARTICLE=9017) | jumper cap | 0.02 | J1 |
| 2 | [`H25PR050`](https://www.reichelt.de/index.html?ACTION=3&ARTICLE=8268) | perfboard 50 × 100 mm, 2.54 mm | 1.11 | the adapter board |
| 1 | [`STECKBOARD 1K2V`](https://www.reichelt.de/index.html?ACTION=3&ARTICLE=67678) | breadboard 640 + 200 contacts | 3.35 | first tests, the DevKit plugs in |
| 1 | [`STECKBOARD DBS`](https://www.reichelt.de/index.html?ACTION=3&ARTICLE=79056) | 140-piece wire-bridge set | 4.12 | breadboard wiring |

Subtotal ≈ 13 €, plus shipping (≈ 6 €). Alternative to the single resistors: [`K/RES-E12`](https://www.reichelt.de/index.html?ACTION=3&ARTICLE=119272),
610-piece E12 assortment, 7.27 €, if you want a stock for later.
Reichelt has **no** JST SM connectors (its "JST SM02B" hit is a different 3.5 mm series) and no cheap
logic analyzer (only a 108 € USB scope), so those come from Amazon.

## Alternative B: Amazon.de items only for the Reichelt route
| Qty | Item | Listing | Price |
|----:|------|---------|-------|
| 1 set | **JST SM 4-pin male + female pigtail pairs, 2.5 mm pitch, 22 AWG, ~15 cm** (sets of 10–15 pairs; we need 2 pairs, the rest are spares/for a second lead) | search "JST SM 4 Pin Stecker Buchse Kabel"; e.g. "Lyeteung 15 Paar JST SM 4 Pin Steckverbinder 150 mm 22AWG", or the 2/3/4-pin selectable set https://www.amazon.de/dp/B0GYJWPB7P (choose 4p) | ≈ 7–10 € |
| 1 | **USB logic analyzer 8 ch 24 MHz** (fx2lafw / Saleae-clone, works with PulseView) | https://www.amazon.de/dp/B08MXZYMJ5 | 13.35 € |
| 1 | Dupont jumper wire set, 120 pcs, 20 cm, M-M / M-F / F-F | search "Dupont Kabel 120 Stück 20cm"; any 4+ star set | ≈ 6–8 € |

Alternative for the analyzer: AZ-Delivery "Logic Analyzer 8 CH 24 MHz", 13.99 €, same hardware.

## Alternative C: Conrad (conrad.de) – only useful locally if you are near Wernberg-Köblitz (DE) or Linz (AT)
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
