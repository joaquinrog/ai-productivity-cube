# Bring-up plan — Phase A (bench)

Rule: **one subsystem at a time**, commit firmware after each pass, log results in `notes/research_log.md`.
Toolchain: ESP-IDF v5.x (primary) — Arduino-ESP32 allowed for quick driver checks. Wiring: `prototype_wiring.md`.

| # | Test | Setup | Success criteria |
|---|---|---|---|
| 1 | **ESP32 dev environment** | Feather on USB-C, ESP-IDF | `idf.py flash monitor` works over native USB; PSRAM detected = 2 MB; deep-sleep → wake on PTT (A0) works; Feather `I2C_POWER` (GPIO7) driven high |
| 2 | **One display** | module 0 on SPI | GxEPD2/ESP-IDF driver draws `WORK` full-screen; full refresh ≤ 2.5 s; **partial update ≤ 0.35 s** measured (BUSY low→high) on a logic analyzer; image persists with module unplugged |
| 3 | **Four displays on a shared bus** | 4 modules, shared SCK/MOSI/DC/RST, CS×4, BUSY×4 | All four addressed independently; **no cross-talk** after 1,000 random partial updates; SPI ≥ 10 MHz with clean edges on the scope/LA; ghosting acceptable after 20 partials, full-refresh cadence chosen; refresh energy per panel measured with PPK2; serialized refresh keeps 3V3 peak < 30 mA above baseline |
| 4 | **IMU orientation** | BMI270 on Qwiic, block fixture with 4 faces | Face classification **100 % correct over 200 rotations** (4 faces × 50); decision latency ≤ 1 s after the cube stops; no false face change from tilts < 30°; any-motion INT wakes the S3 from deep sleep; IMU current in LP mode measured ≤ 30 µA |
| 5 | **Microphone capture** | ICS-43434 I2S, then MP34DT01 PDM | 16 kHz/16-bit WAV recorded on PTT hold; speech intelligible at 30 cm (5-person listening check); SNR estimate ≥ 50 dB in a quiet room; key-click trimmed; PDM path produces equivalent audio (validates Phase B choice) |
| 6 | **Haptic feedback** | DRV2605L + LRA on a 90 g dummy; ERM for A/B | Auto-calibration succeeds (resonance ≈ 205–215 Hz); 5 patterns distinguishable by ≥ 4 of 5 testers blindfolded; LRA preferred over ERM by majority (else revisit D-007); IMU interrupts masked during playback |
| 7 | **BLE connection** | NimBLE GATT server + minimal phone app (Android first, then iOS) | Pairs and reconnects automatically after phone reboot and after 1 h idle; Opus/ADPCM audio of an 8 s utterance delivered with < 1 s extra latency; **measured keep-alive average current** with phone screen off for 30 min (replaces the 0.25–2 mA assumption); iOS app backgrounded still receives `face_changed` within 2 s |
| 8 | **Power subsystem** | PPK2 in source mode on Feather BAT; thermocouple | Sleep, BLE-idle, PTT, refresh and haptic currents logged; light-sleep floor with/without 32 kHz XTAL compared on a board that has one (or documented as Phase B test); charger temperature at 400 mA charge in a closed printed box ≤ 15 °C rise |
| 9 | **Battery operation** | 803040 + 603040 cells, Feather MAX17048 | 48 h scripted "normal day" run on battery; mAh/day within ±30 % of `power_budget.md` (else update the model); MAX17048 SoC error ≤ ±5 % vs coulomb count from PPK2; brown-out never occurs at SoC > 5 % |
| 10 | **Dock detect** | VBUS divider on A3; printed dock wall + face-B coupon with 8 pogo pins and magnets | Dock/undock event detected in < 300 ms (wakes from deep sleep); contact resistance < 100 mΩ over 200 dock cycles; all 4 rotations make contact; magnet hold > 4× pogo spring force (luggage-scale measurement) |
| 11 | **Integrated interaction** | everything on the cross fixture + phone app + stub backend | End-to-end: rotate to STUDY → phone sees context; hold PTT "remind me tomorrow at 9" → stub agent replies → **haptic confirm < 150 ms after card arrives**, card visible ≤ 0.5 s later; 20 consecutive runs without reboot; logged energy per interaction |

## Exit criteria for Phase A
All 11 tests pass **or** each failure has a recorded decision (superseding ADR) before Phase B schematic starts.
