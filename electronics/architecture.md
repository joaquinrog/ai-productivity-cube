# Electronics architecture (proposed V1)

Status: **Proposed — awaiting TASK-001 review.** Rationale: `research/*`. Decisions: D-002 … D-016.

## Summary

| Block | Phase A (bench) | Phase B (integrated) |
|---|---|---|
| MCU | Adafruit ESP32-S3 Feather 4 MB/2 MB PSRAM (#5477) | ESP32-S3-WROOM-1-N16R2 + 32.768 kHz XTAL |
| Displays | 4 × Waveshare 1.54″ e-Paper Module #12955 | 4 × raw 1.54″ SSD1681 panel + per-panel booster + FH12-24S FPC |
| Display power | module 3V3 (ungated) | TPS22916C gated rail 3V3_EPD |
| IMU | SparkFun BMI270 (#22397) on Qwiic | BMI270 on main PCB, Z = rotation axis |
| Mic | Adafruit ICS-43434 I2S (#6049) + MP34DT01 PDM (#3492) | IM69D130 PDM, TPS22916C gated rail 3V3_MIC |
| Haptics | Adafruit DRV2605L (#2305) + VG1030001XH LRA | DRV2605L on VSYS + VG1030001XH |
| Charger / path | Feather on-board charger | BQ25180 (I2C, power path, ship mode) |
| Regulator | Feather on-board LDO | TPS63802 buck-boost 3.3 V |
| Fuel gauge | Feather on-board MAX17048 | MAX17048 |
| Keys | 12 mm tact + PTS526 feel samples | 2 × PTS526 (PTT, AUX) + BOOT |
| USB | Feather USB-C | internal service USB-C (USB4105) → native USB-Serial/JTAG |
| Dock | pogo coupon experiment | face-B ring PCB + dock with Hall-gated VBUS |
| ALS | optional VEML7700 experiment | footprint only (DNP) |

## Buses

| Bus | Devices | Notes |
|---|---|---|
| **SPI (FSPI, write-only)** | 4 × SSD1681 | SCK/MOSI/DC/RST shared, CS×4, BUSY×4; ≤ 10 MHz on long traces |
| **I2C0 (400 kHz)** | BMI270 0x68, DRV2605L 0x5A, MAX17048 0x36, BQ25180 0x6A, (ALS 0x10 DNP), (NFC DNP) | 4.7 kΩ pull-ups to always-on 3V3; no address clash (BQ25180 7-bit 0x6A confirmed in TI DS §I2C; DRV2605L 0x5A fixed; BMI270 0x68/0x69) |
| **PDM-RX (I2S0)** | IM69D130 (+ DNP 2nd mic) | CLK + DATA |
| **USB FS** | service USB-C | GPIO19/20 |
| **UART0** | test pads | GPIO43/44 |

## Power domains

| Domain | Source | Always on? | Loads |
|---|---|---|---|
| VBAT | cell (PCM) | yes | MAX17048 sense, BQ25180 BAT |
| VSYS | BQ25180 SYS | yes | TPS63802 in, DRV2605L |
| 3V3 | TPS63802 | yes | ESP32-S3, BMI270, I2C pull-ups, LED |
| 3V3_EPD | TPS22916C #1 (EN GPIO42) | gated | 4 panels + boosters |
| 3V3_MIC | TPS22916C #2 (EN GPIO37) | gated | PDM mic |

Block diagram: `block_diagram.md`. Pins: `preliminary_pinmap.md`. Budget: `power_budget.md`.
