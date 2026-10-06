# Research — MCU / RF module

Checked 2026-10-05. Decision: D-002, D-011.

## 1. Is ESP32-S3 the right MCU?

| Requirement | ESP32-S3 | Notes |
|---|---|---|
| BLE to phone (primary link) | BLE 5, 0 dBm TX 176 mA peak, RX 93 mA peak (DS Table 5-8) | |
| Wi-Fi (docked / direct-to-cloud fallback) | 802.11 b/g/n, TX 340 mA peak @21 dBm (Table 5-7) | regulator must handle it |
| PTT audio capture + encode | I2S + **hardware PDM-RX**; dual LX7 @240 MHz for Opus + BLE | |
| Low power | Deep sleep 7–8 µA; light sleep 240 µA (DS Table 5-10); **BLE light-sleep floor 230 µA with 32 kHz XTAL, 3.3 mA without** (ESP-IDF power_save README) | 32 kHz XTAL mandatory |
| USB flashing/debug without extra chip | Native USB-Serial/JTAG on GPIO19/20 | |
| Firmware ecosystem | ESP-IDF, NimBLE, ESP-ADF, LVGL, GxEPD2, Arduino | strong for a student team |

**Verdict: yes for V1.** The power penalty vs. alternatives (below) is real but not decisive because
the e-paper architecture already puts standby in the multi-week range.

### Alternatives

| MCU | Pros | Cons | Verdict |
|---|---|---|---|
| ESP32-C6 | Light-sleep floor **34 µA** (same README), Wi-Fi 6 TWT, BLE 5.3, cheaper | single 160 MHz core, no PSRAM, smaller audio headroom; PDM-RX support to verify | **V2 power candidate** |
| ESP32-C3 | cheap, 140 µA floor | single core, no PSRAM, no PDM-RX | no |
| nRF52840 / nRF5340 / nRF54L | best-in-class BLE current (µA-level connected) | no Wi-Fi; Zephyr ramp-up | no for V1 |
| ESP32-S3 bare chip | smallest | RF layout + certification | no for early revisions |

## 2. Exact module

| Module | Flash / PSRAM | Size (mm) | Price / stock @DK MX | GPIO impact |
|---|---|---|---|---|
| **ESP32-S3-WROOM-1-N16R2** ✅ | 16 MB / 2 MB quad | 18 × 25.5 × 3.1 | **USD 6.70, 7,110 pcs** | GPIO35–37 free |
| ESP32-S3-WROOM-1-N8R2 | 8 MB / 2 MB quad | 18 × 25.5 × 3.1 | USD 5.88, **0 pcs (ETA 2027-11)** | free |
| ESP32-S3-WROOM-1-N8R8 | 8 MB / 8 MB **octal** | same | USD 6.32, in stock | **loses GPIO35–37** |
| ESP32-S3-MINI-1-N4R2 | 4 MB / 2 MB quad | 15.4 × 20.5 × 2.4 | USD 5.37, 106 pcs | free |
| ESP32-S3-MINI-1-N8 | 8 MB / none | 15.4 × 20.5 × 2.4 | USD 5.43, in stock | free |

### Do we need PSRAM? How much?
- E-paper framebuffers are tiny (4 × 5 kB).
- Audio: 10 s of 16 kHz/16-bit PCM = 320 kB — buffering a full utterance when the BLE link is slow
  or the phone app is suspended needs PSRAM; Opus-compressed it's ~20–30 kB but the encoder
  itself wants working memory.
- Wi-Fi + BLE coexistence + TLS (direct-to-cloud fallback) consume ~100–150 kB of internal SRAM.
- **2 MB quad PSRAM is enough and costs ~USD 0.8.** 8 MB octal (N8R8) is not justified and costs 3 GPIO
  plus ~100 µA more in light sleep (DS: 140 µA for 8 MB octal vs 40 µA for 2 MB quad).

### Module vs bare chip
Module for Phase B (pre-certified RF, antenna matched, crystal and flash included).

## 3. GPIO availability
WROOM-1 exposes 36 GPIO. After strapping (0, 3, 45, 46), USB (19, 20), UART0 (43, 44) and
32 kHz XTAL (15, 16), the design uses **34 of 36** — see `electronics/preliminary_pinmap.md`.
Pins that can be freed if needed: IMU_INT2, FG_ALRT (poll instead).

## 4. Wi-Fi/BLE coexistence
Software coexistence (time-sliced) on a shared 2.4 GHz radio. Rule for V1: **BLE is primary**; Wi-Fi
only docked or as fallback; never stream audio over BLE while Wi-Fi is scanning.

## 5. Antenna keep-out
WROOM-1 PCB antenna needs the board-edge keep-out from the module datasheet §"Keepout Zone"
and no metal (battery pouch, magnets, LRA, panel backplanes) in front of it. In the cube this
requires either a ~8 mm panel-free band next to face A (drives H ≥ 42.1 mm) or the WROOM-1U
with a flex antenna on the face-A cap (H ≥ 36.4 mm). See `mechanical/INTERNAL_PACKAGING.md`.

## 6. Dev board for Phase A
Every Espressif ESP32-S3-DevKitC-1 variant is **0-stock or obsolete** at Digi-Key MX (2026-10-05).
**Adafruit ESP32-S3 Feather 4 MB/2 MB PSRAM (#5477)**: USD 17.50, 328 pcs, LiPo charger + MAX17048
on board, STEMMA QT, 52.3 × 22.7 mm. Caveat: ~100 µA deep-sleep draw from the LiPo (Adafruit page)
→ standby numbers must be measured on Phase B hardware or with board-level isolation.
