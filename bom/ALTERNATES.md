# Alternate parts

Checked 2026-10-05 at Digi-Key MX unless stated. "Penalty" = what we lose by switching.

| Function | Primary | Alternate | Price / stock | Penalty / when to use |
|---|---|---|---|---|
| Dev board | Adafruit Feather ESP32-S3 #5477 (USD 17.50, 328) | Espressif ESP32-S3-DevKitC-1-N8R8 / 1U-N8R8 | USD 15.00, **0** (ETA 2027) — check Mouser MX / local clones (N16R8) | octal PSRAM ≠ Phase B; clones = unknown quality |
| Dev board | — | Seeed XIAO ESP32S3 (Sense has PDM mic + camera) | not checked | tiny, fewer pins |
| MCU module | ESP32-S3-WROOM-1-N16R2 (USD 6.70, 7,110) | ESP32-S3-MINI-1-N4R2 | USD 5.37, 106 | 4 MB flash tight for OTA; smaller (good) |
| MCU module | — | ESP32-S3-WROOM-1U-N16R2 + 2.4 GHz flex antenna | — (check) | enables 52 × 52 × 38 / 55 × 55 × 42; RF tuning |
| MCU module | — | ESP32-S3-WROOM-1-N8R2 | USD 5.88, **0 until 2027-11** | — |
| Display (bench) | Waveshare #12955 (USD 9.99) | RobotShop "1.54″ e-Paper Module 200x200" | USD 11.99 | — |
| Display (raw) | Waveshare #12561 (USD 5.99) | Good Display GDEY0154D67 (direct/buy-lcd.com quote) | quote | same panel family |
| Display (fallback tech) | e-paper | Sharp LS013B7DH03 1.28″ memory LCD | USD 12.39, **27,094** | fast refresh; needs VCOM toggling, can't be gated, smaller |
| Display (rejected) | — | NHD-1.5-128128UGC3 RGB OLED | USD 24.55, 306 | 160 mA on / 2 mA sleep, burn-in |
| FPC connector | Hirose FH12-24S-0.5SH(55) (USD 2.41, 15,204) | JLC/LCSC 24P 0.5 mm bottom-contact | ~USD 0.1–0.3 | verify actuator style & height |
| IMU | BMI270 (USD 4.23, 52,386) | BMI323 | USD 3.91, 31,554 | +11 µA suspend; gains native orientation/tap |
| IMU | — | LSM6DSV16X | USD 5.75, **0** | best features (6D, MLC); no stock |
| IMU | — | ICM-42688-P | USD 4.86 | high-performance part, no orientation engine |
| IMU breakout | SparkFun 22397 (USD 18.50, 259) | SparkFun 21325 LSM6DSV16X | USD 24.54, 89 | different IMU |
| Mic (bench) | Adafruit #6049 ICS-43434 (USD 8.95, 1,282) | INMP441 modules (marketplace) | ~MXN 80–150 | legacy/clone quality |
| Mic (Phase B) | IM69D130 (USD 2.66) | ICS-43434 (I2S) | USD 3.92, 94,290 **obsolete** | last-time buy only |
| Mic (Phase B) | — | TDK T5838 MMICT5838-00-012 | USD 2.83, 67,466 | **1.8 V only** → extra rail + level shift; lowest current, AAD |
| Haptic driver | DRV2605LDGSR (USD 2.28, 4,661) | Renesas DA7280 | not checked | different library/effects |
| Haptic breakout | Adafruit #2305 (USD 7.95, 1,571) | SparkFun 14538 | USD 11.95, 187 | — |
| LRA | VG1030001XH (USD 3.22, 465) | VG0832012 (8 mm, 1 G) | USD 3.21, 1,316 | weaker |
| LRA | — | VG1040003D (10 mm, 2 G, 170 Hz) | USD 6.50, 9,672 | pressure contacts → spring pads needed |
| Charger | BQ25180YBGR (USD 3.01, 3,019) | BQ25185 (standalone, WSON 2.2 × 2) | not priced | no I2C; **hand-solderable** |
| Charger | — | BQ24074RGTR | USD 2.43, in stock | larger, no ship mode, higher drain |
| Fuel gauge | MAX17048G+T10 (USD 4.61, 24,141) | MAX17260 | not priced | needs sense resistor; better accuracy |
| 3.3 V regulator | TPS63802DLAR (USD 3.40, 19,575) | TPS62840 (buck, 60 nA Iq, 100 % mode) | not priced | rail sags to VBAT below 3.3 V |
| Load switch | TPS22916CYFPR (USD 0.63, 20,624) | P-MOSFET + gate resistor | cents | slower, more leakage |
| 32 kHz XTAL | Epson FC-135 (USD 2.66) | Abracon ABS07-32.768KHZ | ~USD 0.6 | check load capacitance |
| Battery | Cyberpuerta DP-80304 1000 mAh (MXN 177) | Mercado Libre 803040 listings | MXN 149–416 | verify PCM, polarity, dimensions |
| Battery | — | UNIT Electronics 802535 650 mAh | not readable | smaller body option |
| Pogo pin | Mill-Max 0906-0-15-20-76-14-11-0 (USD 0.81, 50,282) | Mill-Max 0906-1-15-20-75-14-11-0 (0.177″) | USD 0.86, 67,800 | longer stroke |
| Key | C&K PTS526 SK15 (USD 0.16, 203,592) | Alps SKRP series | not priced | different force/travel |
| Power profiler | Nordic PPK2 (USD 113.74, 1,336) | Joulescope / Otii Arc (lab) | — | borrow |
