# Research log

## 2026-10-05 — TASK-001
- Workspace created at `~/ai-cube` (no prior project found in the home directory).
- **Sourcing reality check (Digi-Key MX):** every Espressif ESP32-S3-DevKitC-1 variant is 0-stock or obsolete; WROOM-1-N8R2
  0-stock until 2027-11; **WROOM-1-N16R2 in stock (7,110)**; Adafruit Feather ESP32-S3 #5477 in stock (328).
- Digi-Key MX does not stock monochrome 1.54″ e-paper modules (Adafruit #4196 discontinued; Seeed Grove tri-color only) →
  Waveshare direct.
- **NHD-1.5-128128UGC3 datasheet:** OLED panel ICC 160 mA typ / 330 max, sleep 2 mA typ, burn-in warning → key evidence
  against 4 OLEDs.
- **ESP-IDF power_save README:** ESP32-S3 BLE light-sleep 230 µA with 32 kHz XTAL vs 3.3 mA without; ESP32-C6 34 µA.
- **ICS-43434 is obsolete** (Digi-Key: 94,290 last-time stock); TDK replacements T5837/T5838 are 1.8 V-only → chose IM69D130.
- LSM6DSV16X IC 0-stock at Digi-Key MX; ICM-42688-P has APEX (pedometer/tilt/tap/WoM) but no orientation engine.
- BMI323 datasheet: suspend 15 µA, accel-LP 45 µA (vs BMI270 3.5 / "down to 4" µA).
- BQ25180 I2C address 0x6A confirmed; IQ_BAT 3–4 µA; ship 3.2 µA. DRV2605L shutdown 4 µA (not nA).
- TPS63900 limited to ">400 mA" → rejected for Wi-Fi peaks.
- Lithium cells: not importable practically (Class 9) → local: Cyberpuerta DP-80304 MXN 177 (+128 shipping).
- Mexico courier duty on non-FTA (China) parcels: 33.5 % since 2025-08-15; Digi-Key MX is CPT (taxes on delivery).
- Mercado Libre / Amazon MX / UNIT block automated reads (403/503, Cloudflare); Chrome not installed for DevTools →
  marketplace prices are search-snippet estimates, flagged in the cart.
- Model (`tools/cube_model.py`): 55 × 55 × 45 ≈ 132 cm³, ~86 g; 50³ panel margin only 0.7 mm; standby 0.63/0.96/2.58 mA.
