# Risk register (TASK-001)

Likelihood / Impact: L = low, M = medium, H = high. Owner of every mitigation: Phase A/B test noted.

| ID | Risk | Likelihood | Impact | Evidence | Mitigation |
|---|---|---|---|---|---|
| R-01 | **Four-display power** | L (with e-paper) | H | OLED: 160 mA on, 2 mA sleep each (NHD DS). E-paper: 26.4 mW × 0.3 s, 0 W hold | D-003 e-paper + gated rail; Test 3 PPK2 measurement |
| R-02 | **Display bus performance** (shared SPI, long traces to 4 faces) | M | M | 5 kB/frame → 2–4 ms @10–20 MHz; refresh is waveform-bound | 33 Ω series, ≤ 10 MHz in Phase B, LA check in Test 3 |
| R-03 | **E-paper UX latency / ghosting** | M | M | partial 0.26–0.3 s, full 2 s with flash | haptic gives instant feedback; full refresh only on face change when hidden / on dock; Test 3 cadence; Sharp memory LCD fallback |
| R-04 | **Display module thickness** (Phase A modules don't fit) | H (expected) | L | module 48 × 33 PCB | Phase B uses raw 1.05 mm panels |
| R-05 | **Raw display integration** (booster per panel, FPC fold, ZIF blind mating) | M | H | SSD1681 needs external boost parts; 4 × FH12 on a 44 mm board | build a single-panel booster coupon PCB first (TASK-003); FPC fold mock in TASK-002 |
| R-06 | **Display durability in pocket** (glass panels, pressure, drops) | M | H | bare glass panels behind 0.8 mm PMMA | recess windows 0.3 mm, foam backer, 1 m drop test on Phase B shell; consider 0.55 mm chemically-strengthened glass |
| R-07 | **ESP32 antenna placement** | M | H | WROOM-1 keep-out; battery, magnets, LRA, panel backplanes nearby | panel-free 8 mm band at face A or WROOM-1U + flex antenna; RSSI test vs. bare module (≤ 6 dB loss) |
| R-08 | **BLE reliability** (reconnects, coexistence with Wi-Fi) | M | H | single 2.4 GHz radio, time-sliced coex | BLE-first policy, no Wi-Fi scan during audio; Test 7 reconnect criteria |
| R-09 | **BLE keep-alive cost set by the phone** | M | M | model 0.25–2 mA (8× spread) | measure in Test 7; request long intervals via connection-parameter update; allow disconnect + fast re-advertise strategy |
| R-10 | **iOS background behaviour** (app suspended/killed, BLE events delayed) | H | H | Core Bluetooth background limits; force-quit stops relaunch | state restoration, queue in PSRAM, Wi-Fi fallback, Android-first dev; explicit iOS test in Test 7 |
| R-11 | **Wi-Fi peak current** | L | M | 340 mA TX (DS T.5-7) | TPS63802 2 A; 22 µF+ bulk on 3V3; no Wi-Fi at < 15 % SoC |
| R-12 | **Microphone acoustics** (port, gasket, leaks) | M | M | bottom-port MEMS needs sealed path | gasket + Ø0.8–1.0 mm port + mesh; record test in printed shell (Phase B) |
| R-13 | **Charging heat** | M | M | linear: (5 − 3.6) × 0.4 A ≈ 0.56 W in ~120 cm³ | ICHG 300–400 mA, BQ25180 thermal regulation, copper pour, Test 8 thermocouple in closed box |
| R-14 | **LiPo swelling / safety** | L–M | H | unbranded cells, pocket heat, pressure | PCM required, 10 % swell gap + foam, inspect cells, charge only 0–45 °C (firmware via BQ25180 + IMU temp), no rigid clamp |
| R-15 | **Rubbing / wind / key-click noise** | M | M | thumb on face A near mic | port offset ≥ 10 mm from PTT, HPF, trim first/last 80 ms |
| R-16 | **Haptic coupling** (foam-isolated LRA feels weak) | M | M | LRA rated on 100 g rigid jig | bond LRA to a rigid rib/face; Test 6 on a 90 g dummy, re-test in Phase B shell |
| R-17 | **Pogo alignment** | M | M | 4 rotations, lift-and-reseat docking | concentric rings (rotation-invariant), locating lip in dock floor, magnets; Test 10 |
| R-18 | **Pogo wear / contamination** | L | M | Mill-Max 0906: 1 M cycles; pocket lint on pads | springs in the dock (replaceable), ENIG pads flush, wipe-clean surface |
| R-19 | **Dock geometry / scrape short** | M | M | VBUS pin crosses GND ring while docking | Hall-gated, current-limited dock VBUS; no data rings connected in V1 |
| R-20 | **Accidental button presses** (pocket) | H | M | keys on a 55 × 55 face that rests against the thigh | recessed keys inside a 1 mm guard ring, 260 gf PTS526, PTT requires ≥ 150 ms hold + not-in-pocket heuristic (IMU), ALS footprint as fallback |
| R-21 | **Audio captured in pocket by accident** | M | H (privacy) | consequence of R-20 | LED + haptic on PTT start, discard < 400 ms utterances, no send without release, ALS fallback |
| R-22 | **FFC routing** (4 tails to one board) | M | H | 15.4 mm connectors, 44 mm board | connector placement study + paper/Kapton FPC mock (TASK-002); FPC extension adapters as fallback |
| R-23 | **Enclosure assembly** (glued panels + blind ZIF latches) | M | M | 4 faces + 2 caps | assembly order designed with jig; face-A cap removable with screws |
| R-24 | **50 mm feasibility** | H | M | panel 37.32 needs W ≥ 49.3 with 6 mm radius (0.7 mm margin) | not recommended; only with smaller radius or smaller panel |
| R-25 | **55 × 55 × 40–45 feasibility** | L (45) / M (42) | M | 42 needs flex antenna or < 8 mm band | rev A at 45; RF test decides 42 |
| R-26 | **Thickness comfort in pants pocket** | M | H | 42–45 mm ≈ Rubik's-class bulge | physical mockup test with 3 thicknesses (TASK-002) before CAD freeze |
| R-27 | **Component obsolescence** | M | M | ICS-43434 obsolete; DevKitC boards obsolete/0-stock; WROOM-1-N8R2 0-stock | Phase B uses active parts (IM69D130, N16R2); check stock at order time |
| R-28 | **Import costs/delays** (33.5 % China courier rate, hazmat cells) | H | M | SAT 2025-08-15 rule; DK CPT | consolidate orders, buy cells locally, budget tax explicitly |
| R-29 | **Magnets attract debris / affect cards** | M | L | N52 on face B | 0.5–1 mm skin, user guidance; dock Hall sensor benefits from them |
| R-30 | **Hand assembly of DSBGA/LGA parts** | H if hand-built | M | BQ25180 1.6 × 1.1 BGA, BMI270/mic LGA | JLC PCBA; BQ25185 (WSON) fallback for hand builds |
