# Internal packaging concept (rev A, 55 × 55 × 45)

Status: concept for review — **not CAD**. Numbers from `tools/cube_model.py`.

## 1. Section along the rotation axis

```text
 z (mm)  face A (user face)                                         ← outer surface
  0.0  ┌─────────────────────────────────────────────────────┐
       │ cap 1.2: PTT key window (Ø18, recessed 1 mm inside   │   guard ring), AUX key, mic port Ø0.9 + mesh,
       │ light pipe (LED), 4 × M1.6 screws, hides USB-C+BOOT │
  1.2  │ PTS526 keys (1.5)          USB-C (service)          │
  2.7  ╞═════ main PCB 44 × 44 × 1.0 (4-layer) ═════════════╡  ← top: keys, mic (port through PCB), LED, USB-C
  3.7  │ WROOM-1 (3.1) ⟶ antenna edge faces one display face  │  ← bottom: module, BQ25180, TPS63802, MAX17048,
       │ BMI270, DRV2605L, 4 × FH12 FPC connectors on edges   │     booster ×4, load switches, 32 kHz XTAL
  7.3  ├───── panel-free antenna band ends at z ≈ 8 ─────────┤
       │                                                     │
       │   ┌──────── LiPo 803040 (8 + swell) ──────┐ ┌LRA┐   │  ← battery in foam cradle, LRA Ø10 bonded to a
       │   │ 30 × 40 footprint                     │ │   │   │     rigid rib next to the 30 mm side
       │   └───────────────────────────────────────┘ └───┘   │
       │      display panels span z ≈ 8 → 40 on all 4 sides  │
 41.7  ├──── dock-pad PCB 0.8 (rings) ← wires/flex to main ──┤
 42.5  │ face B wall 2.5 with 4 magnet pockets (Ø6.2 × 2.1)   │
 45.0  └─────────────────────────────────────────────────────┘  face B (dock face)
```

## 2. Cross-section (perpendicular to the axis)

```text
            display face N (WORK)
     ╭───────────────────────────────╮
     │ ▒▒▒▒▒▒▒ panel 37.3 ▒▒▒▒▒▒▒▒▒ │   ▒ = panel + window + backer (3.85 deep)
   ▒ │                               │ ▒
   ▒ │   core 47.3 × 47.3            │ ▒   main PCB 44 × 44 (corners chamfered
 W ▒ │   battery 30 × 40 + LRA       │ ▒ E  around display ribs)
   ▒ │                               │ ▒
     │ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ │
     ╰───────────────────────────────╯
            display face S
   corners: 6 mm radius; each panel end sits ≈ 8.8 mm from the outer edge (2.8 mm beyond the radius).
   Option P1 (modelled): the panel's 37.32 mm side runs around the axis, so the FPC tail exits toward a corner,
   folds behind the panel and runs along the inside of the face to the main PCB at face A.
```

### Panel orientation options (decide in TASK-003 with a real panel)
| | P1 — 37.32 mm around the axis (modelled) | P2 — 37.32 mm along the axis |
|---|---|---|
| FPC path | exits at a corner, folds, runs ~20–30 mm to face A → may need an FPC extension | exits toward face A, folds straight onto the PCB edge connector (shortest) |
| Axis length needed | ≥ 36.4 mm (+ antenna band → 42.1) | ≥ 37.32 + 2 × 1.8 + 1 ≈ 42 mm; the face-A band is occupied by the panel bond area |
| Antenna | 8 mm panel-free band at face A works | band not available → antenna toward a corner gap or flex antenna |
| Active-area position | offset toward face B by the band | offset toward face B by the bond area |

## 3. Placement rules
- **Antenna:** WROOM-1 antenna end toward the middle of one display face, inside the face-A band (z < 8 mm), ≥ 15 mm
  from the battery pouch and magnets. Ground-plane cut-out per Espressif keep-out drawing.
- **IMU:** near PCB centre, Z ∥ rotation axis, ≥ 15 mm from LRA.
- **Mic:** bottom-port under the cap port, ≥ 10 mm from the PTT key centre, gasket to cap.
- **FPC connectors:** one per PCB edge (N/E/S/W) so each panel tail folds straight back — no crossing.
- **Charger + buck-boost:** opposite corner from the cell's thickest side; thermal vias to inner copper.
- **Dock-pad PCB:** connected by 2 wires (VBUS, GND) — or a 4-wire flex if D+/D− are ever used.

## 4. Assembly sequence (draft)
1. Bond 4 windows into the shell; bond panels to windows (OCA or perimeter PSA); route each FPC tail toward face A (P1: via a fold at the corner).
2. Insert dock-pad PCB + magnets into face B; route 2 wires to face-A side.
3. Battery in foam cradle; LRA bonded to rib.
4. Lower main PCB from face A; latch 4 FPCs into ZIFs (connectors reachable from the face-A opening — design requirement).
5. Connect battery, dock wires; close face-A cap (4 × M1.6). Service USB-C and BOOT reachable with the cap off.

## 5. Open packaging questions
- Exact FPC tail length of the raw panel vs. the needed fold (measure on a real panel — TASK-002).
- Whether the 8 mm antenna band can shrink (RF test).
- Window material: PMMA 0.8 vs chemically-strengthened glass 0.55.
