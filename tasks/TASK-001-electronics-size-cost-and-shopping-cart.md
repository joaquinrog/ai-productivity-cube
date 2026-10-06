# TASK-001 — Validate V1 Electronics, Size, Pocketability, Cost, and Build Prototype Shopping Cart

Status: **Complete — awaiting human review** · Opened/closed: 2026-10-05 · Owner: engineering agent
**Do not begin PCB design until this task is reviewed.**

## Answers to the objectives

| # | Question | Answer (→ detail) |
|---|---|---|
| 1 | Exact MCU/module? | **ESP32-S3-WROOM-1-N16R2** (Phase B); Adafruit ESP32-S3 Feather #5477 (Phase A) → D-002, `research/mcu.md` |
| 2 | Exact displays? | **1.54″ 200 × 200 B/W e-paper, SSD1681**: Waveshare #12955 modules (A), raw #12561 / GDEY0154D67 (B) → D-003, `research/displays.md` |
| 3 | Monochrome vs color? | **Monochrome** → D-004 |
| 4 | Exact IMU? | **Bosch BMI270** (alt. BMI323) → D-006, `research/imu.md` |
| 5 | Exact microphone? | Phase A **ICS-43434** I2S breakout (+ MP34DT01 PDM test); Phase B **Infineon IM69D130** PDM → D-008, `research/audio.md` |
| 6 | Exact haptic actuator/driver? | **TI DRV2605L + Vybronics VG1030001XH** LRA → D-007, `research/haptics.md` |
| 7 | Ambient-light sensor? | **No** in baseline; DNP footprint reserved → D-009 |
| 8 | Battery requirements? | 1S LiPo + PCM, 3.7/4.2 V, ≤ 30 × 40 × 8 mm, ~1000 mAh, ≥ 1 C, JST-PH → `research/battery.md` §1 |
| 9 | Actual battery candidates? | Cyberpuerta DP-80304 1000 mAh (MXN 177), Mercado Libre 803040 (MXN 149–416), UNIT 802535 650 mAh, 603040/103040 classes → `research/battery.md` §3 |
| 10 | Charger/power-path IC? | **TI BQ25180** (alt. BQ25185 for hand assembly) → D-010 |
| 11 | 3.3 V regulator? | **TI TPS63802 buck-boost** → D-010, `research/power.md` |
| 12 | Fuel gauge? | **MAX17048** → D-010 |
| 13 | Buttons/switch mechanism? | 2 × C&K PTS526 (260 gf, 0.25 mm) under a recessed PTT cap inside a 1 mm guard ring on face A + AUX key; BOOT hidden → D-014 |
| 14 | Dock contacts? | Concentric ENIG rings on face B (VBUS centre, GND outer; D+/D− reserved), Mill-Max 0906 pogo pins in the dock → D-015 |
| 15 | Magnet/alignment? | 4 × N52 Ø6 × 2 in face-B corners, same polarity → 90° detents; Hall-gated dock VBUS → `research/dock.md` |
| 16 | USB architecture? | **Option C**: dock charging + hidden service USB-C (native USB-Serial/JTAG) → D-016 |
| 17 | Debug/programming? | Native USB-Serial/JTAG over service USB-C; UART0 + EN + GPIO0 Tag-Connect pads; BOOT key → `research/architecture.md` §5 |
| 18 | Dev boards needed? | 2 × Feather #5477 (all Espressif DevKitC-1 are 0-stock at DK MX) |
| 19 | Breakouts needed? | BMI270 (SparkFun 22397), ICS-43434 (#6049), MP34DT01 (#3492), DRV2605L (#2305); optional VEML7700 (#4162) |
| 20 | Cables/connectors? | 6 × STEMMA QT, breadboards + jumpers, 2 × USB-C data; panel PH2.0 cables included; Phase B: FH12-24S, USB4105 |
| 21 | What moves to custom PCB? | Module, XTAL, charger, gauge, buck-boost, load switches, IMU, mic, haptic driver, 4 boosters + FPC connectors, keys, LED, service USB-C, ESD; separate dock-pad PCB → `research/architecture.md` §6 |
| 22 | Can 4 displays share one bus? | **Yes** (5 kB/frame ≈ 2–4 ms; refresh is waveform-bound) → `research/displays.md` §5 |
| 23 | Can inactive displays be power-gated? | **Yes, with zero visual cost** (bistable); one TPS22916; drive bus pins low first → §6 |
| 24 | Real power budget? | Standby 0.63 / 0.96 / 2.58 mA (opt/nom/pess); normal day 29–68 mAh → `electronics/power_budget.md` |
| 25 | Realistic battery life? | 1000 mAh: **~1–4 weeks** (normal use, link-dependent), ~9 days heavy; model until Test 9 measures it |
| 26 | What dimensions are pocketable? | ≤ 45 mm thick, ≤ 58 mm face, ≤ 100 g, 6 mm edge radius — Rubik's-class, not AirPods-class → `research/size_and_pocketability.md` |
| 27 | 55 × 55 × 40–45 better than 50³? | **Yes**: same volume, 8 mm thinner, more internal margin → `mechanical/SIZE_ENVELOPES.md` §3 |
| 28 | Realistic total mass? | **≈ 86 g model; 80–105 g realistic** |
| 29 | Phase A cost? | Goods MXN 5,475 (with PPK2) / 3,371 (without); **practical budget MXN 5,500 (PPK2 borrowed) or 8,500 (bought)** |
| 30 | Phase B electronics cost? | Goods MXN 3,915 (1,825 per-unit parts + 2,090 batch fees); landed **MXN 5,789** |
| 31 | First integrated prototype all-in? | **≈ MXN 9,750** (range 7,000–10,000) incl. mechanical + 25 % contingency |
| 32 | What dominates the BOM? | Recurring: **the four displays (40 % of per-unit parts)**. First unit: PCB/PCBA/DHL batch fees (36 %) |
| 33 | What to buy now? | Phase A cart sections 1–2 of `bom/SHOPPING_CART.md` (+ optional Phase B raw panels in the same Waveshare order) |

## Must-resolve questions (§48) — short answers
- ESP32-S3 best? **Yes for V1**; ESP32-C6 is the V2 power candidate. Variant: **WROOM-1-N16R2**. PSRAM: **yes, 2 MB quad**. Module vs bare: **module**.
- 4 screens on one bus? **Yes.** Refresh latency matters? **Yes — 0.3 s partial; designed around with haptics.** Power-gate? **Yes.**
- Best display tech: **e-paper**. Mono vs RGB: **mono**. I2S vs PDM: **PDM for Phase B, I2S on bench**. One mic: **yes**.
- DRV2605L worthwhile: **yes**. LRA vs ERM: **LRA** (confirm by A/B). Light sensor: **no (footprint only)**.
- MAX17048 vs alternatives: **MAX17048**. BQ24074 vs alternatives: **BQ25180**. LDO vs buck vs buck-boost: **buck-boost**.
- USB data vs power only: **data on the hidden service port; dock = power only in V1**. Dock exposes USB/UART: **not in V1 (rings reserved)**.
- Dock detection: **VBUS divider on RTC GPIO + BQ25180 /INT**. Pogo placement: **on the axis face B, concentric**. Button geometry: **large recessed PTT in a guard ring on face A**.
- Avoid pocket presses: **recess + 260 gf key + ≥ 150 ms hold + IMU heuristic (+ ALS fallback)**.
- Realistic capacity: **~1000 mAh (700 if the body shrinks)**. Runtime: **1–4 weeks normal**. Weight: **80–105 g**.
- Fits in 50 mm? **Barely (0.7 mm panel margin) — not recommended.** Flattened 55 × 55 × 40–45 better? **Yes.**
- Pocketable size: **55 × 55 × 42–45 realistic; 52 × 52 × 38 ideal; 58 × 58 × 45 max** — confirm with mockups.
- What dominates cost: **displays (recurring), batch PCB fees (first unit)**.
- Minimum bench prototype that proves the concept: **Feather + 4 e-paper modules + BMI270 + I2S mic + DRV2605L/LRA + 1 cell + 2 keys + phone app stub** (≈ MXN 3,400 goods without PPK2).

## Definition of Done

- [x] workspace initialized
- [x] PROJECT_BRIEF.md
- [x] CURRENT_STATE.md
- [x] DECISIONS.md
- [x] OPEN_QUESTIONS.md
- [x] architecture research (`research/architecture.md`)
- [x] exact MCU recommendation (D-002)
- [x] display comparison (`research/displays.md`)
- [x] monochrome vs color decision (D-004)
- [x] IMU recommendation (D-006)
- [x] microphone recommendation (D-008)
- [x] haptic recommendation (D-007)
- [x] power architecture (`research/power.md`, `electronics/block_diagram.md`)
- [x] battery recommendation (D-012)
- [x] dock architecture (D-015)
- [x] USB/debug architecture (D-016)
- [x] preliminary pin map (`electronics/preliminary_pinmap.md`)
- [x] power budget (`electronics/power_budget.md`)
- [x] mechanical feasibility analysis
- [x] size-envelope comparison
- [x] pocketability recommendation
- [x] physical mockup test plan
- [x] realistic mass estimate
- [x] Phase A BOM
- [x] Phase B BOM
- [x] current shopping cart with links/prices/stock
- [x] BOM.csv
- [x] cost breakdown
- [x] cost sensitivity analysis
- [x] alternate parts
- [x] source list
- [x] risk register
- [x] bring-up plan
- [x] next-task recommendation

## Known limitations of this task
- Mercado Libre / Amazon MX / UNIT pages block automated reads → marketplace prices are search-snippet estimates.
- Waveshare shipping to Mexico and JLC quotes not live-quoted (assumptions in the model).
- MAX17048 and IM69D130 electrical figures come from search summaries / memory of the datasheets — re-check when drawing the schematic.
- BLE keep-alive current is an assumption (0.25–2 mA) — the single biggest uncertainty in battery life.

## Next-task recommendation
**TASK-002 — Execute Phase A:** place the Phase A order, run bring-up Tests 1–11 (`electronics/bringup_plan.md`), and in
parallel run the pocketability mockup study (`mechanical/POCKETABILITY_TEST_PLAN.md`). Output: measured power numbers that
replace the model, a locked body thickness, and confirmed/superseded D-003…D-013 — the inputs the Phase B schematic needs.
