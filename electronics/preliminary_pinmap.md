# Preliminary pin map — ESP32-S3-WROOM-1-N16R2 (Phase B)

Status: **Preliminary** (no schematic yet). Verified against **ESP32-S3-WROOM-1/1U datasheet v1.8,
Table 3-1 & §4** and **ESP32-S3 Series datasheet v2.2, Tables 2-2 (power-up glitches), 3-1 (strapping),
5-10**, downloaded 2026-10-05. Phase A (Feather) wiring is in `prototype_wiring.md`.

## Constraints checked

| Constraint | Source | Effect on the map |
|---|---|---|
| Strapping pins **GPIO0** (boot, weak PU), **GPIO3** (JTAG source, floating; only used if eFuse STRAP_JTAG_SEL burnt), **GPIO45** (VDD_SPI, weak PD — must be low for 3.3 V flash), **GPIO46** (boot/ROM print, weak PD) | WROOM-1 DS Table 4-1 | GPIO0 = BOOT key only; GPIO45/46 left **NC**; GPIO3 used with an external pull-down for an *output* (HAPTIC_EN) — safe with default eFuses |
| Flash/PSRAM pins GPIO26–32 | not exposed on WROOM-1 | — |
| **Octal** PSRAM uses GPIO35–37 | WROOM-1 DS Table 3-1 note b | N16R2 is **quad** → GPIO35–37 usable |
| GPIO47/48 run at 1.8 V only on R16V variants | note c | 3.3 V on N16R2 ✓ |
| USB D−/D+ = GPIO19/20 (USB-Serial/JTAG default) | DS v2.2 §IO MUX | reserved for service USB-C |
| UART0 = GPIO43 TX / GPIO44 RX | Table 3-1 | test pads |
| JTAG on GPIO39–42 | Table 3-1 | not needed (USB-JTAG) → used as GPIO |
| XTAL_32K_P/N = **GPIO15/16** | Table 3-1 | 32.768 kHz crystal |
| ADC2 unusable while Wi-Fi active | DS v2.2 §ADC | analog sense only on ADC1 (GPIO1–10) |
| Deep-sleep wake (ext0/ext1) needs **RTC GPIO 0–21** | DS v2.2 RTC IO MUX | keys, IMU INT, VBUS, CHG_INT on RTC pins |
| **Power-up glitches** on GPIO1–14, 17, 18, 19, 20, XTAL pins (60 µs low; 19/20 high) | DS v2.2 Table 2-2 | load-switch enables on glitch-free pins (GPIO37, 42) |
| FSPI IO-MUX pins: CS0 10, D 11, CLK 12, Q 13 | Table 3-1 | panel SPI on IO-MUX pins for clean timing |

## Map

| GPIO | Function | Bus | Direction | Boot concern | Notes |
|---|---|---|---|---|---|
| 0 | BOOT key (service, behind face-A cap) | — | in | **strap** (PU = SPI boot) | key to GND; never pulled low by other circuitry |
| 1 | VBUS_SENSE (dock/USB detect) | ADC1_CH0 | in | glitch (input, harmless) | 100 k / 150 k divider from VBUS; RTC wake |
| 2 | BTN_PTT | — | in | glitch harmless | active-low, RTC pull-up; ext1 wake |
| 3 | HAPTIC_EN (DRV2605L EN) | — | out | **strap (JTAG sel)**, ignored with default eFuse | 100 k pull-down → DRV off during boot |
| 4 | BTN_AUX | — | in | — | active-low; also to BQ25180 TS/MR via isolation (schematic review) |
| 5 | IMU_INT1 (any/no-motion) | — | in | — | RTC wake |
| 6 | IMU_INT2 (steps/activity) | — | in | — | **freeable** |
| 7 | CHG_INT (BQ25180 /INT, open-drain) | — | in | — | RTC; 100 k PU |
| 8 | I2C_SDA | I2C0 | bi | glitch (bus idle) | 4.7 k to 3V3 |
| 9 | I2C_SCL | I2C0 | out | glitch (bus idle) | 4.7 k to 3V3 |
| 10 | EPD_CS0 | FSPI CS0 (IO MUX) | out | glitch — panels unpowered at boot | 100 k PU |
| 11 | EPD_MOSI | FSPID (IO MUX) | out | glitch — panels unpowered | 33 Ω series |
| 12 | EPD_SCK | FSPICLK (IO MUX) | out | glitch — panels unpowered | 33 Ω series |
| 13 | EPD_DC | — | out | glitch — panels unpowered | shared |
| 14 | EPD_RST (shared) | — | out | glitch — panels unpowered | shared |
| 15 | XTAL_32K_P | — | — | glitch n/a | 32.768 kHz crystal |
| 16 | XTAL_32K_N | — | — | — | 32.768 kHz crystal |
| 17 | FG_ALRT (MAX17048 ALRT, open-drain) | — | in | — | **freeable** (poll SoC instead) |
| 18 | STATUS_LED | — | out | glitch → LED blips at boot (acceptable) | single LED behind light pipe |
| 19 | USB_D− | USB | bi | high glitch at power-up (DS note) | service USB-C |
| 20 | USB_D+ | USB | bi | high glitch at power-up | service USB-C |
| 21 | EPD_CS1 | — | out | glitch-free | 100 k PU |
| 35 | MIC_PDM_CLK | I2S0 PDM | out | — (quad PSRAM) | |
| 36 | MIC_PDM_DATA | I2S0 PDM | in | — | 2nd mic footprint (DNP) shares this line |
| 37 | MIC_PWR_EN (TPS22916C #2) | — | out | glitch-free | 100 k PD |
| 38 | EPD_BUSY0 | — | in | — | |
| 39 | EPD_BUSY1 | — | in | (MTCK unused) | |
| 40 | EPD_BUSY2 | — | in | (MTDO unused) | |
| 41 | EPD_BUSY3 | — | in | (MTDI unused) | |
| 42 | EPD_PWR_EN (TPS22916C #1) | — | out | glitch-free (MTMS unused) | 100 k PD |
| 43 | UART0_TX | UART0 | out | ROM boot log | test pad |
| 44 | UART0_RX | UART0 | in | — | test pad |
| 45 | **NC** | — | — | **strap VDD_SPI** | leave unconnected |
| 46 | **NC** | — | — | **strap boot/ROM print** | leave unconnected |
| 47 | EPD_CS2 | — | out | 3.3 V on N16R2 | 100 k PU |
| 48 | EPD_CS3 | — | out | 3.3 V on N16R2 | 100 k PU |
| EN | CHIP_PU | — | in | RC 10 k / 1 µF | test pad (+ optional reset key) |

**Budget:** 34 of 36 GPIO used; GPIO45/46 intentionally NC. Freeable if needed: GPIO6, GPIO17.

## Rules for firmware
1. Before switching `EPD_PWR_EN` off, drive GPIO10–14, 21, 47, 48 **low** (or Hi-Z) — prevents back-powering panels through ESD diodes.
2. Keep `HAPTIC_EN` low except during playback.
3. Deep-sleep wake set: ext1 on GPIO2 | GPIO4 | GPIO5 | GPIO1 | GPIO7 (any-low/any-high mix needs care: VBUS_SENSE is active-high → use ext1 "any high" with inverted keys or ext0 for VBUS; finalize in firmware design).
4. Mask IMU any-motion for ~150 ms around haptic playback.
