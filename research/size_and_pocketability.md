# Research — Size and pocketability

Checked 2026-10-05. Envelope table: `mechanical/SIZE_ENVELOPES.md`. Physical test: `mechanical/POCKETABILITY_TEST_PLAN.md`.

## 1. What "pocketable" means here
Not "fits in a pocket" but **"I forget it's there for 1–3 hours and can pull it out one-handed"**. Factors:

| Factor | Driver | Target |
|---|---|---|
| Thickness against the thigh | smallest dimension | ≤ 45 mm acceptable, ≤ 40 good, ≤ 25 excellent |
| Entering / leaving the pocket | largest face | ≤ 60 mm (front-pocket openings are ~120–150 mm wide) |
| Pressure points | edge radius | ≥ 5–6 mm edge radius, no sharp corners |
| Mass | total grams | ≤ 100 g (phone-like 150–200 g is noticeable in a second pocket) |
| Accidental presses | key exposure | recessed key inside a guard ring + firmware gating |
| Display protection | window recess | windows 0.2–0.3 mm below the shell surface |
| Desk ↔ pocket handling | grip | 50–58 mm faces fit a palm and a 3-finger pinch |

## 2. Reference objects (data)

| Object | Dimensions (mm) | Volume | Mass | Thickness in pocket |
|---|---|---|---|---|
| AirPods Pro 2 case | 60.6 × 45.2 × 21.7 | 59 cm³ | 50.8 g | 21.7 |
| Flipper Zero | 100 × 40 × 25 | 100 cm³ | 102 g | 25 |
| Rabbit r1 | 78 × 78 × 13 | 79 cm³ | 115 g | 13 |
| Rubik's cube 3×3 | 57 × 57 × 57 | 185 cm³ | ~75 g | 57 |
| **Cube 55 × 55 × 42** | | **123 cm³** | **~84 g** | **42** |
| **Cube 55 × 55 × 45** | | **132 cm³** | **~86 g** | **45** |

Honest position: **this device is Rubik's-cube class in the pocket, not AirPods class.** A flattened body takes ~30 %
of the volume and ~12 mm of thickness off a Rubik's cube, which is a real comfort gain, but it will still be felt.

## 3. Is 55 × 55 × 40–45 better than 50 × 50 × 50? — Yes

| | 50 × 50 × 50 | 55 × 55 × 42 | Δ |
|---|---|---|---|
| Outer volume (6 mm edges) | 121 cm³ | 123 cm³ | ≈ same |
| Pocket thickness | 50 mm | 42 mm | **−16 %** |
| Free core square | 42.3 mm | 47.3 mm | +5 mm (battery + LRA side-by-side easily) |
| Panel width margin past radius | 0.7 mm | 5.7 mm | much easier windows/bezels |
| Axial space | 39.4 mm (wasted, panel is 31.8) | 31.4 mm | 50 cube's extra height buys nothing |
| Display face | 50 × 50 square | 55 × 42 landscape | panel is square (27.6 active) → fine in both |
| Mass (model) | ~84 g | ~84 g | same |
| Looks like a cube? | yes | "a squashed cube / puck" | the main cost |
| Dock | any face symmetric | axis faces are the big flat faces → natural side-dock | flattened is *better* for D-015 |

The perfect cube spends its extra height on nothing (the panel only needs ~36 mm), while the flattened body
uses the same volume to be thinner and give the internals more room.

## 4. Recommendation

| | Size | Why |
|---|---|---|
| **Ideal target** | **52 × 52 × 38 mm** | ~99 cm³ (−20 %), 38 mm thick. Needs WROOM-1U + flex antenna on face A, a 603040 (~700 mAh) cell, and tight FPC routing. Pursue only if the mockup test shows a clear comfort win over 42–45. |
| **Realistic target** | **55 × 55 × 42–45 mm** (rev A at **45**) | All parts fit with margin; PCB-antenna module works at 45 (42 needs flex antenna or a passing RF test). |
| **Maximum acceptable** | **58 × 58 × 45 mm** | ~147 cm³; beyond this (60 × 60 × 50 = 175 cm³) it is Rubik's-cube bulk and users will leave it on the desk. |

Final call between 38 / 42 / 45 mm thickness is made **physically** with the mockup test (TASK-002) before the
enclosure CAD is frozen.
