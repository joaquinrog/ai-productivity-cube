# CURRENT STATE

_Last updated: 2026-10-05 (end of TASK-001). Fastest way in for a new engineer or agent._

## Current architecture (proposed, awaiting review)
Phone-as-gateway BLE device. **ESP32-S3-WROOM-1-N16R2** + 32.768 kHz crystal · **4 × 1.54″ B/W e-paper (SSD1681)** on one
shared SPI bus with a gated rail · **BMI270** (face detection in firmware) · **IM69D130** PDM mic (PTT only, gated) ·
**DRV2605L + 10 mm LRA** · **BQ25180** power-path charger → **TPS63802** 3.3 V buck-boost · **MAX17048** gauge · 1S LiPo
~1000 mAh (803040) · face A = keys/mic/LED/service USB-C under a cap · face B = concentric dock rings + 4 magnets ·
side-wall magnetic dock with Hall-gated VBUS. Diagrams: `electronics/block_diagram.md`.

## Accepted decisions
D-001 phased prototyping · D-018 push-to-talk only · D-019 phone gateway / cloud intelligence / no LLM on MCU.

## Provisional decisions (Proposed in TASK-001)
D-002 MCU/module · D-003 e-paper (replaces SSD1351 OLED) · D-004 monochrome · D-005 shared SPI + gated rail · D-006 BMI270 ·
D-007 DRV2605L + LRA (pending A/B) · D-008 single mic, I2S bench / PDM Phase B · D-009 no ALS (footprint) · D-010 power
architecture · D-011 32 kHz XTAL · D-012 battery · D-013 geometry · D-014 face allocation · D-015 dock · D-016 USB/debug ·
D-017 sourcing.

## Current recommended dimensions
- **Rev A: 55 × 55 × 45 mm** (rotation axis = 45 mm), ~86 g (80–105 g realistic).
- Realistic band 55 × 55 × 42–45 · ideal 52 × 52 × 38 (needs flex antenna, ~700 mAh) · max 58 × 58 × 45.
- Final thickness decided by the physical mockup study (TASK-002).

## Current BOM estimate (MXN, price checked 2026-10-05, FX 18.50)
| | Goods | Landed | With contingency |
|---|---:|---:|---:|
| Phase A (PPK2 borrowed) | 3,463 | 4,807 | **5,528** |
| Phase A (PPK2 bought) | 5,475 | 7,322 | **8,420** |
| Phase B electronics, first unit | 3,915 | 5,789 | 7,236 |
| Mechanical | 1,705 | 2,015 | 2,519 |
| **First integrated prototype all-in** | | 7,804 | **≈ 9,750** (range 7,000–10,000) |
| Repeat unit @ 10 pcs | | | ≈ 2,480 |

Displays = 40 % of per-unit parts (flagged > 35 %, accepted). Batch PCB/PCBA fees = 36 % of the first unit.

## Biggest risks
1. **iOS background BLE** behaviour and the phone-dictated BLE keep-alive current (R-09, R-10).
2. **Raw e-paper integration**: 4 boosters + 4 FPC tails into one 44 mm board, glass durability in a pocket (R-05, R-06, R-22).
3. **Pocket thickness comfort + accidental PTT** at 42–45 mm (R-20, R-21, R-26).
Full register: `electronics/risks.md`.

## Current task
TASK-001 — **complete, awaiting human review** (`tasks/TASK-001-electronics-size-cost-and-shopping-cart.md`).

## Next milestone
TASK-002 — Phase A executed: parts ordered, Tests 1–11 passed or superseded by ADRs, pocketability mockup study done,
measured power numbers replace the model. Then Phase B schematic.
