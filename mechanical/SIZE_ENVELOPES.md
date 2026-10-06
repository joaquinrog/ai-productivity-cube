# Size envelopes

Generated with `tools/cube_model.py` (2026-10-05). Notation **W × W × H**: W × W = square interaction faces
(A, B) at the ends of the rotation axis; H = axis length = pocket thickness when the cube lies flat.
Display faces are W × H. Edge radius 6 mm, wall 1.8 mm, display stack 3.85 mm (see `research/mechanical_feasibility.md`).

## 1. Quantitative comparison

| Envelope | Outer vol. | Free core (square) | Axial space | Panel fits width? | Panel fits height (PCB ant. / flex ant.) | Largest cell that fits | Mass w/ 803040 |
|---|---:|---:|---:|---|---|---|---:|
| 50 × 50 × 50 | 121 cm³ | 42.3 mm | 39.4 mm | **barely** (0.7 mm) | ✅ / ✅ | 103040 1200 mAh (tight) | ~84 g |
| 52 × 52 × 38 | 99 cm³ | 44.3 mm | 27.4 mm | ✅ | ❌ / ✅ | 103040 in plan; 603040/803040 realistic | ~80 g |
| 55 × 55 × 42 | 123 cm³ | 47.3 mm | 31.4 mm | ✅ | ⚠️ needs 42.1 / ✅ | 103040 | ~84 g |
| **55 × 55 × 45** | 132 cm³ | 47.3 mm | 34.4 mm | ✅ | ✅ / ✅ | 103040 | **~86 g** |
| 58 × 58 × 45 | 147 cm³ | 50.3 mm | 34.4 mm | ✅ | ✅ / ✅ | 103040 | ~88 g |
| 60 × 60 × 50 | 175 cm³ | 52.3 mm | 39.4 mm | ✅ | ✅ / ✅ | 103040 / 503450 | ~93 g |

Mass realistic range: model −5 % / +20 %. Volumes include 6 mm edge rounding.

## 2. Qualitative evaluation (1 = poor, 5 = excellent)

| Envelope | Battery fit | Display fit | PCB fit | Antenna | FFC routing | Hand comfort | Pants-pocket | Desk presence | Manufacturability |
|---|---|---|---|---|---|---|---|---|---|
| 50 × 50 × 50 | 4 | **2** | 3 | 4 | 3 | 4 | **2** (50 mm thick) | 4 | 3 |
| 52 × 52 × 38 | 3 | 4 | 3 | **2** (flex ant. needed) | **2** (27 mm axial) | 4 | **4** | 3 | 2 |
| 55 × 55 × 42 | 5 | 5 | 4 | 3 | 3 | 4 | 3 | 4 | 4 |
| **55 × 55 × 45** | 5 | 5 | 5 | **4** | 4 | 4 | 3 | 4 | **5** |
| 58 × 58 × 45 | 5 | 5 | 5 | 4 | 4 | 3 | 2 | 5 | 5 |
| 60 × 60 × 50 | 5 | 5 | 5 | 5 | 5 | 3 | **1** | 5 | 5 |

## 3. Squashed cube vs. perfect cube (55 × 55 × 42 vs 50 × 50 × 50)
Same volume (123 vs 121 cm³) and mass, **8 mm thinner in the pocket (−16 %)**, +5 mm of free core, 5 mm more panel
margin. The perfect cube's extra height is unused (panel needs only ~36 mm). Costs: looks less like a cube; display
faces become 55 × 42 landscape (fine — panel active area is a 27.6 mm square). **The flattened body is better.**

## 4. Recommendation

| | Envelope | Condition |
|---|---|---|
| **Ideal target** | 52 × 52 × 38 | only if mockup test shows a clear pocket win **and** flex-antenna RF test passes; ~700 mAh cell |
| **Realistic target** | 55 × 55 × 42–45 → **rev A = 55 × 55 × 45** | PCB-antenna module; 42 after RF test |
| **Maximum acceptable** | 58 × 58 × 45 | beyond this, users leave it on the desk |
