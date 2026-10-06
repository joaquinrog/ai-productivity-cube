# Pocketability mockup test plan

Goal: decide the body thickness (38 / 42 / 45 mm) **physically**, before enclosure CAD is frozen. Cost: ~MXN 150 (BOM M1).

## 1. Dummies
Print solid-feel dummies (PLA, 3 perimeters, 20 % infill, 6 mm edge radius) and ballast each to the modelled mass
with steel washers/fishing weights glued in a centre pocket:

| ID | Size (mm) | Target mass | Notes |
|---|---|---|---|
| D1 | 52 × 52 × 38 | 80 g | ideal target |
| D2 | 55 × 55 × 42 | 84 g | realistic thin |
| D3 | 55 × 55 × 45 | 86 g | rev A |
| D4 (control) | 50 × 50 × 50 | 84 g | perfect cube |
| D5 (optional) | 58 × 58 × 45 | 88 g | max acceptable |

Each dummy gets: a recessed Ø18 mm "PTT" key area with a 1 mm guard ring on face A, a 12 mm tact switch glued under
it (wired to a coin-cell LED or simply inspected for presses — see §3), engraved face labels, and a printed dock
contact pattern on face B.

## 2. Protocol (≥ 5 participants, mixed pocket types incl. women's jeans)
For each dummy, randomized order, 2 h carry during normal activity (walk, sit, drive/transport, climb stairs):
1. Pants front pocket 2 h; jacket pocket 30 min.
2. Every 30 min: rate comfort; take out one-handed and put back (time it).
3. Desk: rotate through 4 faces 10 times one-handed; simulate PTT hold 3 s; simulate docking against a printed wall.
4. Record accidental key presses (LED counter or a mark-paint check on the key cap).

## 3. Accidental-press detector (cheap)
- **Zero-electronics version:** a dab of lipstick/whiteboard ink on the key's travel stop that transfers to a paper
  disc under it when the key bottoms out; inspect and replace the disc after each carry.
- **Counting version (if time):** the second Feather (R1) + the 600–700 mAh test cell (A9) inside one dummy counts presses
  ≥ 150 ms (the real PTT threshold) and logs timestamps.

## 4. Scorecard (per participant, per dummy)

| Criterion | Scale | Weight |
|---|---|---|
| Comfort sitting (pants) | 1–5 | 3 |
| Comfort walking (pants) | 1–5 | 2 |
| Visible bulge / self-consciousness | 1–5 | 2 |
| One-handed pull-out ease | 1–5 | 1 |
| Grip & rotate on desk | 1–5 | 2 |
| PTT hold comfort | 1–5 | 1 |
| Desk presence ("looks like a product") | 1–5 | 1 |
| Accidental presses during 2 h | count (0 = 5 pts, 1 = 3, ≥ 2 = 0) | 3 |
| "Would carry it daily?" | yes/no | gate |

**Decision rule:** pick the thickest envelope whose weighted score is within 10 % of the best *and* where ≥ 4/5 say
"would carry daily" (thicker = more engineering margin). If D1 wins by > 10 %, open a ticket to evaluate WROOM-1U +
flex antenna and a 700 mAh cell.
