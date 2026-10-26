# Perfboard layout of the adapter board

`gen_layout.py` holds the layout as data (component holes, bottom-side links, top-side jumpers),
validates it (every net one connected graph, no hole with two nets, pin/net sets equal to the
schematic in `../kicad/`), and renders `layout.svg` plus the link table `links.md`.

Board: 5 x 7 cm double-sided prototype board, 18 x 24 holes, 2.54 mm. Hole (1,1) is top-left when
looking at the component side. The ESP32 is **not** on the board: header H1 (1x8, column 17) takes
female-female Dupont wires to the DevKit pins 5V(VIN), GPIO16, GPIO2, GPIO27, GPIO34, GPIO25, GPIO26, GND.

```
python3 gen_layout.py      # prints "layout OK" or the conflict, writes layout.svg and links.md
```
