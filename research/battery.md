# Research — Battery

Checked 2026-10-05. Decision: D-012.

## 1. Requirements (derived)

```text
Chemistry:                    Li-ion polymer (LiPo), 1S
Nominal voltage:              3.7 V
Maximum charged voltage:      4.20 V (BQ25180 VBATREG default 4.2 V)
Capacity:                     700–1000 mAh (baseline 1000 mAh for the 55 mm body)
Dimensions:                   footprint ≤ 30 × 40 mm, thickness ≤ 8 mm (≤ 10 mm with 45 mm body)
Mass:                         ≤ 22 g
Minimum discharge capability: ≥ 1 C continuous (≥ 1 A for 1000 mAh) — system peak ≈ 0.56 A
Protection:                   integrated PCM (over-charge, over-discharge ~3.0 V, short circuit)
Connector:                    2-wire JST-PH 2.0 (polarity must be verified against the Feather/PCB!)
Certification wish:           UN38.3 + MSDS available from seller (needed if ever shipped)
```

## 2. Geometry first, capacity second
The 55 mm body has a ~47 × 47 mm free core inside the four display stacks (`mechanical/SIZE_ENVELOPES.md`).
A cell must fit in plan **with a 10 mm LRA beside it**, and in thickness inside the ~31–34 mm axial space
(PCB + button stack take the rest).

| Cell family | Size (t × w × l) | Fits 52 core (44.3)? | Fits 55 core (47.3)? | Verdict |
|---|---|---|---|---|
| **803040** 1000 mAh | 8 × 30 × 40 | yes (tight) | **yes** | baseline |
| 603040 ~700 mAh | 6 × 30 × 40 | yes | yes | small-body fallback |
| 103040 1200 mAh | 10 × 30 × 40 | yes (axial OK only ≥ 42) | yes | optional upgrade |
| 503450 1000 mAh (UNIT) | 5 × 34 × 50 | **no** | **no** (50 > 47) | needs 58–60 body |
| Adafruit #258 1200 mAh | 5 × 34 × 62 | no | no | long-thin: wrong shape |
| Adafruit #1578 500 mAh | 4.75 × 29 × 36, 10.5 g | yes | yes | quality reference |

**The hypothesis "a ~30 × 35–40 × 8–10 mm cell is more useful than a long thin 1200 mAh cell" is
confirmed**: long-thin cells (≥ 50 mm) do not fit any body ≤ 55 mm because the display stacks eat
~8 mm of each cross-section dimension.

## 3. Real purchasable candidates (Mexico)

| Class | Candidate | Capacity | Size | Mass | PCM | Connector | Vendor / price | Status |
|---|---|---|---|---|---|---|---|---|
| 900–1100 | **Dataproducts DP-80304** (803040) | 1000 mAh | listing doesn't state; 803040 = 8 × 30 × 40 | ~20 g (typ. 803040) | listing doesn't state — **verify** | 2-wire | Cyberpuerta **MXN 177** + MXN 128 ship; 5 pcs | verified listing |
| 900–1100 | Mercado Libre "Batería LiPo 3.7 V 1000 mAh" (803040 class) | 1000 mAh | 40 × 30 × 7.8 typ. | ~20 g | usually | JST-PH 2.0 / 2.54 | **MXN 149–416** (search snippets, not opened) | estimate |
| 900–1100 | Akyga AKY0571 LP803040 (EU brand w/ datasheet) | 1000 mAh | 8 × 30 × 40 | 20 g | **yes, PCM** | JST 2.54, 150 mm leads | EU distributors; not found in MX | reference |
| 700–900 | 603040 generic (Mercado Libre / AliExpress) | 700–800 mAh | 6 × 30 × 40 | ~14 g | usually | JST-PH | ~MXN 120–180 | estimate |
| 600–700 | **UNIT Electronics 802535** | 650 mAh | 8 × 25 × 35 | ~13 g | listing to verify | JST | uelectronics.com (price not readable by bot) | listing exists |
| 1100–1300 | 103040 generic | 1200 mAh | 10 × 30 × 40 | ~24 g | usually | JST-PH | ~MXN 180–250 | estimate |

**Note on stock:** marketplace listings could not be opened programmatically (anti-bot); prices in the
"estimate" rows come from search snippets and must be confirmed at purchase time.

## 4. Why not import cells
Lithium cells are Class 9 dangerous goods: carrier restrictions (USPS forbids international mail), UN38.3
paperwork, and Digi-Key returned no LiPo results for Mexico. **Buy cells in Mexico.**

## 5. Handling rules for the team
- Inspect every cell: no puffing, PCM present, measure OCV (≥ 3.6 V on arrival).
- **Check JST polarity** before plugging into the Feather (many Chinese cells use reversed polarity).
- Charge first time on the bench at 0.3 C with supervision; LiPo bag for storage.
- Enclosure must leave **≥ 10 % thickness** swelling allowance (0.8 mm for an 8 mm cell) and foam, never a
  rigid clamp.

## 6. Runtime (summary — details in `electronics/power_budget.md`)

| Scenario | mAh/day | 700 mAh | 1000 mAh |
|---|---|---|---|
| A — pocket standby (nominal BLE) | 23 | 26 days | 37 days |
| B — normal day (nominal BLE) | 29 | 21 days | 29 days |
| B′ — normal day, pessimistic BLE link (2 mA) | 68 | 9 days | 12.5 days |
| C — heavy day incl. 5 min Wi-Fi | 96 | 6 days | 9 days |

(usable = 85 % of nameplate). These are **model outputs, not claims**; Test 9 replaces them with measurements.
