# OPEN QUESTIONS

Format: question · why it matters · how/when it gets answered.

## Need a human decision (TASK-001 review)
1. **Accept e-paper (D-003) and the "cube is readable while asleep" UX** — including no readability in the dark? · defines the product look · reviewer.
2. **Accept the flattened body (D-013)** and rev A at 55 × 55 × 45? · enclosure, dock, branding · reviewer, then mockup test.
3. **Buy a PPK2 or borrow one?** · MXN ~2,600 landed swing in Phase A · reviewer / lab.
4. **Phone platform priority: Android first or iOS first?** · iOS background BLE is the top risk · reviewer.
5. **Budget envelope for Phase B (~MXN 9,750 first unit)** vs the brief's ~MXN 4,000 target · reviewer.

## Engineering unknowns (answered by tests)
| # | Question | Why | Answer in |
|---|---|---|---|
| E1 | Real BLE keep-alive current with the actual phone app (0.25–2 mA modelled) | dominates battery life | Test 7 |
| E2 | iOS: does a backgrounded app receive `face_changed` within 2 s, all day? | core UX | Test 7 |
| E3 | E-paper ghosting rate and full-refresh cadence for this panel | UX quality | Test 3 |
| E4 | Partial refresh at < 10 °C | outdoor use | Test 3 (fridge test) |
| E5 | BMI270 any-motion + firmware face classification robustness | core UX | Test 4 |
| E6 | Does LRA beat ERM in blind A/B on a 90 g body? | D-007 | Test 6 |
| E7 | Charger temperature rise at 400 mA in a closed shell | safety/comfort | Test 8 |
| E8 | MAX17048 SoC error with this cell | UX | Test 9 |
| E9 | Magnet hold vs pogo force through the shell skins | dock UX | Test 10 |
| E10 | Can the antenna band shrink below 8 mm (→ 42 mm body)? | size | Phase B RF test |
| E11 | Raw panel FPC tail length and fold radius | packaging | TASK-002 (inspect a raw panel) |
| E12 | Accidental PTT presses at 38/42/45 mm in real pockets | size + privacy | mockup study |
| E13 | Is the ALS needed for pocket detection? | D-009 | mockup + Test 11 |
| E14 | IM69D130 current & ESP32-S3 PDM-RX quality vs I2S | D-008 | Test 5 (PDM breakout) |
| E15 | Exact landed costs: Waveshare shipping, DK brokerage, JLC quote | budget | at order time |

## Product questions (later)
- Default context set and user configuration UX (phone app).
- What happens on the down-facing panel (blank? mirror? "flip me")?
- Should the up-face or the user-facing side face be the "active" display when docked? (on a side-wall dock the up face is still visible from above at desk height)
