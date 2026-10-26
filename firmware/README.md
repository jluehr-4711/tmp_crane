# Firmware

ESP-IDF projects for the classic ESP32 (see `docs/`).

| Project | Purpose |
|---------|---------|
| `sniffer/` | Measurement tool for sessions 3/4 and the replay test of session 6: ADC probes, DOUT PWM capture, speed-pulse timing, UART sniff, PWM output. Usage in `docs/07-sniffer.md`. |

Build (ESP-IDF v5.5 installed under `~/esp/esp-idf`, toolchain under `~/.espressif`):
```
. ~/esp/esp-idf/export.sh
cd firmware/sniffer
idf.py set-target esp32      # once
idf.py build
idf.py -p /dev/ttyUSB0 flash monitor   # Ctrl+] leaves the monitor
```
