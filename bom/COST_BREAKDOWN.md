# Cost breakdown

Price checked **2026-10-05** · FX **18.50 MXN/USD** · all MXN unless stated · generated figures from
`python3 tools/cube_model.py`. Method and tax assumptions: `research/cost_model.md`.

## 1. Reusable development hardware (Phase A tooling)

| Item | Goods MXN |
|---|---:|
| 2 × Adafruit ESP32-S3 Feather #5477 | 648 |
| Nordic PPK2 (**skip if borrowed**) | 2,104 |
| 6 × STEMMA QT cables | 105 |
| Breadboards + jumpers | 250 |
| 2 × USB-C data cables | 180 |
| **Subtotal (required)** | **3,287** (1,183 without PPK2) |
| Optional logic analyzer | 250 |

## 2. Phase A consumed electronics

| Item | Goods MXN |
|---|---:|
| 4 × e-paper modules #12955 | 739 |
| BMI270 breakout | 342 |
| ICS-43434 breakout | 166 |
| DRV2605L breakout | 147 |
| 2 × LRA | 119 |
| 1000 mAh cell (Cyberpuerta) | 177 |
| PTS526 ×10 + 12 mm keys | 90 |
| **Required subtotal** | **1,780** |
| Recommended: PDM mic breakout, ERM, 600–700 mAh cell, 8 pogo pins | 408 |
| **Required + recommended** | **2,188** |
| Optional: VEML7700, Sharp Memory LCD | 554 |

## 3. Phase A landed (one order per vendor)

| Variant | Goods | Shipping | Tax/duty (range) | Landed | +15 % contingency |
|---|---:|---:|---:|---:|---:|
| PPK2 **bought** | 5,475 | 498 | 1,349 (997–1,681) | 7,322 | **8,420** |
| PPK2 **borrowed** (+VEML7700 to reach DK free shipping) | 3,463 | 498 | 846 (675–1,007) | 4,807 | **5,528** |

**Phase A exact subtotal (goods, req + rec):** MXN 5,475 with PPK2 / MXN 3,371 without.
**Phase A practical budget:** **MXN 5,500** if the lab lends a power profiler; **MXN 8,500** if the team buys a PPK2.
The brief's MXN 3,000–4,500 is only reachable without the PPK2 *and* with near-zero contingency.

## 4. Phase B integrated electronics (first unit)

| Item | Goods MXN |
|---|---:|
| ESP32-S3-WROOM-1-N16R2 | 124 |
| 5 × raw e-paper (4 + spare) | 554 |
| 4 × FH12 FPC connectors | 178 |
| 4 × booster sets | 111 |
| BMI270 / IM69D130 / DRV2605L / LRA | 78 / 49 / 42 / 60 |
| BQ25180 / MAX17048 / TPS63802 / 2 × TPS22916 | 56 / 85 / 63 / 23 |
| 32 kHz XTAL, USB-C, 3 keys, ESD, passives | 49 / 15 / 9 / 19 / 74 |
| Battery 803040 | 177 |
| 4 dock pogo pins | 60 |
| **Per-unit components** | **1,825** |
| Main PCB ×5, dock PCBs ×5 | 555 |
| JLC PCBA (setup, stencil, ~15 extended feeders, joints; 2 boards) | 1,073 |
| DHL from JLC | 463 |
| **Batch / non-recurring** | **2,090** |
| **Phase B electronics goods** | **3,915** |
| Shipping (Waveshare) + duties (33.5 % China origin, ICs bought through JLC PCBA) | 498 + 1,376 |
| **Landed** | **5,789** |
| **+25 % contingency** | **7,236** |

## 5. Mechanical / enclosure / dock

| Item | Goods MXN |
|---|---:|
| Pocketability dummies (PLA + ballast) | 150 |
| SLA enclosure ×2 iterations (JLC3DP or local) | 925 |
| Cover windows (PMMA, laser cut) | 200 |
| N52 magnets (50 pcs) | 180 |
| Dock body, feet, screws | 250 |
| **Goods** | **1,705** |
| Duty on JLC3DP | 310 |
| **Landed / +25 %** | **2,015 / 2,519** |

## 6. Unknown / contingency
Phase A 15 %, Phase B 25 %. Covers: Waveshare shipping quote, Digi-Key courier brokerage, a cracked panel, a
wrong-polarity cell, extra FPC connectors, a PCB respin of the dock-pad board, marketplace price drift.
Not covered: a full main-PCB respin (+~MXN 3,000), lab equipment beyond the PPK2.

## 7. Summary

| Figure | MXN |
|---|---:|
| Phase A exact subtotal (goods, req + rec) | 5,475 (with PPK2) · 3,371 (without) |
| **Phase A practical budget** | **5,500 (PPK2 borrowed) · 8,500 (PPK2 bought)** |
| Phase B electronics (landed, first unit) | 5,789 |
| **First integrated prototype all-in** | **≈ 9,750** (landed 7,804 + 25 %) — **range 7,000–10,000** |
| Second unit from the same batch (marginal) | ≈ 3,000 |
| **Low-quantity repeat unit (10 pcs)** | **≈ 2,480** (range 2,100–2,900) |

## 8. Largest cost drivers (first integrated unit, landed)

| # | Driver | MXN (landed) | Share of 7,804 |
|---|---|---:|---:|
| 1 | PCB + PCBA + DHL batch fees (+33.5 %) | ≈ 2,790 | 36 % |
| 2 | Mechanical (SLA iterations, windows, dock, magnets) | ≈ 2,015 | 26 % |
| 3 | **Displays** (5 panels + Waveshare shipping + connectors + boosters, +33.5 %) | ≈ 1,620 | 21 % |
| 4 | Power subsystem (charger, gauge, buck-boost, switches, cell) | ≈ 480 | 6 % |
| 5 | MCU module | ≈ 165 | 2 % |

Of the **per-unit component BOM** (MXN 1,825): **displays 40 % (> 35 % flag)**, power + cell 22 %, MCU 7 %, haptics 6 %, IMU 4 %.
**Four displays dominate the recurring BOM; batch fees dominate the first unit.**

## 9. Cost sensitivity (top 5)

| Driver | Absolute (MXN) | % of per-unit BOM | Cheaper realistic alternative | Saving | UX / performance penalty |
|---|---:|---:|---|---:|---|
| Displays | 732 (per unit) | 40 % | JLC-stocked FPC connectors, no spare, Good Display direct at qty 10 | ≈ 260 | none |
| | | | 2 e-paper faces + 2 printed static labels | ≈ 370 | **severe**: 2 faces can't show status; breaks the concept |
| MCU | 124 | 7 % | ESP32-C3-MINI-1 | ≈ 70 | no PSRAM, no PDM-RX, single core → audio buffering/Opus at risk |
| Power subsystem | 404 | 22 % | LDO instead of TPS63802; ADC SoC instead of MAX17048 | ≈ 150 | −10–15 % usable capacity, brown-out risk on Wi-Fi bursts; SoC ±10–20 % |
| Haptics | 102 | 6 % | ERM + MOSFET | ≈ 75 | buzzy, slow (50–100 ms), "toy" feel — contradicts product goal |
| PCB / assembly | 2,090 (batch) | — | hand assembly at the university (stencil + hot plate), BQ25185 instead of BGA charger | ≈ 1,400 | risk on LGA IMU/mic + BGA; team time; rework |
