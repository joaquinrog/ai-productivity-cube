# Research — Mechanical feasibility

Checked 2026-10-05. Numbers come from `tools/cube_model.py` (edit assumptions there, not here).
Packaging concept: `mechanical/INTERNAL_PACKAGING.md`. Size comparison: `mechanical/SIZE_ENVELOPES.md`.

## 1. Component dimensions used

| Item | Dimensions (mm) | Source |
|---|---|---|
| E-paper raw panel (each of 4) | 31.8 × 37.32 × 1.05; active 27.6 × 27.6 | Waveshare #12561 / GD GDEY0154D67 |
| Panel FPC tail | 24-pin, 0.5 mm pitch, ~15–20 mm, folds behind panel | GD reference (verify on sample) |
| FPC connector FH12-24S | ≈ 15.4 × 4.9 × 2.0 (R/A) | Hirose (verify drawing) |
| ESP32-S3-WROOM-1 | 18 × 25.5 × 3.1 + antenna keep-out | Espressif DS v1.8 |
| ESP32-S3-MINI-1 (alt.) | 15.4 × 20.5 × 2.4 | Espressif DS |
| BMI270 | 2.5 × 3.0 × 0.8 | Bosch DS |
| IM69D130 mic | 4 × 3 × 1.2 | Infineon (verify) |
| LRA VG1030001XH | Ø10 × ~3 (from part code) | Vybronics |
| Battery 803040 | 8 × 30 × 40 (+10 % swell) | listings |
| PTS526 key | 5.2 × 5.2 × 1.5 | C&K |
| USB-C USB4105 | ≈ 8.9 × 7.4 × 3.2 | GCT (verify) |
| Pogo target pads | flush ENIG on 0.8 mm PCB | — |
| Magnets | Ø6 × 2 (×4) | N52 discs |
| Shell wall | 1.8 (SLA/MJF) | assumption |
| Cover window | 0.8 PMMA | assumption |

## 2. Stack-ups

### Display face (outside → in) = 3.85 mm
window 0.8 + panel 1.05 + adhesive 0.2 + backer rib 0.8 + FPC fold 1.0.
→ free core square = W − 7.7 mm (55 body → **47.3 mm**; 50 body → 42.3 mm).

### Rotation axis (face A → face B)
| Layer | mm |
|---|---|
| Face-A cap (keys, mic port, LED pipe) | 1.2 |
| PTS526 key height | 1.5 |
| Main PCB, 4-layer, 1.0 mm | 1.0 |
| Tallest bottom-side part (WROOM-1) | 3.1 |
| clearance | 0.5 |
| **Face-A stack** | **7.3** |
| … battery (8 + 10 % + foam) / LRA beside it … | 9.3 |
| Face-B wall with magnet pockets | 2.5 |
| Dock-pad PCB | 0.8 |
| **Face-B stack** | **3.3** |

### Panel vs. axis length
- Panel 31.8 mm must sit between the two end walls: **H ≥ 36.4 mm**.
- With the PCB-antenna module, the antenna sits at z ≈ 3–5 mm from face A; keeping an ~8 mm panel-free
  band there requires **H ≥ 42.1 mm**. (8 mm band = assumption; verify RSSI in printed shell.)

### Panel vs. face width
Panel 37.32 mm must clear the 6 mm edge radius on both sides: **W ≥ 49.3 mm**.
**A 50 mm cube fits the 1.54″ panel with 0.7 mm to spare** — feasible but tight; 52–55 mm is comfortable.

## 3. Feasibility by element

| Element | 55 × 55 × 45 (rev A) | Comment |
|---|---|---|
| 4 panels | ✅ | 37.32 in a 55 face; 2.8 mm margin each side beyond the 6 mm edge radius (5.7 mm total) |
| Main PCB ≈ 44 × 44 | ✅ | fits the 47.3 core; corners chamfered for display ribs |
| WROOM-1 + keep-out | ✅ | antenna edge toward one display face, in the face-A band |
| Battery 803040 | ✅ | 40 + 1.5 ≤ 47.3; LRA (10 mm) beside the 30 mm side |
| FPC routing | ✅ (needs proof) | each panel tail folds behind its panel and reaches a connector on the PCB edge; 4 connectors × 15.4 mm on a 44 mm board edge set — **biggest layout risk** |
| Buttons on face A | ✅ | keys on PCB top side under the cap |
| Mic port | ✅ | through-PCB port + gasket |
| Dock pads + magnets | ✅ | separate 0.8 mm PCB, flex/wire to main PCB |
| Service USB-C | ✅ | on PCB top side, behind the removable face-A cap |
| Assembly | ⚠️ | panels glued into windows first, then core (PCB + battery) slides in from face A; 4 FPCs latched blind → needs a jig or connectors reachable from face A |

## 4. Realistic total mass

| Part | g |
|---|---|
| Shell (SLA, 1.8 mm walls, 55 × 55 × 45) | ~25 |
| Internal ribs / frames / bosses (25 % of shell) | ~6 |
| 4 panels | 12 |
| 4 windows | 3.6 |
| Main PCB + module + parts | 8.5 |
| Dock-pad PCB | 1.5 |
| LRA | 1.5 |
| Magnets | 1.7 |
| Key caps, light pipe | 2 |
| Screws, FPCs, foam, tape | 4 |
| Battery 803040 | 20 |
| **Total (model)** | **≈ 86 g** |

**Realistic range: 80–105 g** (prototype SLA, thicker walls, glue and screws push it up; a 700 mAh cell takes ~6 g off).
For reference: AirPods Pro 2 case 50.8 g, official Rubik's cube ~75 g, Flipper Zero 102 g, Rabbit r1 115 g.

## 5. Conclusion
The architecture is mechanically feasible at **55 × 55 × 45** with margin, at **55 × 55 × 42** only with a
flex antenna (or after an RF test shows the 8 mm band can shrink), and at **50 × 50 × 50** with almost no margin
on the panel width. The binding constraints are **panel outline + FPC folding + antenna keep-out**, not the battery.
