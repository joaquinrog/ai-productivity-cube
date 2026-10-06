# Power budget (Phase B design, model)

Generated from `tools/cube_model.py` (2026-10-05). **These are model outputs to be replaced by PPK2
measurements in Tests 8–9**, not battery-life claims. Battery current = rail current × 3.3 / (3.7 × η),
η = 0.80 at sleep loads, 0.90 active (TPS63802, assumption); usable capacity = 85 % of nameplate.

## 1. Per-subsystem currents

| Subsystem | Sleep | Idle | Typical active | Peak | Duty cycle (normal day) | Source |
|---|---:|---:|---:|---:|---|---|
| ESP32-S3 (CPU) | 7–8 µA deep · **230 µA light (32 kHz XTAL)** | 27.6 mA modem-sleep 160 MHz idle | 40 mA (160 MHz, 1 core) | 66–92 mA (dual-core 160–240 MHz) | ~0.3 % awake | DS v2.2 T.5-9/5-10; ESP-IDF power_save |
| PSRAM 2 MB quad | +40 µA in light sleep | — | — | — | always | DS T.5-10 note |
| BLE | — | link keep-alive **+0.25 / 0.55 / 2.0 mA** (opt / nom / pess) | ~45 mA avg while streaming audio | 176 mA TX @0 dBm | PTT ≈ 160 s/day | DS T.5-8; keep-alive = **assumption** |
| Wi-Fi | off | off in pocket | ~120 mA mixed | 340 mA TX 802.11b | docked / fallback only | DS T.5-7; mix = assumption |
| Active display (1 panel) | 0 | 0 | 8 mA × 0.3 s | ~8 mA + booster inrush | ~70 s/day | Waveshare 26.4 mW |
| Inactive displays (3–4) | **0 (gated)** · 0.7–1 µA each if only deep-slept | — | — | — | always | SSD1681 DS; TPS22916 10 nA |
| IMU BMI270 | 3.5 µA suspend | **25 µA** accel-LP + features (assumption; DS "down to 4 µA") | 685 µA 6-axis | ~1 mA | always LP | Bosch DS |
| Mic IM69D130 | 0 (gated) | — | ~1 mA | ~1 mA | PTT only | Infineon (verify) |
| Haptics DRV2605L + LRA | 4 µA (EN low) | 0.5 mA (EN high) | ~110 mA | 135 mArms | ~10 s/day | TI DS; Vybronics DS |
| Ambient-light sensor | **not fitted** (D-009) | — | — | — | — | — |
| Fuel gauge MAX17048 | 3 µA hibernate | 23 µA active | — | — | always | ADI |
| Charger BQ25180 (battery side) | 3–4 µA | — | — | — | always | TI DS |
| Regulator TPS63802 | 11 µA Iq | η ≈ 80 % at µA–mA | η ≈ 90 % | 2 A capability | always | TI DS; η assumption |

Standby from the battery: **0.63 mA (optimistic) · 0.96 mA (nominal) · 2.58 mA (pessimistic)** — the BLE keep-alive
assumption dominates everything else combined.

## 2. Scenarios (mAh per 24 h)

| Scenario | Assumptions | Standby | PTT audio | Face changes | Status/timer | Haptics | Wi-Fi | **Total** |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **A — Pocket standby** | BLE linked, no use | 23.1 | 0 | 0 | 0 | 0 | 0 | **23.1** |
| **B — Normal day** | 20 PTT × 8 s, 40 rotations, 30 status, 2 h focus timer (1/min), 40 haptics | 23.1 | 3.8 | 0.6 | 1.1 | 0.4 | 0 | **29.0** |
| **B′ — Normal day, pessimistic BLE** | same, keep-alive 2 mA | 61.9 | 3.8 | 0.6 | 1.1 | 0.4 | 0 | **67.8** |
| **C — Heavy day** | 60 PTT × 12 s, 150 rotations, 100 status, 6 h timer, 150 haptics, 5 min Wi-Fi, pessimistic BLE | 61.9 | 17.0 | 2.2 | 3.3 | 1.5 | 9.9 | **95.9** |
| **D — Docked** | external 5 V; Wi-Fi associated ~30 mA @3.3 V + 400 mA charge | — | — | — | — | — | — | **0 from battery**; input ≈ 0.45 A × 5 V ≈ 2.2 W; heat ≈ 0.6–0.7 W |

## 3. Runtime (days, 85 % usable)

| Battery | A standby | B normal | B′ normal (pess.) | C heavy |
|---|---:|---:|---:|---:|
| 500 mAh | 18.4 | 14.7 | 6.3 | 4.4 |
| 700 mAh | 25.7 | 20.5 | 8.8 | 6.2 |
| **1000 mAh** | **36.8** | **29.3** | **12.5** | **8.9** |
| 1200 mAh | 44.1 | 35.2 | 15.0 | 10.6 |

**Realistic statement for V1 (until measured):** with a 1000 mAh cell, *about 1–4 weeks* depending mostly on how the
phone keeps the BLE link; heavy users ~1 week; docked use is unlimited. Docked charge 1000 mAh at 400 mA ≈ 2.5–3 h.

## 4. Sensitivity — why the architecture matters
- **Without the 32 kHz crystal:** light-sleep floor 3.3 mA → standby ≈ 4.4 mA from the battery → 1000 mAh ≈ **8 days doing nothing**.
- **With 4 RGB OLEDs (NHD-1.5) merely in sleep mode:** +8 mA → 1000 mAh ≈ **4 days**; plus 160 mA when lit.
- **With an LDO instead of buck-boost:** ~10–15 % of capacity unusable below ~3.5 V.
- **The phone dominates:** connection interval/latency negotiated by iOS/Android sets the keep-alive cost (0.25 → 2 mA = 8×).
  Phase A Test 7 must measure it with the real phone app.

## 5. Peak current
Battery-side worst case ≈ **0.56 A** (Wi-Fi TX + CPU + panel on 3V3 ≈ 0.41 A through the buck-boost, plus ~0.15 A haptic on VSYS).
Within a 1 C cell and BQ25180's 2.5 A discharge path.
