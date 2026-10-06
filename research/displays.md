# Research — Displays (critical subsystem)

Checked 2026-10-05. Decision record: D-003, D-004, D-005.

## 1. What the display must do (derived from the brief)

| Need | Implication |
|---|---|
| Each face shows its context (`WORK`, `STUDY`, …) so the cube *is* a context switch | Ideally visible **while the cube sleeps** |
| Up-face shows status: `✓ SAVED / Tomorrow 09:00`, `01:27 FOCUS 3 pending` | 1–4 short lines, large type; 1 Hz–1/min updates |
| Pocket Mode | ~0 W when idle; survive pocket pressure |
| Desktop Mode | richer layout, external power allowed |
| Face is ~55 × 45 mm, panel must sit inside a ~47 × 38 mm window region | ≈1.3–1.5″ class |

## 2. Technology comparison

| | **E-paper 1.54″ B/W** (SSD1681) | **RGB OLED 1.5″** (SSD1351) | **Gray OLED 1.5″** (SSD1327) | **Sharp Memory LCD 1.28″** | **IPS TFT 1.3–1.54″** (ST7789) |
|---|---|---|---|---|---|
| Example part | Waveshare #12955 module / #12561 raw; GD GDEY0154D67 | Waveshare #14747; NHD-1.5-128128UGC3 | Waveshare #13992 | LS013B7DH03 | generic 240 × 240 |
| Resolution | 200 × 200 (184 dpi) | 128 × 128 | 128 × 128, 16 gray | 128 × 128 | 240 × 240 |
| Active area | 27.6 × 27.6 mm | 26.9 × 26.9 (NHD 28 × 28) | 26.9 × 26.9 | 23.0 × 23.0 | ≈23 × 23 / 27.7 × 27.7 |
| Raw outline / thickness | **31.8 × 37.32 × 1.05** | ≈33 × 37 × 1.6–2 (glass + FPC) | similar | ≈26 × 29 × 0.8 (verify) | ≈31 × 33 × 1.6 + backlight |
| Module outline | 48 × 33 | 44.5 × 37.0 | 44.5 × 37.0 | breakout 37 × 33 (Adafruit) | ≈38 × 32 |
| Interface | 4-wire SPI | SPI | SPI / I2C | SPI + EXTCOMIN | SPI |
| Image retained unpowered | **Yes (bistable)** | No | No | No (needs VCOM toggling, µW) | No |
| Active power | 26.4 mW during 0.3 s partial | **ICC 160 mA typ / 330 max** (NHD DS) | ~20–60 mA | ~µW at 1 Hz | 15–30 mA backlight |
| Sleep / idle | 0 (gated) · 0.7–1 µA deep sleep (SSD1681 DS) | **2 mA typ (NHD DS)** unless gated | mA-class | 2–5 µA | backlight off, blank |
| Update latency | **0.26–0.3 s partial; 1.5–2 s full (flashes)** | <16 ms | <16 ms | <16 ms | <16 ms |
| Viewing angle | >170°, sunlight readable | wide | wide | moderate, reflective | IPS wide |
| Dark readability | **No** (front-light variant FL04 exists) | Yes | Yes | No | Yes |
| Burn-in | No | **Yes** (NHD DS warning) | Yes | No | No |
| Price (qty 1) | **raw USD 5.99**, module 9.99 | raw 24.55, module 18.99 | module 12.99 | raw 12.39 | ~USD 4–8 |
| Availability | Waveshare / Good Display (not at DK MX) | DK 306 pcs | Waveshare | DK **27,094 pcs** | marketplaces |
| ESP32 driver | GxEPD2, ESP-IDF components, LVGL (1-bit) | Adafruit_SSD1351, LVGL | U8g2 | Adafruit_SharpMem, LVGL | TFT_eSPI, LVGL |

## 3. Why e-paper wins for V1

1. **The cube is asleep >95 % of the time.** Only bistable displays keep the context labels visible
   for free. With four OLEDs the user sees a blank black cube until it wakes (IMU pickup), which
   undermines "orientation is the interface".
2. **Power.** Four NHD OLEDs merely *sleeping* draw 8 mA → 1000 mAh lasts ~4 days on that alone.
   One OLED lit at a modest 40 mA for 15 min/day adds 10 mAh/day — a third of the whole e-paper day budget.
3. **Thickness & mechanics.** 1.05 mm raw panel; leaves room for FPC fold and backer in a 3.85 mm face stack.
4. **Cost.** Raw e-paper is 4× cheaper than raw RGB OLED.

Accepted costs: 0.3 s partial-refresh latency, periodic full refresh (ghosting), no dark readability,
glass fragility (mitigated by cover window, `electronics/risks.md`).

## 4. Monochrome vs color (D-004)
Nothing in the core UX needs color. Color e-paper takes 10–20 s per refresh. Color OLED loses
bistability. **Monochrome.** Differentiate contexts with inversion, patterns, iconography.

## 5. Can 4 displays share one SPI bus? — Yes

- SSD1681 is written over 4-wire SPI (CS, DC, SCK, MOSI) plus RST and BUSY.
- Frame = 200 × 200 / 8 = **5,000 bytes**; at 10 MHz ≈ 4 ms, at 20 MHz ≈ 2 ms.
- Refresh time (0.3 s partial) is waveform-limited inside the panel, so bus sharing is invisible.
- Shared: SCK, MOSI, DC, RST. Per panel: CS, BUSY. → 4 + 4 + 4 = **12 GPIO**.
- Firmware serializes refreshes (one panel at a time) to cap rail current at ~8 mA + booster inrush.
- Risk: long shared SCK/MOSI traces to four faces → keep ≤ 10 MHz, series 33 Ω at source,
  verify with logic analyzer (Test 3).

## 6. Can inactive displays be power-gated? — Yes, and it is free with e-paper

- Image persists with the panel unpowered. Gate all four through one **TPS22916C** (2 A, 10 nA off).
- After power-up each SSD1681 needs reset + init + LUT (~10–20 ms) before a partial update.
- **Back-powering hazard:** when the rail is off, drive CS/DC/RST/MOSI/SCK **low or Hi-Z**, otherwise
  current flows through panel ESD diodes. Must be enforced in firmware and checked with PPK2 (Test 3).
- Independent control: yes (per-CS). Individual rails per panel are not needed.

## 7. Phase A vs Phase B implementations

| | Phase A — off-the-shelf modules | Phase B — raw panels |
|---|---|---|
| Part | 4 × Waveshare 1.54″ e-Paper Module #12955 (USD 9.99) | 4 × raw panel #12561 / GDEY0154D67 (USD 5.99) + 1 spare |
| Booster | on module | per-panel booster on main PCB (or 4 tiny FPC daughter boards) |
| Connection | 8-pin PH2.0 cable → breadboard | 24-pin 0.5 mm FPC tail → Hirose FH12-24S-0.5SH(55) ZIF |
| Size | 48 × 33 mm PCB — does **not** fit the enclosure | 31.8 × 37.32 × 1.05 — fits a 55 mm face |
| Purpose | bus, refresh, ghosting, power, UX latency | real packaging and FPC routing |

## 8. Display-cost sensitivity (from `tools/cube_model.py`)

| Metric | Value |
|---|---|
| Phase A: 4 e-paper modules | USD 39.96 = **MXN 739** |
| Share of Phase A consumed electronics (req + rec, MXN 2,188) | **34 %** (just under the 35 % flag) |
| Phase B: 4 raw panels + 4 FPC connectors + 4 booster sets | USD 39.60 = **MXN 732** |
| Share of Phase B per-unit components (MXN 1,825) | **40 % → above 35 %: flagged** |
| Mono vs color delta, modules (RGB OLED 18.99 vs 9.99) | +USD 36 / +MXN 666 for 4 |
| Mono vs color delta, raw (NHD 24.55 vs 5.99) | +USD 74 / +MXN 1,373 for 4 |
| Module vs raw e-paper per panel | 9.99 vs 9.90 (raw + Hirose + booster) → **≈ no saving**; with a JLC-stocked FPC connector ≈ 7.7 → saves ~USD 2.3/panel |

**Is >35 % acceptable for V1? Yes.** The four faces are the product's defining feature; the next
best option (RGB OLED) would push the display share to ~60 % and break the power budget. The
lever to pull if cost matters later is the FPC connector (Hirose → JLC-stocked part), not the panel.

## 9. Open display questions
- Ghosting after N partial refreshes on this panel → full-refresh cadence (Test 3).
- Partial-refresh behaviour below 10 °C (spec 0–50 °C).
- Pocket pressure / impact on bare glass behind a 0.8 mm PMMA window (drop test in Phase B).
- Front-light variant (GDEY0154D67-FL04) for dark readability — parked for V2.
