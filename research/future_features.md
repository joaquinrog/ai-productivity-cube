# Research — Future-feature parking lot

Only enough research to decide whether to **reserve PCB resources now**. GPIO budget is 34/36 used, so
"reserve" mostly means *pads or a footprint on an existing bus*, not new pins.

| Feature | Benefit | HW cost (est.) | Power | Size | SW complexity | Reserve now? |
|---|---|---|---|---|---|---|
| **NFC** (tap phone to pair / tag actions) | instant pairing, context tags | NT3H2111 tag IC ~USD 1 + loop antenna on a face | ~0 (passive, harvested) | coil 20–30 mm on an axis face; conflicts with dock rings/magnets | low | **Yes: I2C footprint + antenna pads on face-A side** (DNP) |
| Camera / "what am I seeing?" | multimodal agent | OV2640/OV5640 + DVP needs ~11 pins | 100+ mA | lens through a display face | high | **No** (no pins; V2 board / ESP32-S3 with fewer panels) |
| Speaker | spoken replies, alerts | MAX98357A I2S amp + 15 × 11 mm speaker | 100–500 mA peaks | needs acoustic volume + grille | medium | **No** (reuse I2S? pins are used by PDM; revisit with V2) |
| Microphone array | far-field, noise suppression | +1 PDM mic (same CLK, 2nd DATA edge → **0 extra pins** on S3 stereo PDM) | +1 mA when on | 4 × 3 mm | medium | **Yes: second mic footprint on PDM DATA (L/R select)** — cheap, keep DNP |
| Wireless charging (Qi) | no dock alignment | RX coil + IC ~USD 5–8 | heat while charging | 30+ mm coil on an axis face | low | **No** for V1 (D-015) |
| UWB | precise desk/room presence | DW3000 module, SPI + 3 pins | 30–100 mA bursts | 10 × 10 mm module | high | **No** |
| Desktop USB data via dock | dock as HID / data | 2 rings + analog switch | ~0 | none | medium | **Yes: D+/D− rings reserved** on face B (not connected) |
| Capacitive touch on faces | swipe/tap on displays | ESP32-S3 touch pins are GPIO1–14 (all used) | µA | electrode under window | medium | **No** (IMU tap is the cheaper path; BMI323 fallback has tap) |
| Smarter dock (MCU, Wi-Fi, ambient light bar) | richer Desktop Mode | dock-side ESP32-C3 | external power | dock only | medium | **No change to cube** — dock can grow independently |
| Front-lit e-paper | readable in the dark | GDEY0154D67-FL04 + LED driver | ~5–15 mA when lit | +0.5–1 mm | low | **No** (V2 display option) |

### Net reservations for Phase B rev A
1. Second PDM mic footprint (DNP).
2. NFC tag IC footprint on I2C + antenna pads (DNP).
3. ALS footprint on I2C behind light pipe (DNP) — D-009.
4. D+/D− rings on the dock-pad PCB, unconnected.
