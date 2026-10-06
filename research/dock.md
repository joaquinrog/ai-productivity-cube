# Research — Dock

Checked 2026-10-05. Decisions: D-014, D-015, D-016.

## 1. Constraints
- The cube rotates about the axis through the two interaction faces (A and B).
- The user must be able to switch `WORK → STUDY → AVAILABLE → DND` **while docked**, by rotating the cube.
- The dock must charge, detect docking, and keep the cube from being knocked out.
- Display faces cannot carry contacts (they are windows).
- V1 simplicity: no Qi unless compelling.

## 2. Options evaluated

| Option | Contacts on | Works in all 4 rotations? | Conflicts | Verdict |
|---|---|---|---|---|
| Pogo surface under the cube | the down display face | needs contacts on every display face | breaks display faces | ✗ |
| Rear support / easel | a display face | same | same | ✗ |
| Recessed contacts on one corner edge | edge | only 1 of 4 rotations | — | ✗ |
| Magnetic rail (cube slides along) | axis face | yes | complex, scraping | ✗ |
| Axle cradle ("rotisserie", cube spins in place) | both axis faces | **yes, without lifting** | two-sided clamp, cube hard to remove, button face covered | V2 idea |
| **Side-wall dock, contacts on axis face B** ✅ | face B (axis) | **yes** (concentric rings) | none with buttons (face A) | **V1** |
| Qi wireless | any face | needs coil behind a display face or axis face | ~30–40 mm coil + ferrite + RX IC, heat, cost | ✗ for V1 |

## 3. Recommended geometry

```text
            side view (docked)                       face B (dock face) — 55 x 55
      ┌────────── wall ──────────┐                  ┌───────────────────────────┐
      │ pogo pins ●●  magnets ▣  │                  │ ▣                       ▣ │  ▣ = N52 Ø6x2 magnet (x4,
      │                          │                  │        ┌─────────┐        │      all same polarity →
 face A (PTT, mic, LED) ← cube → face B             │        │ ◯ GND   │        │      90° detents)
      │      [ display UP ]      │                  │        │ ◯ (D+)  │        │
      └──────── dock floor ──────┘                  │        │ ◯ (D−)  │        │  rings: ENIG on a 0.8 mm
         (cube rests on the DOWN display face;      │        │ ● VBUS  │        │  PCB, flush with skin
          floor has a felt pad + 1 mm locating lip) │        └─────────┘        │
                                                    │ ▣                       ▣ │
                                                    └───────────────────────────┘
```

- Contact pattern: centre pad **VBUS** (Ø3 mm), outer ring **GND** (widest, outermost). V1 populates only
  these two; two inner rings (D+/D−) are **reserved** and left unconnected until dock rev 2.
- Pogo pins (Mill-Max 0906-0-15-20-76-14-11-0, 2 A, 1 M cycles) live **in the dock** on a radial line at
  the ring radii; the cube has flat pads only (no springs to wear or snag in a pocket).
- Any 90° rotation keeps each pin on its ring. The user rotates by lifting slightly, turning, re-seating —
  magnets snap it to the next detent.
- Face A faces away from the wall → PTT, mic and LED remain usable when docked.

## 4. Scrape / short-circuit problem and the fix
Lowering the cube into the dock drags the pins across face B, so the VBUS pin momentarily touches the GND
ring. Fix in the dock, not the cube:
- **Dock VBUS is off until the cube is seated**: a Hall switch (e.g. TI DRV5032) in the wall senses the cube's
  magnets → RC debounce ~300 ms → current-limited load switch (e.g. TPS2553, ~0.5–1 A limit, auto-retry) → VBUS pin.
- Benefits: no live 5 V on exposed dock pins when keys/coins land on the dock; tolerant of scraping.
- Cube side: BQ25180 IN is 25 V-tolerant and blocks reverse current; TVS on the VBUS pad.
- **Data rings are not connected to the ESP32 in V1**: a scraping VBUS pin could put 5 V on D+/D−, and the
  ESP32-S3 USB pins are not 5 V tolerant. Revisit with an analog switch (TS3USB221-class) gated by VBUS-good.

## 5. Dock detection (cube side)
VBUS pad → 100 k / 150 k divider → **GPIO1** (RTC, ADC1) wakes the MCU; BQ25180 /INT (GPIO7) confirms
power-good/charging state. No extra contact required.

## 6. Magnets
- 4 × N52 Ø6 × 2 mm in face-B corners (cube) + 4 opposite pole in the dock wall; ~0.5–1 mm plastic skin each side.
- Expected hold through ~1.5 mm total gap: a few hundred gf per pair (estimate — **measure in Phase A**) vs. 2–4
  pogo pins at ~50 gf each mid-stroke → comfortable margin.
- Keep magnets ≥ 15 mm from the antenna corner and ≥ 10 mm from the LRA; no magnetometer in the design (D-006).
- Side effects: attracts steel debris in pockets; avoid placing next to magstripe cards (note in user guide).

## 7. Button / pogo / mic / magnet conflict check

| Pair | Same face? | Resolution |
|---|---|---|
| Buttons ↔ pogo pads | no (A vs B) | docking never presses a key |
| Mic ↔ dock | no | mic on face A stays open when docked |
| Magnets ↔ buttons | no | — |
| Magnets ↔ antenna | different end | antenna at face-A end of the main PCB |
| LED ↔ dock | no | LED on face A visible when docked |

## 7b. USB architecture (Option C, D-016)

| Option | Flash/debug | Recovery | Enclosure opening | Board complexity | Field use |
|---|---|---|---|---|---|
| A — USB-C power only | via pads only | pads | yes | low | charge anywhere |
| B — USB-C power + data | native USB-Serial/JTAG | good | yes (lint, water) | low | best |
| **C — dock charging + hidden service USB-C** ✅ | native USB behind face-A cap | Tag-Connect UART pads + BOOT | **none** | low | needs dock (or travel puck) |

Travel charging: a "dock puck" (dock wall electronics on a USB-C cable) can be printed later.

## 8. Phase A dock experiment
3D-print a dock wall + a face-B coupon (55 × 55 printed plate with a copper-tape or PCB ring target and 4 magnets);
8 Mill-Max pins. Measure: contact resistance over 200 docking cycles, alignment at each of the 4 rotations, magnet
hold force (luggage scale), and whether rotation-by-lift-and-reseat feels natural.
