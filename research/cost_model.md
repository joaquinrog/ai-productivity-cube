# Research — Cost model (method and assumptions)

Checked 2026-10-05. Numbers: `bom/COST_BREAKDOWN.md` (generated from `tools/cube_model.py`).

## 1. Currency
- Banxico FIX determined 2026-10-01: **18.3688 MXN/USD**; market ~18.07 on 2026-10-02.
- Planning rate: **18.50 MXN/USD** (FIX + card spread, rounded up). Native USD prices are preserved in `bom/BOM.csv`.

## 2. Vendor landed-cost rules

| Channel | Price basis | Shipping | Taxes / duties | Source |
|---|---|---|---|---|
| Digi-Key México | USD | **free ≥ USD 100**, else USD 30 | **CPT**: IVA/duties/courier fees paid on delivery. Planning **25 %** (range 16–33.5 %) | Digi-Key MX site/search summary; MX courier rules |
| Mouser México | USD | free ≥ USD 100 (most orders) | **DDP** (included) — compare at checkout | Mouser MX (search summary) |
| Waveshare (China) | USD | **assumed USD 20** (quote at checkout) | **33.5 %** courier rate for non-FTA origin since 2025-08-15 | SAT/press coverage |
| JLCPCB / JLC3DP (China) | USD | DHL ≈ USD 25 (BOM row) | **33.5 %** | same |
| Cyberpuerta / Mercado Libre / UNIT / Amazon MX | MXN incl. IVA | per listing (Cyberpuerta MXN 128) | included | listings |

US-origin parcels under USD 50 are duty/IVA-exempt under USMCA courier rules; 50–117 → 17 %, > 117 → 19 %.
Most electronics shipped by Digi-Key are *not* US-origin goods, so the 25 % planning rate is deliberately conservative.

## 3. Cost categories
1. **Reusable development hardware** — dev boards, PPK2, cables, breadboard, logic analyzer. Survives into Phase B and beyond.
2. **Phase A consumed electronics** — display modules, breakouts, battery, keys, pogo pins.
3. **Phase B integrated electronics** — module, raw panels, ICs, PCB, PCBA, shipping/duty. First unit carries **batch fees** (PCB ×5, PCBA ×2 boards).
4. **Mechanical** — mockups, SLA enclosure ×2 iterations, windows, magnets, dock.
5. **Unknown / contingency** — Phase A **15 %**, Phase B **25 %** (first-of-kind PCB, likely one respin of the enclosure, broken panels, wrong-polarity cells).

## 4. Assumptions that move the result most
| Assumption | Value | If wrong |
|---|---|---|
| DK tax on delivery | 25 % | ±MXN 400 on Phase A |
| Waveshare shipping | USD 20 | ±MXN 300 |
| JLC PCBA fees | USD 58 (setup 8 + stencil 1.5 + ~15 extended feeders × 3 + joints) | ±MXN 500 |
| SLA enclosure | USD 25 per iteration | could be MXN 300–1,500 depending on service |
| PPK2 bought vs borrowed | MXN 2,104 + tax | single largest Phase A swing |

## 5. Hypotheses vs. researched estimate

| Hypothesis (brief) | Researched | Verdict |
|---|---|---|
| Phase A budget MXN 3,000–4,500 | **MXN ~4,800 landed (PPK2 borrowed) → ~5,500 with 15 % contingency**; **~7,300 → ~8,400** if a PPK2 is bought | budget is short unless the lab lends a power profiler and the team accepts tight contingency |
| Phase A electronics subtotal MXN 2,300–3,700 | **MXN 2,188** goods (consumed, req + rec) | ✔ low end |
| Phase B first unit MXN 2,700–5,800 (target ~4,000) | **≈ MXN 7,800 landed → ≈ 9,750 with 25 %** (range ~7,000–10,000) | ✗ too optimistic — batch PCB/PCBA/DHL/duty fees (~MXN 2,800) dominate a single unit |
| Repeat unit MXN 1,500–2,500 | **≈ MXN 2,480 at 10 units** (range ~2,100–2,900) | ✔ upper half |
