# DECISIONS — ADR log

Status values:
- **Accepted**: part of the product definition (from the brief) or approved by the human reviewer.
- **Proposed**: TASK-001 recommendation backed by evidence; **awaiting human review**.
- **Superseded by D-xxx**: never edited in place; a new record replaces it.

All prices/stock checked **2026-10-05** unless noted. Evidence URLs are expanded in `bom/SOURCES.md`.

---

## D-001 — Phased prototype strategy
Status: **Accepted** · Date: 2026-10-05

### Decision
Phase A bench prototype (dev board + breakouts) → Phase B integrated prototype (custom PCB,
raw panels, enclosure, dock). No PCB design until TASK-001 is reviewed.

### Why
Proves buses, power, audio, haptics and interaction before money and time go into a PCB.

### Consequences
Two BOMs (A and B). Phase A parts are chosen to be the *same silicon* as Phase B where possible
(BMI270, DRV2605L, MAX17048, SSD1681 panel family, quad-PSRAM ESP32-S3).

---

## D-002 — MCU family and module
Status: **Proposed** · Date: 2026-10-05

### Decision
- MCU: **ESP32-S3**.
- Phase B module: **ESP32-S3-WROOM-1-N16R2** (16 MB flash, 2 MB *quad* PSRAM, PCB antenna, 18 × 25.5 × 3.1 mm).
- Phase A board: **Adafruit ESP32-S3 Feather 4 MB / 2 MB PSRAM (#5477)**.

### Why
- Wi-Fi + BLE in one certified module; native USB-Serial/JTAG (no USB-UART chip); hardware PDM-RX and I2S; dual core for Opus encode + BLE; mature ESP-IDF, LVGL/GxEPD2, ESP-ADF.
- Quad PSRAM (R2) does **not** consume GPIO35–37 (octal R8 does — WROOM-1 datasheet Table 3-1 note b). 2 MB is enough for audio buffering + TLS.
- 16 MB flash: dual OTA slots + fonts/assets with headroom.
- Stock: N16R2 7,110 pcs at USD 6.70; **N8R2 is 0-stock until 2027**; every Espressif DevKitC-1 is 0-stock or obsolete at Digi-Key MX → Feather 5477 (328 pcs, USD 17.50) is the practical dev board and has the same PSRAM class.

### Alternatives considered
- ESP32-S3-MINI-1-N4R2 (15.4 × 20.5 × 2.4, USD 5.37, 106 pcs): smaller, 4 MB flash tight for OTA. Good fallback.
- ESP32-S3-WROOM-1U-N16R2 + flex antenna: needed only if the body goes below ~42 mm on the axis (see D-013).
- ESP32-C6: light-sleep floor 34 µA vs 230 µA (ESP-IDF power_save README) — ~2.5× better standby, but single core, no PSRAM, less audio headroom. **V2 power candidate.**
- nRF52840/nRF5340: best BLE power, no Wi-Fi, Zephyr learning curve for the team. Rejected for V1.
- Bare ESP32-S3 chip: RF layout + certification risk. Rejected for V1.

### Evidence
ESP32-S3 datasheet v2.2 §5.6; WROOM-1 datasheet v1.8 Table 3-1; Digi-Key MX listings; ESP-IDF `examples/bluetooth/nimble/power_save/README.md`.

### Consequences
External 32.768 kHz crystal on GPIO15/16 required (D-011). Pin budget is tight (34 of 36 usable GPIO; see `electronics/preliminary_pinmap.md`).

---

## D-003 — Display technology: 1.54″ monochrome e-paper ×4 (replaces SSD1351 RGB OLED hypothesis)
Status: **Proposed** · Date: 2026-10-05

### Decision
Four **1.54″ 200 × 200 black/white e-paper panels (SSD1681 controller)**, one per display face.
Phase A: Waveshare 1.54″ e-Paper Module (#12955). Phase B: raw panel (Waveshare #12561 / Good Display GDEY0154D67) on 24-pin 0.5 mm FPC.

### Why
- **Bistable**: each face keeps showing `WORK / STUDY / AVAILABLE / DND` with **zero power**. With OLED/TFT the cube is a blank box whenever it sleeps — which is most of the time in Pocket Mode.
- Power: refresh 26.4 mW for 0.3 s (partial) per change; panels can be **hard power-gated** with no loss of image. A 1.5″ RGB OLED (NHD-1.5-128128UGC3) draws **160 mA typ** panel current when on and **2 mA in sleep mode** — ×4 = 8 mA just sleeping, which alone would cut standby from weeks to ~4 days on 1000 mAh.
- Viewing angle >170°, sunlight readable, paper-like, no burn-in (OLED datasheet warns of burn-in).
- Thin (1.05 mm) and cheap (USD 5.99 raw).

### Alternatives considered
- RGB OLED SSD1351 1.5″ (Waveshare #14747 USD 18.99 module; NHD raw USD 24.55): vivid, readable in dark; rejected on power, blank-when-asleep, burn-in, cost.
- Grayscale OLED SSD1327 (Waveshare #13992 USD 12.99): same power/blank issues.
- Sharp Memory LCD LS013B7DH03 (1.28″ 128 × 128, USD 12.39, 27,094 stock): 60 Hz updates at µW, but needs continuous VCOM toggling (cannot be power-gated without losing image), lower contrast, smaller (23 mm active). **Kept as fallback** if e-paper latency fails Test 3.
- TFT ST7789: backlight power, blank when off. Rejected.

### Evidence
Waveshare #12955 / #12561 pages; Good Display GDEY0154D67 page; NHD-1.5-128128UGC3 datasheet (ICC 160 mA typ, sleep 2 mA typ); Digi-Key LS013B7DH03.

### Consequences
- No readability in the dark (reflective). Front-lit variant GDEY0154D67-FL04 exists — parked.
- UI latency: 0.26–0.3 s partial refresh; full refresh (2 s, flashing) needed periodically to clear ghosting. UX must be designed around this (haptic gives instant feedback).
- Each panel needs its own small boost circuit (SSD1681 external MOSFET/inductor/diodes).
- Display subsystem ≈ 34 % of Phase A consumed BOM and ≈ 40 % of Phase B components (>35 % flag) — accepted because displays *are* the product; the OLED alternative would be ~60 %.

---

## D-004 — Monochrome, not color
Status: **Proposed** · Date: 2026-10-05

### Decision
Monochrome (1-bit, black/white) for V1.

### Why
The core UX is a 1–3 word context label, a time, a count, and a ✓/✗ — none need color. Color e-paper (3/4/6-color) refreshes in 10–20 s and has no partial refresh; color OLED costs power and bistability (D-003).

### Alternatives considered
RGB OLED (+USD 36 for 4 modules, +USD 74 for 4 raw panels vs e-paper), tri-color e-paper (too slow).

### Consequences
Icons and typography carry meaning; context can be differentiated by inverted backgrounds/patterns.

---

## D-005 — One shared SPI bus for 4 panels, single gated display rail
Status: **Proposed** · Date: 2026-10-05

### Decision
SCK, MOSI, DC, RST shared; **4 × CS** and **4 × BUSY** individual; all panels powered from one TPS22916 load switch (10 nA off).

### Why
SSD1681 is write-only over 4-wire SPI; frame is 5 kB (200 × 200 / 8). At 10–20 MHz a frame transfers in 2–4 ms — the 0.3 s refresh is waveform-bound, not bus-bound, so sharing costs nothing visible. Refreshes are serialized (one panel at a time) to cap peak current.

### Consequences
12 GPIO for displays. BUSY lines could be freed later by polling via 3-wire read (not validated).

---

## D-006 — IMU: Bosch BMI270; face detection in firmware
Status: **Proposed** · Date: 2026-10-05

### Decision
BMI270 (LGA-14 2.5 × 3 mm). Accelerometer-only low-power mode + any-motion / no-motion interrupts wake the MCU; the MCU classifies the up-face from the gravity vector with hysteresis. Gyro off except during gestures.

### Why
Lowest always-on current of the candidates (accel-only LP "down to 4 µA", suspend 3.5 µA; BMI270 DS Table "power modes"); step counter + activity recognition included; 52,386 pcs at USD 4.23; SparkFun breakout (#22397) for Phase A; ESP-IDF component available.

### Alternatives considered
- **BMI323** (USD 3.91): native orientation/flat/tap/tilt detection, but suspend 15 µA and accel-LP 45 µA (DS Table 10). Strong alternate if firmware orientation proves fiddly.
- **ICM-42688-P** (USD 4.86): APEX pedometer/tilt/tap/WoM, but designed for high-performance motion (0.88 mA LN 6-axis); no orientation engine. Not a fit.
- **LSM6DSV16X**: excellent (6D orientation interrupt, MLC/FSM, 0.65 mA combo) but the IC is **0-stock at Digi-Key MX**; breakout USD 24.54.

### Consequences
Mount with IMU Z along the rotation axis so the four faces map to ±X/±Y.

---

## D-007 — Haptics: DRV2605L + 10 mm LRA
Status: **Proposed (pending Phase A blind A/B test)** · Date: 2026-10-05

### Decision
TI **DRV2605LDGSR** driving a **Vybronics VG1030001XH** LRA (10 mm, 210 Hz, ≥2.0 G on a ~100 g jig, 135 mArms max, wire leads). Driver on VSYS, not on the 3.3 V rail.

### Why
Consumer-grade "click" needs auto-resonance tracking, overdrive and active braking (LRA alone: rise ≤50 ms, fall ≤100 ms per DS; DRV2605L shortens both). 123-effect ROM library = distinct confirm / error / pending / notify patterns without custom waveforms. ERM is slow and buzzy.

### Alternatives
ERM + MOSFET (saves ~USD 4, "toy" feel); Renesas DA7280; VG1040003D (2 G, pressure contacts).

### Consequences
DRV2605L shutdown current is 4 µA (not nA) — accepted in budget.

---

## D-008 — Single microphone; I2S on the bench, PDM in Phase B
Status: **Proposed** · Date: 2026-10-05

### Decision
One mic. Phase A: Adafruit #6049 (ICS-43434 I2S). Phase B: **Infineon IM69D130** PDM (69 dB SNR, 1.62–3.6 V, bottom port) on ESP32-S3 PDM-RX. Mic rail hard-gated.

### Why
PTT speech at 10–30 cm needs no array. ICS-43434 is **obsolete** at Digi-Key (last-time stock 94,290) — fine for a bench, not for a product. TDK's suggested replacements (T5837/T5838) are **1.8 V-only** → would need an extra rail + level shifting. IM69D130 runs from 3.3 V directly. PDM uses 2 pins instead of 3.

### Alternatives
ICS-43434 last-time-buy; TDK T5838 (330 µA, acoustic activity detect) if a 1.8 V rail is added in V2; Knowles/Syntiant SPH0645LM4H-B (I2S, ESP32 timing quirk).

---

## D-009 — Ambient-light sensor: not in baseline (footprint reserved, DNP)
Status: **Proposed** · Date: 2026-10-05

### Decision
No ALS in the V1 baseline. Reserve an I2C footprint (VEML7700 / LTR-303 class) behind the face-A light pipe, **do not populate** unless Phase A pocket tests show PTT false triggers that IMU + button guard cannot solve.

### Why
Its main job — display auto-brightness — disappears with reflective e-paper (D-003). Remaining value is pocket detection, which is unproven.

---

## D-010 — Power architecture
Status: **Proposed** · Date: 2026-10-05

### Decision
`Dock/USB 5 V → BQ25180 (linear, power path, I2C, ship mode) → VSYS → TPS63802 buck-boost → 3V3`;
`MAX17048` fuel gauge on the cell; `TPS22916` load switches for display and mic rails; DRV2605L on VSYS.
Charge current 400 mA (≈0.4 C on 1000 mAh) — revisit with thermal test.

### Why
- BQ25180: 1 A power path (runs from dock with any battery state), ship mode 3.2 µA, 15 nA shutdown, push-button reset, 1.6 × 1.1 mm. USD 3.01, 3,019 pcs.
- TPS63802: holds 3.3 V across the full 4.2 → 3.0 V cell range with 2 A capability (ESP32-S3 Wi-Fi TX 340 mA peak), 11 µA Iq. An LDO drops out below ~3.4–3.5 V and wastes the last 10–15 % of the cell; TPS63900 (75 nA Iq) is limited to ~400 mA — too little margin for Wi-Fi + panel + haptics.
- MAX17048: ModelGauge, no sense resistor, 3 µA hibernate, same part already on the Feather.

### Alternatives
BQ25185 (standalone, WSON — easier hand assembly), BQ24074 (older, QFN-16, no ship mode), MCP73871; MAX17260; LDO.

### Consequences
DSBGA charger requires machine assembly (JLCPCB). Linear charging from 5 V at 400 mA dissipates ≈0.57 W in the cube — must be thermally tested (risk R-13).

---

## D-011 — External 32.768 kHz crystal is mandatory
Status: **Proposed** · Date: 2026-10-05

### Decision
Fit an Epson FC-135 32.768 kHz crystal on GPIO15/GPIO16 (XTAL_32K_P/N).

### Why
ESP-IDF BLE power-save measurements for ESP32-S3: light-sleep floor **230 µA with 32 kHz XTAL vs 3.3 mA with main XTAL** — a 14× difference that dominates Pocket-Mode standby.

---

## D-012 — Battery: 1S LiPo, 30 × 40 mm footprint, ~1000 mAh baseline
Status: **Proposed** · Date: 2026-10-05

### Decision
1S Li-polymer with protection (PCM), 3.7 V nominal / 4.2 V max, **30 × 40 mm footprint, ≤ 8 mm thick, ~1000 mAh (803040)** for the 55 mm body; 603040 (~700 mAh) if the body shrinks. Buy locally (hazmat import restrictions).

### Why
With reflective displays the battery is no longer the size driver: modeled normal-day use is ~29 mAh/day (nominal) to ~68 mAh/day (pessimistic BLE link) → 1000 mAh lasts ~12–29 days. A 30 × 40 footprint fits the 47 mm core of a 55 mm body with room for the LRA beside it. Peak load ≈0.5 A (≤0.5 C) is within a standard 1 C cell.

---

## D-013 — Body geometry: flattened cube, rotation axis along the short dimension
Status: **Proposed (pending pocketability mockup test)** · Date: 2026-10-05

### Decision
- Rotation axis = short dimension; the two square faces are the interaction faces; the four display faces are W × H rectangles.
- **Phase B rev A: 55 × 55 × 45 mm** (WROOM-1 PCB antenna, comfortable margins).
- Stretch: **55 × 55 × 42** (or 52 × 52 × 38) using WROOM-1U + flex antenna on face A.
- Maximum acceptable: **58 × 58 × 45**.

### Why
Same volume as a 50 mm cube (≈123 vs 121 cm³) but 8 mm thinner where it matters (pocket bulge). The 1.54″ panel (31.8 × 37.3 mm) sets the floor: H ≥ 36.4 mm with a flex antenna, ≥ 42.1 mm if the PCB antenna needs a panel-free band. See `mechanical/SIZE_ENVELOPES.md`.

---

## D-014 — Face allocation
Status: **Proposed** · Date: 2026-10-05

### Decision
- **Face A (user face):** PTT key (large, recessed inside a raised guard ring), secondary key, mic port, status LED / light pipe, removable cap hiding the service USB-C + BOOT.
- **Face B (dock face):** concentric gold contact rings + 4 magnets. No buttons.

### Why
Pogo contacts and buttons on the same face fight for area and make docking press buttons. Putting them on opposite axis faces means: docked → face A faces the user, PTT stays reachable; the contact pattern is rotation-invariant.

---

## D-015 — Dock: side-wall magnetic dock with concentric ring contacts (no Qi)
Status: **Proposed** · Date: 2026-10-05

### Decision
Cube face B has 2–4 concentric ENIG rings (VBUS, GND, reserved D+/D−). The dock has a vertical wall with spring pogo pins (Mill-Max 0906 series, springs in the dock) on a radial line and 4 magnets. Cube sits on a display face; any of the 4 rotations makes contact; magnets (all same polarity) give 90° detents. Dock detect = VBUS present (BQ25180 /INT + GPIO divider).

### Why
Rotation-invariant contact, no moving springs on the pocket device, cheap, no Qi coil (Qi adds a 30+ mm coil, ferrite, heat, and a receiver IC to a full cube face).

---

## D-016 — USB & debug: dock charging + hidden service USB-C
Status: **Proposed** · Date: 2026-10-05

### Decision
Option C. Internal USB-C (GCT USB4105-GF-A) on the main PCB behind the removable face-A cap → ESP32-S3 native USB-Serial/JTAG (flash, logs, JTAG debug) + charging on the bench. UART0 + EN + GPIO0 on Tag-Connect-style pads for recovery. Dock D+/D− rings reserved for evaluation in a later dock revision.

### Why
No external opening on the pocket device; full debug for the team; dock remains the user's only interaction for charging.

---

## D-017 — Sourcing policy
Status: **Proposed** · Date: 2026-10-05

Semiconductors from Digi-Key MX (prices in USD, CPT: taxes paid on delivery; free shipping ≥ USD 100) or Mouser MX (DDP). E-paper from Waveshare/Good Display (not stocked by Digi-Key MX). **LiPo cells bought locally** (Class 9 hazmat for import). PCB/PCBA from JLCPCB (China-origin courier imports pay 33.5 % since 2025-08-15).

---

## D-018 — Push-to-talk only in V1
Status: **Accepted** (brief) · Date: 2026-10-05

## D-019 — Phone = gateway, cloud = intelligence; no LLM on the MCU
Status: **Accepted** (brief) · Date: 2026-10-05
