# Research — Haptics

Checked 2026-10-05. Decision: D-007.

## 1. UX targets
Distinct, short, "consumer electronics" patterns for: **confirm**, **fail/error**, **pending
confirmation**, **notification**, **mode change** (face rotation). Must be felt in hand and on a desk,
and ideally through a pocket for notifications.

## 2. ERM vs LRA

| | ERM (eccentric rotating mass) | LRA (linear resonant actuator) |
|---|---|---|
| Feel | buzzy, rumbly | crisp "tap"/"click", cleaner |
| Rise / fall | 50–100 ms spin-up, coasts | VG1030001XH: rise ≤ 50 ms, fall ≤ 100 ms (DS) — shortened by driver overdrive/brake |
| Drive | DC + MOSFET | AC at resonance (210 Hz) → needs a driver |
| Efficiency | lower | higher for the same perceived strength |
| Life | brushes wear | no brushes |
| Example | Adafruit #1201 (USD 1.95) | **Vybronics VG1030001XH** (USD 3.22) |

## 3. Is a dedicated driver (DRV2605L) justified? — Yes
- LRA needs AC drive at resonance; DRV2605L does **closed-loop auto-resonance tracking**, overdrive
  and active braking — exactly what makes Apple/Google haptics feel crisp.
- 123 licensed **ROM effects** (strong click, double click, alert, ramp…) → confirm/error/pending/
  notify/mode-change patterns without writing waveforms.
- I2C control (shared bus), EN pin for shutdown (4 µA DS), 0.5 mA Iq when enabled.
- Cost USD 2.28 (4,661 pcs). Breakout Adafruit #2305 for Phase A.
- Alternative: Renesas DA7280 (newer, also LRA-capable). DRV2605L chosen for library support.

## 4. Actuator choice
**VG1030001XH**: Ø10 mm coin, 210 ± 10 Hz, 2.0 Vrms rated, **≥ 2.0 G peak on a ~100 g jig** (the cube
is ~85–95 g, so the rating transfers almost directly), 135 mArms max, 17 Ω, wire leads, 465 pcs.
- Coin (Z-axis) LRAs vibrate perpendicular to their face: mount it flat against the **battery-side
  of face B** or a display-face rib so the enclosure couples, not the foam.
- Alternate: VG1040003D (Ø10, 2 G, 170 Hz, pressure contacts — needs spring-contact pads).

## 5. Pattern draft (to validate in Test 6)

| Event | DRV2605L effect idea | Duration |
|---|---|---|
| Confirm (✓ saved) | Strong Click 100 % (#1) | ~30 ms |
| Error | Double Click 100 % (#10) + 120 ms + Buzz 40 % | ~300 ms |
| Pending (agent working) | soft pulse every 1.5 s (Pulsing Sharp, low) | until result |
| Notification | Alert 750 ms (#15) or Transition Ramp | 0.5–0.75 s |
| Mode change (face rotation) | Sharp Tick 1 (#24) | ~10 ms |

## 6. Phase A experiment
Blind A/B with 5 users: same patterns on ERM (#1201 via DRV2605L ERM mode) vs LRA, cube-mass
dummy (~90 g) — score crispness / annoyance / distinguishability. Lock D-007 only after this.
