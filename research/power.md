# Research — Power architecture

Checked 2026-10-05. Decision: D-010, D-011. Budget: `electronics/power_budget.md`.

## 1. Rails and loads

| Load | Rail | Peak | Notes |
|---|---|---|---|
| ESP32-S3 module | 3V3 | **340 mA** Wi-Fi TX (DS T.5-7); 176 mA BLE TX @0 dBm | needs 3.0–3.6 V |
| 4 × e-paper (one refreshing at a time) | 3V3_EPD (gated) | ~8 mA + booster inrush | 26.4 mW per refresh |
| PDM mic | 3V3_MIC (gated) | ~1 mA | only during PTT |
| BMI270, MAX17048 | 3V3 always-on | < 1 mA | |
| DRV2605L + LRA | **VSYS** | ~135 mArms | keep haptic surges off the 3V3 rail |
| BQ25180 | VBUS / VBAT | 1 A charge max | |

## 2. Regulator: LDO vs buck vs buck-boost

LiPo: 4.2 V full → 3.7 V nominal → ~3.0–3.3 V usable end. ESP32-S3 needs ≥ 3.0 V.

| Option | Example | Pros | Cons | Verdict |
|---|---|---|---|---|
| LDO 3.3 V | 300 mV-dropout class | cheapest, quiet, ~1–2 µA Iq parts exist | drops out below ~3.5–3.6 V at Wi-Fi load → last **~10–15 %** of capacity unusable, brown-out risk on TX bursts; efficiency = 3.3 / VBAT (≈85 % avg) | no |
| Buck with 100 % mode | TI TPS62840 (60 nA Iq, 750 mA) | best light-load efficiency | below 3.3 V the rail tracks VBAT − I·R → 3.0–3.3 V; TX bursts near 3.0 V risk brown-out | **alternate** |
| **Buck-boost** | **TI TPS63802** (2 A, 11 µA Iq, 3 × 2 mm) | regulated 3.3 V over the whole 4.2→3.0 V range, handles 340 mA peaks with margin | 11 µA Iq; needs 0.47 µH inductor | ✅ |
| Ultra-low-Iq buck-boost | TI TPS63900 (75 nA Iq) | tiny Iq | ">400 mA for VI ≥ 2.0 V" — not enough margin for Wi-Fi + panel + inrush | no |

11 µA Iq is ~1 % of the ~0.9 mA BLE-connected standby, so the buck-boost costs almost nothing in
standby and buys the full battery range.

## 3. Charger / power path

| | **BQ25180** ✅ | BQ25185 | BQ24074 |
|---|---|---|---|
| Type | linear, I2C, power path | linear, standalone (resistor-set) | linear, standalone |
| Charge current | 5 mA – 1 A | 5 mA – 1 A | 100 mA – 1.5 A |
| SYS | regulated 4.4–4.9 V or VBAT tracking | regulated 4.5 V | DPPM, OUT |
| Battery quiescent | **3–4 µA** (IQ_BAT) | 4–5 µA | 4.3–6.5 µA (BAT sleep) |
| Ship mode | **3.2 µA w/ button wake; 15 nA shutdown** | factory mode | SYSOFF (BQ24075/9 only) |
| Input | 25 V tolerant, 3.0–5.9 V operating | 3–18 V | 28 V rated |
| Package | DSBGA-8 1.6 × 1.1 (machine assembly) | WSON-10 2.2 × 2.0 | VQFN-16 3 × 3 |
| DK MX | USD 3.01, 3,019 pcs | — | USD 2.43 |

BQ25180 adds I2C control (charge current per thermal state, status, faults, ship mode) in the
smallest footprint. **BQ25185** is the pick if the team insists on hand assembly (no BGA).

### Charging while running
Power path: with dock VBUS present, SYS is regulated from VIN; the battery charges with what is
left of the input current limit. Desktop Mode runs from the dock even with a dead battery.

### Charger thermal behaviour
Linear loss = (VIN − VBAT) × ICHG. At 400 mA and VBAT = 3.6 V: **≈0.56 W** inside a sealed
~120 cm³ plastic body, plus the system load. Expect a few °C to ~10 °C rise near the charger and
cell. Mitigations: ICHG 300–400 mA (≈0.3–0.4 C), use BQ25180 thermal regulation, pad the charger to a
copper pour, keep the cell away from the charger, measure in Test 8 with a thermocouple. A
switching charger (e.g. BQ25619) is the V2 escape if heat is a problem.

## 4. Fuel gauge
**MAX17048** (ModelGauge, no sense resistor, 3 µA hibernate / 23 µA active, I2C 0x36, ALRT pin).
Good enough for a % indicator; accuracy improves with a custom cell model (ADI service) — not needed
for V1. Alternative: MAX17260 (m5 EZ, coulomb + model, needs sense resistor) if SoC error > ±5 %
in Test 9. ESP32 ADC-only SoC is rejected (load-dependent voltage on LiPo → ±10–20 % error).

## 5. Gating
- **3V3_EPD**: TPS22916C (10 nA off, 2 A). Enable pin on a glitch-free GPIO (GPIO42).
- **3V3_MIC**: TPS22916C. Enable on GPIO37.
- DRV2605L: EN pin low → 4 µA.
- Always-on 3V3: ESP32-S3, BMI270, MAX17048 (on VBAT directly), I2C pull-ups (4.7 kΩ to 3V3 — they
  draw nothing while the bus idles high).

## 6. Peak current check (battery side)
Wi-Fi TX 340 mA + CPU 60 mA + panel 10 mA on 3V3 → 3.3 × 410 / (3.7 × 0.9) ≈ 406 mA from the cell,
plus haptic ~150 mA on VSYS → **≈0.56 A worst case** (≈0.56 C on 1000 mAh; a 1 C cell is fine).
Firmware rule: no Wi-Fi TX burst + haptic + panel refresh simultaneously at < 15 % SoC.

## 7. Power block diagram
See `electronics/block_diagram.md` (Mermaid).

## 8. Ship mode and recovery
Factory/storage: BQ25180 ship mode (3.2 µA) — cube is "off" until the AUX key or dock power wakes it.
BQ25180 push-button long-press hardware reset is the last-resort recovery if firmware hangs (wire AUX
key to TS/MR with isolation; confirm in schematic review — TS function is lost when used as MR, which
is acceptable because the selected cells have no NTC lead).
