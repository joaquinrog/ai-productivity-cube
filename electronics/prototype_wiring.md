# Phase A — bench wiring (Adafruit ESP32-S3 Feather #5477)

Feather header → GPIO mapping taken from Adafruit CircuitPython board definition
`ports/espressif/boards/adafruit_feather_esp32s3_4mbflash_2mbpsram/pins.c` (fetched 2026-10-05).
All 20 header GPIOs are used.

## On-board resources (do not reuse)
NeoPixel GPIO33, NeoPixel power GPIO21, **I2C_POWER GPIO7 (must be driven HIGH to power STEMMA QT + I2C pull-ups)**,
red LED GPIO13, BOOT GPIO0, MAX17048 on I2C at 0x36, LiPo JST-PH, USB-C.

## Wiring table

| Function | Feather pin | GPIO | RTC? | Device pin |
|---|---|---|---|---|
| I2C SDA | SDA | 3 | yes | STEMMA QT chain: BMI270 (0x68) → DRV2605L (0x5A) → [VEML7700 0x10 optional] |
| I2C SCL | SCL | 4 | yes | same |
| EPD SCK (shared) | SCK | 36 | no | all 4 modules `CLK` |
| EPD MOSI (shared) | MOSI | 35 | no | all 4 modules `DIN` |
| EPD DC (shared) | D11 | 11 | yes | all 4 `DC` |
| EPD RST (shared) | D12 | 12 | yes | all 4 `RST` |
| EPD CS0..3 | D5, D6, D9, D10 | 5, 6, 9, 10 | yes | module 0..3 `CS` |
| EPD BUSY0..3 | RX, TX, A2, A3 | 38, 39, 16, 15 | –, –, yes, yes | module 0..3 `BUSY` |
| I2S BCLK | A4 | 14 | yes | ICS-43434 `BCLK` |
| I2S WS | A5 | 8 | yes | ICS-43434 `LRCL` |
| I2S DIN | MISO | 37 | no | ICS-43434 `DOUT` (SEL → GND = left) |
| PDM CLK (alt. test, swap with I2S) | A4 | 14 | | MP34DT01 `CLK` |
| PDM DATA (alt. test) | MISO | 37 | | MP34DT01 `DAT` |
| BTN_PTT | A0 | 18 | **yes** | key to GND (internal pull-up) — deep-sleep wake |
| BTN_AUX | A1 | 17 | **yes** | key to GND |
| IMU_INT1 | D13 | 13 | **yes** | BMI270 `INT1` (red LED mirrors the interrupt — handy) |
| Power | 3V3 / GND | | | modules + breakouts (Feather LDO; e-paper draws ≤ 10 mA each during refresh) |
| LRA | — | | | DRV2605L `+`/`−` (set LRA mode, library 6) |

## Test-specific re-wiring
- **Test 10 (dock detect):** borrow A3 (GPIO15) from BUSY3; wire Feather `USB` (VBUS) → 100 k/150 k divider → A3. Or detect charging via MAX17048 CRATE > 0.
- **PDM test:** unplug ICS-43434, plug MP34DT01 on the same two pins.
- **Power measurements:** power the Feather from the PPK2 in *source meter* mode on `BAT` (3.7 V), USB unplugged. Expect the Feather's own ~100 µA deep-sleep floor — subtract it or measure modules separately.

## Physical layout tips
- Four modules on a printed "cross" fixture approximating the four faces, cables ≤ 20 cm (PH2.0 cables supplied).
- Twist SCK with GND; start SPI at 4 MHz, raise to 10–20 MHz after Test 3 passes.
- Keep the LRA taped to a ~90 g dummy block (cube mass) for haptic tests, not dangling.
