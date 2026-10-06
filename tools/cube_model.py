#!/usr/bin/env python3
"""
AI Productivity Cube — TASK-001 engineering model.

Single source of truth for the numbers used in the workspace docs:
  * size-envelope / packaging stack-up
  * mass estimate
  * power budget and runtime
  * BOM / cost model  (also writes bom/BOM.csv)

Run:  python3 tools/cube_model.py            (prints all tables)
      python3 tools/cube_model.py --csv      (also rewrites bom/BOM.csv)

Every input is either (a) a datasheet value — see bom/SOURCES.md — or
(b) an explicit ASSUMPTION marked as such below. Change assumptions here,
re-run, and update the docs; do not hand-edit derived numbers in the docs.
"""
import csv
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ----------------------------------------------------------------------------
# Currency
# ----------------------------------------------------------------------------
# Banxico FIX determined 2026-10-01 = 18.3688 MXN/USD. Card/FX spread ~0.7%.
FX_MXN_PER_USD = 18.50  # planning rate (ASSUMPTION: FIX + card spread, rounded)

# ----------------------------------------------------------------------------
# 1. Mechanical stack-up (all mm)
# ----------------------------------------------------------------------------
WALL = 1.8                # printed shell wall (SLA/MJF), ASSUMPTION
CORNER_R = 6.0            # outer edge radius, ASSUMPTION (pocket comfort)
# Display face stack measured from the outer surface inward:
WINDOW = 0.8              # PMMA/glass cover window, flush in wall cut-out
PANEL_T = 1.05            # e-paper raw panel thickness (Waveshare 12561 spec)
ADHESIVE = 0.2
PANEL_BACKER = 0.8        # printed rib / foam behind panel
FPC_FOLD = 1.0            # FPC tail folded behind panel
DISPLAY_DEPTH = WINDOW + PANEL_T + ADHESIVE + PANEL_BACKER + FPC_FOLD  # 3.85
PANEL_W, PANEL_H = 37.32, 31.8   # GDEY0154D67 / Waveshare 12561 outline
PANEL_ACTIVE = 27.6

# Axis stack (rotation axis runs face A -> face B)
FACE_A_STACK = 1.2 + 1.5 + 1.0 + 3.1 + 0.5   # cap + PTS526 switch + 1.0mm PCB + WROOM (3.1) + clr = 7.3
FACE_B_STACK = 2.5 + 0.8                     # wall w/ magnet pockets + dock-pad PCB = 3.3
ANTENNA_BAND = 8.0        # panel-free band from face A outer surface for PCB-antenna module

BATTERIES = [  # name, t, w, l, mAh(nominal), mass g (typical listing values; ASSUMPTION ±15%)
    ("103040 (1200 mAh)", 10.0, 30, 40, 1200, 24.0),
    ("803040 (1000 mAh)", 8.0, 30, 40, 1000, 20.0),
    ("603040 (700 mAh)", 6.0, 30, 40, 700, 14.0),
    ("802535 (650 mAh)", 8.0, 25, 35, 650, 13.0),
    ("503035 / Adafruit 1578 (500 mAh)", 5.0, 30, 36, 500, 10.5),
]

ENVELOPES = [(50, 50, 50), (52, 52, 38), (55, 55, 42), (55, 55, 45), (58, 58, 45), (60, 60, 50)]

REFERENCE_OBJECTS = [  # name, dims (mm), mass g, source
    ("AirPods Pro 2 case (USB-C)", (60.6, 45.2, 21.7), 50.8, "apple.com tech specs"),
    ("Rubik's Cube 3x3 (official)", (57, 57, 57), 75.0, "retail listings"),
    ("Flipper Zero", (100, 40, 25), 102.0, "docs.flipper.net tech specs"),
    ("Rabbit r1", (78, 78, 13), 115.0, "iFixit device page"),
]


def rounded_box_volume(a, b, c, r):
    """Box with all 12 edges rounded to radius r (corners approximated)."""
    v = a * b * c
    edge_loss = (1 - math.pi / 4) * r * r * (4 * (a + b + c) - 8 * 2 * r)
    corner_fix = 8 * (r ** 3) * (1 - math.pi / 6) - 8 * 3 * (1 - math.pi / 4) * r ** 3  # small correction
    return v - edge_loss - max(corner_fix, 0)


def envelope(W, D, H, flex_antenna=False):
    """W x D is the square cross-section (display faces are W x H); H is the rotation-axis length."""
    core = W - 2 * DISPLAY_DEPTH                  # free square inside the 4 display stacks
    axial = H - FACE_A_STACK - FACE_B_STACK       # free length along axis for battery/LRA
    panel_fit_w = W - 2 * CORNER_R >= PANEL_W     # panel must stay clear of rounded corner
    min_h_panel = PANEL_H + 2 * WALL + 1.0
    min_h_antenna = ANTENNA_BAND + PANEL_H + 0.5 + WALL
    panel_fit_h = H >= (min_h_panel if flex_antenna else min_h_antenna)
    best = None
    for name, t, bw, bl, mah, m in BATTERIES:
        fits_plan = core >= bl + 1.5 and core >= bw + 1.5
        lra_beside = core - bw >= 11.0             # 10 mm LRA beside the cell
        fits_axial = axial >= t * 1.1 + 0.5        # 10% swelling allowance + foam
        if fits_plan and fits_axial and lra_beside:
            best = (name, t, bw, bl, mah, m)
            break
    outer_v = rounded_box_volume(W, D, H, CORNER_R) / 1000.0  # cm3
    inner_v = (W - 2 * WALL) * (D - 2 * WALL) * (H - 2 * WALL) / 1000.0
    return dict(W=W, D=D, H=H, core=core, axial=axial, panel_fit_w=panel_fit_w,
                panel_fit_h=panel_fit_h, min_h_panel=min_h_panel, min_h_antenna=min_h_antenna,
                battery=best, outer_v=outer_v, inner_v=inner_v)


def mass_estimate(env, density=1.18):
    """density 1.18 g/cm3 = typical SLA resin; PLA ~1.24, PA12 MJF ~1.01."""
    shell = (env["outer_v"] - env["inner_v"]) * density * 0.92  # 8% for window/button cut-outs
    parts = {
        "shell": shell,
        "4x e-paper panels (glass ~1.19 cm3 x 2.5 g/cm3)": 4 * 3.0,
        "4x cover windows (PMMA 31x31x0.8)": 4 * 0.9,
        "main PCB + module + parts": 8.5,
        "dock-pad PCB": 1.5,
        "LRA": 1.5,
        "4x N52 magnets 6x2": 4 * 0.42,
        "button caps, light pipe": 2.0,
        "screws, FPCs, foam, tape": 4.0,
        "internal ribs, panel frames, bosses (25% of shell, ASSUMPTION)": shell * 0.25,
        "battery": env["battery"][5] if env["battery"] else 0.0,
    }
    return parts, sum(parts.values())


# ----------------------------------------------------------------------------
# 2. Power model
# ----------------------------------------------------------------------------
# Currents at the 3.3 V rail unless noted (mA). Datasheet values cited in docs.
V_RAIL, V_BAT_NOM = 3.3, 3.7
EFF_BB_ACTIVE, EFF_BB_LIGHT = 0.90, 0.80   # TPS63802 (ASSUMPTION from eff. curves; verify on bench)
IQ_BATT_DIRECT_UA = {                      # parts on VBAT/VSYS directly (uA)
    "BQ25180 IQ_BAT (battery only)": 3.5,   # DS: 3 typ (I2C/PB disabled) .. 4 typ
    "TPS63802 IQ": 11.0,
    "DRV2605L shutdown (EN low, on VSYS)": 4.0,
    "MAX17048 hibernate": 3.0,
}
RAIL_SLEEP_UA = {
    "ESP32-S3 light sleep w/ 32k XTAL (ESP-IDF power_save)": 230.0,
    "2 MB quad PSRAM in light sleep (DS note)": 40.0,
    "BMI270 accel low-power + any-motion (ASSUMPTION 25 uA; DS 'down to 4 uA' accel-only)": 25.0,
    "SSD1681 x4 (gated off by TPS22916, 10 nA each)": 0.04,
    "mic rail gated off": 0.01,
}
BLE_CONN_EXTRA_MA = {"optimistic": 0.25, "nominal": 0.55, "pessimistic": 2.0}  # avg add-on for keeping a BLE link (ASSUMPTION)

ACTIVE_MA = {
    "cpu160_single": 40.0,     # DS table 5-9: 160 MHz single core 32-bit 39.9 mA typ1
    "ble_stream_avg": 45.0,    # ASSUMPTION: avg of 176 mA TX peaks @0 dBm at ~25% duty during audio upload
    "mic_i2s": 0.55,           # ICS-43434 550 uA (DK parametric)
    "mic_pdm": 0.98,           # IM69D130 ~980 uA (ASSUMPTION from Infineon DS, verify)
    "epd_refresh": 8.0,        # 26.4 mW / 3.3 V per panel during refresh (Waveshare spec)
    "wifi_avg": 120.0,         # ASSUMPTION: mixed RX 88 mA / TX 340 mA peak bursts
    "haptic_lra": 110.0,       # VG1030001XH max 135 mArms at 2.0 Vrms; DRV2605L Iq 0.5 mA
}


def battery_ma(rail_ma, eff):
    return rail_ma * V_RAIL / (V_BAT_NOM * eff)


def standby_ma(case="nominal"):
    rail = sum(RAIL_SLEEP_UA.values()) / 1000.0 + BLE_CONN_EXTRA_MA[case]
    direct = sum(IQ_BATT_DIRECT_UA.values()) / 1000.0
    return battery_ma(rail, EFF_BB_LIGHT) + direct


def event_mah(rail_ma, seconds, eff=EFF_BB_ACTIVE):
    return battery_ma(rail_ma, eff) * seconds / 3600.0


SCENARIOS = {
    # counts per 24 h
    "A pocket standby": dict(ptt=0, ptt_s=0, faces=0, status=0, timer_min=0, haptics=0, wifi_s=0, ble="nominal"),
    "B normal day": dict(ptt=20, ptt_s=8, faces=40, status=30, timer_min=120, haptics=40, wifi_s=0, ble="nominal"),
    "B' normal day, pessimistic BLE link": dict(ptt=20, ptt_s=8, faces=40, status=30, timer_min=120, haptics=40, wifi_s=0, ble="pessimistic"),
    "C heavy day": dict(ptt=60, ptt_s=12, faces=150, status=100, timer_min=360, haptics=150, wifi_s=300, ble="pessimistic"),
}


def scenario_mah(s, mic="mic_pdm"):
    ptt = event_mah(ACTIVE_MA["cpu160_single"] + ACTIVE_MA["ble_stream_avg"] + ACTIVE_MA[mic], s["ptt_s"]) * s["ptt"]
    # each PTT also: response display refresh (0.3 s panel + 0.6 s CPU awake) - counted in status
    refresh_one = event_mah(ACTIVE_MA["epd_refresh"], 0.3) + event_mah(ACTIVE_MA["cpu160_single"], 0.6)
    faces = refresh_one * 2 * s["faces"]          # old face -> label, new face -> status
    status = refresh_one * s["status"]
    timer = refresh_one * s["timer_min"]
    haptic = event_mah(ACTIVE_MA["haptic_lra"] + ACTIVE_MA["cpu160_single"], 0.25) * s["haptics"]
    wifi = event_mah(ACTIVE_MA["wifi_avg"], s["wifi_s"])
    standby = standby_ma(s["ble"]) * 24.0
    parts = dict(standby=standby, ptt=ptt, faces=faces, status=status, timer=timer, haptic=haptic, wifi=wifi)
    return parts, sum(parts.values())


USABLE = 0.85  # usable fraction of nameplate (cut-off 3.3-3.4 V system, ageing, cold) ASSUMPTION

# ----------------------------------------------------------------------------
# 3. BOM / cost model
# ----------------------------------------------------------------------------
CHECKED = "2026-10-05"
DK = "Digi-Key México"
DK_URL = "https://www.digikey.com.mx/es/products/result?keywords="

# fields: id, phase, req, category, component, mfr, mpn, sku, qty, unit, cur, stock, vendor, url, ds, alt, why, price_status
BOM = [
    # ---------------- Reusable development hardware (Phase A tooling) ----------------
    ("R1", "A-tool", "Required", "Dev board", "ESP32-S3 Feather, 4 MB flash / 2 MB quad PSRAM, MAX17048 + LiPo charger on board",
     "Adafruit", "5477", "1528-5477-ND", 2, 17.50, "USD", "328", DK, DK_URL + "1528-5477-ND",
     "https://learn.adafruit.com/adafruit-esp32-s3-feather",
     "Espressif ESP32-S3-DevKitC-1-N8R8 (0 stock at DK MX on 2026-10-05; check Mouser MX)",
     "Same 2 MB quad-PSRAM class as the Phase B module; battery charger + fuel gauge on board; every Espressif DevKitC-1 variant is 0-stock/obsolete at DK MX", "verified"),
    ("R2", "A-tool", "Required*", "Test equipment", "Power Profiler Kit II (source/ammeter, 200 nA–1 A)",
     "Nordic Semiconductor", "NRF-PPK2", "1490-NRF-PPK2-ND", 1, 113.74, "USD", "1336", DK, DK_URL + "1490-NRF-PPK2-ND",
     "https://www.nordicsemi.com/Products/Development-hardware/Power-Profiler-Kit-2",
     "Borrow lab Joulescope/Otii/PPK2; INA228 breakout is too slow for BLE bursts",
     "*Skip if the university lab lends an equivalent. Only tool that can validate the µA standby budget", "verified"),
    ("R3", "A-tool", "Required", "Cable", "STEMMA QT / Qwiic JST-SH 4-pin cable 100 mm",
     "Adafruit", "4210", "1528-4210-ND", 6, 0.95, "USD", "19592", DK, DK_URL + "1528-4210-ND",
     "https://www.adafruit.com/product/4210", "SparkFun PRT-14427", "Solder-free I2C daisy chain IMU/haptic/ALS", "verified"),
    ("R4", "A-tool", "Required", "Prototyping", "Breadboard 830-pt x2 + M-M/M-F jumper kit",
     "generic", "—", "—", 1, 250.0, "MXN", "local", "Mercado Libre / UNIT / Steren", "https://listado.mercadolibre.com.mx/protoboard-830-puntos",
     "—", "Any local shop", "Bench wiring", "estimate"),
    ("R5", "A-tool", "Required", "Cable", "USB-C data cable 1 m",
     "generic", "—", "—", 2, 90.0, "MXN", "local", "Mercado Libre / Amazon MX", "https://listado.mercadolibre.com.mx/cable-usb-c-datos",
     "—", "—", "Flashing/USB-Serial-JTAG; must be data-capable", "estimate"),
    ("R6", "A-tool", "Optional", "Test equipment", "8-ch 24 MHz USB logic analyzer (sigrok fx2lafw)",
     "generic", "—", "—", 1, 250.0, "MXN", "local", "Mercado Libre / Amazon MX", "https://listado.mercadolibre.com.mx/analizador-logico-8-canales-24mhz",
     "https://sigrok.org/wiki/Fx2lafw", "Lab scope", "Debug 4-panel SPI bus / I2S timing", "estimate"),

    # ---------------- Phase A consumed electronics ----------------
    ("A1", "A", "Required", "Display", "1.54in e-Paper Module 200x200 B/W (SSD1681, partial refresh 0.3 s)",
     "Waveshare", "1.54inch e-Paper Module", "12955", 4, 9.99, "USD", "available", "Waveshare (official)",
     "https://www.waveshare.com/1.54inch-e-paper-module.htm",
     "https://www.waveshare.com/wiki/1.54inch_e-Paper_Module_Manual",
     "RobotShop 'Módulo e-Paper 1,54in 200x200' (USD 11.99); Good Display GDEY0154D67 + DESPI-C02",
     "Bistable, 0 W hold, 170° view; same SSD1681 panel family as Phase B raw panel. Not stocked by DK MX", "verified"),
    ("A2", "A", "Required", "IMU", "6DoF IMU breakout BMI270 (Qwiic)",
     "SparkFun", "22397", "1568-22397-ND", 1, 18.50, "USD", "259", DK, DK_URL + "1568-22397-ND",
     "https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmi270-ds000.pdf",
     "SparkFun 21325 (LSM6DSV16X, USD 24.54)", "Same IMU as Phase B; 4 µA accel-only LP, any/no-motion, step counter", "verified"),
    ("A3", "A", "Required", "Audio", "I2S MEMS microphone breakout (ICS-43434)",
     "Adafruit", "6049", "1528-6049-ND", 1, 8.95, "USD", "1282", DK, DK_URL + "1528-6049-ND",
     "https://invensense.tdk.com/products/ics-43434/",
     "INMP441 module (Amazon MX, legacy part)", "Fastest path to working PTT audio on ESP32-S3 I2S std mode", "verified"),
    ("A4", "A", "Recommended", "Audio", "PDM MEMS microphone breakout (MP34DT01-M)",
     "Adafruit", "3492", "1528-2521-ND", 1, 4.95, "USD", "756", DK, DK_URL + "1528-2521-ND",
     "https://www.adafruit.com/product/3492", "—",
     "Validates ESP32-S3 PDM-RX path planned for Phase B (IM69D130); A/B against I2S", "verified"),
    ("A5", "A", "Required", "Haptics", "DRV2605L haptic driver breakout (STEMMA QT)",
     "Adafruit", "2305", "1528-1346-ND", 1, 7.95, "USD", "1571", DK, DK_URL + "1528-1346-ND",
     "https://www.ti.com/lit/ds/symlink/drv2605l.pdf", "SparkFun 14538 (USD 11.95, 187 stock)",
     "Same driver as Phase B; LRA auto-resonance + 123-effect ROM library", "verified"),
    ("A6", "A", "Required", "Haptics", "LRA coin 10 mm, 210 Hz, 2.0 G (100 g jig), wire leads",
     "Vybronics", "VG1030001XH", "1670-VG1030001XH-ND", 2, 3.22, "USD", "465", DK, DK_URL + "1670-VG1030001XH-ND",
     "https://www.vybronics.com/wp-content/uploads/datasheet-files/Vybronics-VG1030001XH-datasheet.pdf",
     "Vybronics VG0832012 (8 mm, 1 G, USD 3.21)", "Rated on ~100 g jig = cube mass; wire leads work on bench and in Phase B", "verified"),
    ("A7", "A", "Recommended", "Haptics", "ERM vibration disc 10 mm (comparison only)",
     "Adafruit", "1201", "1528-1177-ND", 1, 1.95, "USD", "3719", DK, DK_URL + "1528-1177-ND",
     "https://www.adafruit.com/product/1201", "—", "Blind A/B feel test LRA vs ERM before locking D-007", "verified"),
    ("A8", "A", "Required", "Battery", "LiPo 1S 803040 1000 mAh, PCM, 2-pin (verify JST-PH 2.0 polarity!)",
     "Dataproducts", "DP-80304", "DP-80304", 1, 177.0, "MXN", "5", "Cyberpuerta",
     "https://www.cyberpuerta.mx/Computo-Hardware/Componentes/Placas-de-Desarrollo/Energia-para-Placas-de-Desarrollo/Dataproducts-Bateria-LiPo-3-7V-1000mAh.html",
     "—", "Mercado Libre 'Bateria Lipo 3.7v 1000 mAh' listings MXN 149–416",
     "Geometry candidate for 55x55x42; lithium cells are hazmat for US import — buy locally. +MXN 128 shipping", "verified"),
    ("A9", "A", "Recommended", "Battery", "LiPo 1S ~600–700 mAh, 30x35–40 footprint, ≤6–8 mm, PCM",
     "generic", "603040 / 802535 class", "—", 1, 160.0, "MXN", "local", "UNIT Electronics (802535 650 mAh) / Mercado Libre",
     "https://uelectronics.com/producto/bateria-lipo-3-7v-650mah-802535/", "—", "Adafruit 1578 (500 mAh 29x36x4.75)",
     "Tests whether a smaller cell meets runtime target (enables 52 mm body)", "estimate"),
    ("A10", "A", "Required", "Input", "Tact switch 5.2x5.2 mm 260 gf 0.25 mm travel (Phase B candidate, feel test)",
     "C&K", "PTS526 SK15 SMTR2 LFS", "CKN12221-1-ND", 10, 0.16, "USD", "203592", DK, DK_URL + "PTS526SK15SMTR2LFS",
     "https://www.ckswitches.com/media/1475/pts526.pdf", "Alps SKRP series", "High force + short travel resists pocket presses", "verified"),
    ("A11", "A", "Required", "Input", "12 mm tact switches with caps (bench PTT)",
     "generic", "—", "—", 1, 60.0, "MXN", "local", "Mercado Libre / UNIT / Steren", "https://listado.mercadolibre.com.mx/push-button-12mm", "—", "—",
     "Breadboard-friendly PTT/secondary buttons", "estimate"),
    ("A12", "A", "Recommended", "Dock", "Spring-loaded pogo pin, 0.137in, 2 A, 1M cycles (dock prototype)",
     "Mill-Max", "0906-0-15-20-76-14-11-0", "DK product 1147048", 8, 0.81, "USD", "50282", DK,
     DK_URL + "0906-0-15-20-76-14-11-0", "https://www.mill-max.com/", "Mill-Max 0906-1-15-20-75-14-11-0 (0.177in)",
     "Early wear/alignment test of concentric-ring dock contacts", "verified"),
    ("A13", "A", "Optional", "Sensor", "Ambient light sensor VEML7700 breakout (pocket-detect experiment)",
     "Adafruit", "4162", "1528-2891-ND", 1, 4.95, "USD", "396", DK, DK_URL + "1528-2891-ND",
     "https://www.vishay.com/docs/84286/veml7700.pdf", "LTR-303ALS-01 breakout",
     "Only if PTT false-trigger tests justify a light sensor (D-009)", "verified"),
    ("A14", "A", "Optional", "Display", "Sharp Memory LCD 1.3in 168x144 breakout (fast reflective comparison)",
     "Adafruit", "3502", "—", 1, 24.95, "USD", "unknown", "adafruit.com (not on DK MX)", "https://www.adafruit.com/product/3502",
     "https://www.sharpsde.com/", "Sharp LS013B7DH03 raw panel (DK 425-2903-ND, USD 12.39, 27,094 stock)",
     "Only if e-paper latency/ghosting fails Test 3 acceptance", "verified"),

    # ---------------- Phase B integrated electronics (per unit unless 'batch') ----------------
    ("B1", "B", "Required", "MCU", "ESP32-S3 module, 16 MB flash, 2 MB quad PSRAM, PCB antenna",
     "Espressif", "ESP32-S3-WROOM-1-N16R2", "5407-ESP32-S3-WROOM-1-N16R2CT-ND", 1, 6.70, "USD", "7110", DK,
     DK_URL + "ESP32-S3-WROOM-1-N16R2",
     "https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf",
     "ESP32-S3-MINI-1-N4R2 (USD 5.37, 106 stock, 15.4x20.5x2.4); WROOM-1U-N16R2 + flex antenna for 52x52x38",
     "Certified RF module; quad PSRAM keeps GPIO35–37 free; N8R2 is 0-stock until 2027", "verified"),
    ("B2", "B", "Required", "Display", "1.54in e-paper raw panel 200x200 (SSD1681), 24-pin FPC",
     "Waveshare / Good Display", "1.54inch e-Paper (raw) / GDEY0154D67", "12561", 5, 5.99, "USD", "available",
     "Waveshare (official)", "https://www.waveshare.com/1.54inch-e-paper.htm",
     "https://www.good-display.com/product/388.html", "Good Display direct (buy-lcd.com quote)",
     "4 + 1 spare; 31.8x37.32x1.05 outline", "verified"),
    ("B3", "B", "Required", "Connector", "FPC connector 24-pos 0.5 mm bottom-contact R/A",
     "Hirose", "FH12-24S-0.5SH(55)", "HFJ124CT-ND", 4, 2.41, "USD", "15204", DK, DK_URL + "HFJ124CT-ND",
     "https://www.hirose.com/product/series/FH12", "JLC-stocked 0.5 mm 24P FPC (≈USD 0.10–0.30)", "One per panel", "verified"),
    ("B4", "B", "Required", "Display", "E-paper booster set per panel (MOSFET, 3 Schottky, 10 µH, ~10 caps/res)",
     "various", "per Good Display ref. circuit", "—", 4, 1.50, "USD", "JLC basic/ext", "JLCPCB parts", "https://jlcpcb.com/parts",
     "https://www.good-display.com/product/388.html", "—", "SSD1681 needs external boost parts per panel", "estimate"),
    ("B5", "B", "Required", "IMU", "6-axis IMU, LGA-14 2.5x3x0.83",
     "Bosch Sensortec", "BMI270", "828-1091-1-ND", 1, 4.23, "USD", "52386", DK, DK_URL + "828-1091-1-ND",
     "https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmi270-ds000.pdf",
     "BMI323 (USD 3.91, 31,554 stock; native orientation/tap, but 15 µA suspend)", "Lowest always-on accel current", "verified"),
    ("B6", "B", "Required", "Audio", "PDM MEMS mic, 69 dB SNR, 1.62–3.6 V, bottom port",
     "Infineon", "IM69D130V01XTSA1", "IM69D130V01XTSA1", 1, 2.66, "USD", "in stock (qty not shown)", DK,
     DK_URL + "IM69D130V01XTSA1", "https://www.infineon.com/cms/en/product/sensor/mems-microphones/",
     "ICS-43434 (I2S, OBSOLETE — 94,290 last-time stock); TDK T5838 (1.8 V only)", "Active part that runs on 3.3 V", "verified"),
    ("B7", "B", "Required", "Haptics", "Haptic driver ERM/LRA, I2C, 10-VSSOP",
     "Texas Instruments", "DRV2605LDGSR", "296-40032-1-ND", 1, 2.28, "USD", "4661", DK, DK_URL + "296-40032-1-ND",
     "https://www.ti.com/lit/ds/symlink/drv2605l.pdf", "Renesas DA7280", "Auto-resonance, overdrive/brake, effect ROM", "verified"),
    ("B8", "B", "Required", "Haptics", "LRA 10 mm 210 Hz (same as A6)",
     "Vybronics", "VG1030001XH", "1670-VG1030001XH-ND", 1, 3.22, "USD", "465", DK, DK_URL + "1670-VG1030001XH-ND",
     "https://www.vybronics.com/wp-content/uploads/datasheet-files/Vybronics-VG1030001XH-datasheet.pdf",
     "VG1040003D (2 G, 170 Hz, pressure contacts, USD 6.50)", "—", "verified"),
    ("B9", "B", "Required", "Power", "1-cell 1 A linear charger, power path, I2C, ship mode 3.2 µA",
     "Texas Instruments", "BQ25180YBGR", "296-BQ25180YBGRCT-ND", 1, 3.01, "USD", "3019", DK, DK_URL + "BQ25180YBGR",
     "https://www.ti.com/lit/ds/symlink/bq25180.pdf", "BQ25185 (standalone, WSON 2.2x2); BQ24074RGTR (USD 2.43)",
     "Smallest power-path charger with ship mode + button reset", "verified"),
    ("B10", "B", "Required", "Power", "Fuel gauge ModelGauge, 8-TDFN 2x2",
     "Analog Devices (Maxim)", "MAX17048G+T10", "MAX17048G+T10CT-ND", 1, 4.61, "USD", "24141", DK, DK_URL + "MAX17048G%2BT10",
     "https://www.analog.com/media/en/technical-documentation/data-sheets/MAX17048-MAX17049.pdf",
     "MAX17260 (m5 EZ, needs sense resistor)", "No sense resistor, 3 µA hibernate, same chip as Feather", "verified"),
    ("B11", "B", "Required", "Power", "Buck-boost 3.3 V 2 A, 11 µA Iq, 3x2 VSON",
     "Texas Instruments", "TPS63802DLAR", "296-TPS63802DLARCT-ND", 1, 3.40, "USD", "19575", DK, DK_URL + "TPS63802DLAR",
     "https://www.ti.com/lit/ds/symlink/tps63802.pdf", "LDO (e.g. 300 mV-dropout class) loses the last ~10–15 % of cell",
     "Holds 3.3 V from 4.2 V down to 3.0 V cell with 340 mA Wi-Fi peaks", "verified"),
    ("B12", "B", "Required", "Power", "Load switch 2 A, 10 nA off (display rail, audio rail)",
     "Texas Instruments", "TPS22916CYFPR", "296-50065-1-ND", 2, 0.63, "USD", "20624", DK, DK_URL + "TPS22916CYFPR",
     "https://www.ti.com/lit/ds/symlink/tps22916.pdf", "Si2301 P-FET + gate R", "Hard-off for 4 panels and mic", "verified"),
    ("B13", "B", "Required", "Timing", "32.768 kHz crystal 12.5 pF (GPIO15/16)",
     "Epson", "FC-135 32.7680KA-A3", "FC-135 32.7680KA-A3", 1, 2.66, "USD", "in stock", DK, DK_URL + "FC-135%2032.7680KA-A3",
     "https://www5.epsondevice.com/en/products/crystal_unit/fc135.html", "Abracon ABS07-32.768KHZ",
     "BLE light sleep 230 µA vs 3.3 mA without it (ESP-IDF power_save README)", "verified"),
    ("B14", "B", "Required", "Connector", "USB-C receptacle USB 2.0 16P (internal service port)",
     "GCT", "USB4105-GF-A", "USB4105-GF-A", 1, 0.80, "USD", "in stock", DK, DK_URL + "USB4105-GF-A",
     "https://gct.co/connector/usb4105", "—", "Native USB-Serial/JTAG flashing + charging on the bench", "verified"),
    ("B15", "B", "Required", "Input", "Tact switch PTS526 (PTT, secondary, BOOT)",
     "C&K", "PTS526 SK15 SMTR2 LFS", "CKN12221-1-ND", 3, 0.16, "USD", "203592", DK, DK_URL + "PTS526SK15SMTR2LFS",
     "https://www.ckswitches.com/media/1475/pts526.pdf", "—", "—", "verified"),
    ("B16", "B", "Required", "Protection", "ESD/TVS on dock pads + USB (e.g. TPD4E05U06 + VBUS TVS)",
     "Texas Instruments", "TPD4E05U06 (+ SMF5.0A class TVS)", "—", 1, 1.00, "USD", "JLC/DK", "JLCPCB parts", "https://jlcpcb.com/parts",
     "https://www.ti.com/lit/ds/symlink/tpd4e05u06.pdf", "—", "Exposed pads in a pocket", "estimate"),
    ("B17", "B", "Required", "Passives", "Passives, inductor for TPS63802 (0.47 µH), LED, test pads",
     "various", "—", "—", 1, 4.00, "USD", "JLC basic", "JLCPCB parts", "https://jlcpcb.com/parts", "—", "—", "≈70 placements", "estimate"),
    ("B18", "B", "Required", "Battery", "LiPo 803040 1000 mAh (or 603040 per Test 9 result)",
     "Dataproducts", "DP-80304", "DP-80304", 1, 177.0, "MXN", "5", "Cyberpuerta",
     "https://www.cyberpuerta.mx/Computo-Hardware/Componentes/Placas-de-Desarrollo/Energia-para-Placas-de-Desarrollo/Dataproducts-Bateria-LiPo-3-7V-1000mAh.html",
     "—", "Mercado Libre 1000 mAh listings", "—", "verified"),
    ("B19", "B", "Required", "PCB", "Main PCB 4-layer ~44x44 mm, 1.0 mm, ENIG — 5 pcs (batch)",
     "JLCPCB", "—", "—", 1, 20.0, "USD", "n/a", "JLCPCB", "https://jlcpcb.com/", "—", "PCBWay",
     "Quote live before ordering (JLC price adjustment Aug-2026)", "estimate"),
    ("B20", "B", "Required", "PCB", "Dock-pad PCB (concentric rings, ENIG) + dock PCB, 2-layer — 5 pcs each (batch)",
     "JLCPCB", "—", "—", 1, 10.0, "USD", "n/a", "JLCPCB", "https://jlcpcb.com/", "—", "—", "—", "estimate"),
    ("B21", "B", "Required", "Assembly", "PCBA economic: setup 8 + stencil 1.5 + ~15 extended feeders x3 + joints (batch, 2 boards)",
     "JLCPCB", "—", "—", 1, 58.0, "USD", "n/a", "JLCPCB", "https://jlcpcb.com/help/article/pcb-assembly-price", "—", "Hand assembly at uni lab",
     "Fee schedule from JLC help article", "estimate"),
    ("B22", "B", "Required", "Shipping", "DHL from China for PCB/PCBA (batch)",
     "—", "—", "—", 1, 25.0, "USD", "n/a", "JLCPCB", "https://jlcpcb.com/", "—", "—", "+33.5% MX courier duty (non-FTA origin)", "estimate"),
    ("B23", "B", "Required", "Dock", "Pogo pins for dock (4 rings: VBUS, GND, D+, D−)",
     "Mill-Max", "0906-0-15-20-76-14-11-0", "DK product 1147048", 4, 0.81, "USD", "50282", DK,
     DK_URL + "0906-0-15-20-76-14-11-0", "https://www.mill-max.com/", "—", "Springs live in the dock, flat pads on the cube", "verified"),

    # ---------------- Mechanical / enclosure / dock ----------------
    ("M1", "Mech", "Required", "Mockup", "Pocketability dummy shells x3 sizes + ballast (PLA, uni printer)",
     "—", "—", "—", 1, 150.0, "MXN", "n/a", "university printer / local service", "—", "—", "—", "Filament + washers", "estimate"),
    ("M2", "Mech", "Required", "Enclosure", "SLA resin enclosure (shell + face A cap + face B) x2 iterations",
     "JLC3DP / local SLA", "—", "—", 2, 25.0, "USD", "n/a", "JLC3DP or Mexican SLA service", "https://jlc3dp.com/", "—", "Local MJF/SLA",
     "Two fit iterations expected", "estimate"),
    ("M3", "Mech", "Required", "Enclosure", "Cover windows 31x31x0.8 PMMA (laser cut, 8 pcs)",
     "—", "—", "—", 1, 200.0, "MXN", "n/a", "local laser-cut", "—", "—", "0.55 mm Gorilla-class glass later", "—", "estimate"),
    ("M4", "Mech", "Required", "Dock", "N52 Ø6x2 mm disc magnets (pack of 50)",
     "generic", "—", "—", 1, 180.0, "MXN", "local", "Mercado Libre / Amazon MX", "https://listado.mercadolibre.com.mx/imanes-neodimio-n52-6x2", "—", "—",
     "4 in cube face B + 4 in dock; same polarity -> 90° detents", "estimate"),
    ("M5", "Mech", "Required", "Dock", "Dock body print (PLA/PETG) + rubber feet + M1.6/M2 screws",
     "—", "—", "—", 1, 250.0, "MXN", "n/a", "local", "—", "—", "—", "—", "estimate"),
]


def to_usd(unit, cur):
    return unit if cur == "USD" else unit / FX_MXN_PER_USD


def bom_rows():
    rows = []
    for r in BOM:
        (rid, phase, req, cat, comp, mfr, mpn, sku, qty, unit, cur, stock, vendor, url, ds, alt, why, pstat) = r
        ext = unit * qty
        ext_mxn = ext * (FX_MXN_PER_USD if cur == "USD" else 1.0)
        rows.append(dict(id=rid, phase=phase, required=req, category=cat, component=comp, manufacturer=mfr, mpn=mpn,
                         distributor_sku=sku, qty=qty, unit_price=unit, currency=cur, extended_price=round(ext, 2),
                         extended_mxn=round(ext_mxn, 0), stock=stock, vendor=vendor, purchase_url=url, datasheet_url=ds,
                         alternate=alt, rationale=why, price_status=pstat, price_checked=CHECKED))
    return rows


def subtotal(rows, phase, include=("Required", "Required*", "Recommended", "Optional")):
    return sum(r["extended_mxn"] for r in rows if r["phase"] == phase and r["required"] in include)


# ---- landed-cost assumptions (see research/cost_model.md) ----
TAX_DK = (0.16, 0.25, 0.335)        # min / planning / max on Digi-Key CPT goods (IVA+IGI/tasa global+broker) ASSUMPTION
TAX_CN = 0.335                      # MX courier rate on non-FTA (China) origin since 2025-08-15
SHIP_WAVESHARE_USD = 20.0           # ASSUMPTION; quote at checkout
SHIP_CYBERPUERTA_MXN = 128.0        # verified on listing
CONT_A, CONT_B = 0.15, 0.25         # contingency


def landed(rows, ids, dk_as_jlc=False):
    """Return dict of goods/ship/tax (MXN, planning) for ONE purchase wave (each vendor = one order).
    dk_as_jlc: Phase B ICs bought through JLCPCB/LCSC as part of the PCBA order (taxed as China origin)."""
    sel = [r for r in rows if r["id"] in ids]
    out = dict(goods=0.0, ship=0.0, tax=0.0, tax_min=0.0, tax_max=0.0)
    dk = sum(r["extended_mxn"] for r in sel if r["vendor"] == DK)
    ws = sum(r["extended_mxn"] for r in sel if r["vendor"].startswith("Waveshare"))
    jlc = sum(r["extended_mxn"] for r in sel if r["vendor"].startswith("JLC"))
    if dk_as_jlc:
        jlc, dk = jlc + dk, 0.0
    cp = sum(r["extended_mxn"] for r in sel if r["vendor"] == "Cyberpuerta")
    other = sum(r["extended_mxn"] for r in sel) - dk - ws - jlc - cp
    out["goods"] = dk + ws + jlc + cp + other
    ship_dk = 0.0 if dk / FX_MXN_PER_USD >= 100 else 30 * FX_MXN_PER_USD if dk else 0.0
    ship_ws = SHIP_WAVESHARE_USD * FX_MXN_PER_USD if ws else 0.0
    ship_cp = SHIP_CYBERPUERTA_MXN if cp else 0.0
    out["ship"] = ship_dk + ship_ws + ship_cp           # JLC shipping is its own BOM row (B22)
    cn_base = ws + ship_ws + jlc
    out["tax"] = dk * TAX_DK[1] + cn_base * TAX_CN
    out["tax_min"] = dk * TAX_DK[0] + cn_base * TAX_CN
    out["tax_max"] = dk * TAX_DK[2] + cn_base * TAX_CN
    return out


def cost_summary(rows):
    ids = lambda ph, reqs: {r["id"] for r in rows if r["phase"] == ph and r["required"] in reqs}
    core = ("Required", "Required*", "Recommended")
    print("\n-- landed cost (MXN, planning) --")
    blocks = {
        "Reusable dev hardware (incl. PPK2) [goods only, own block]": (ids("A-tool", core), False),
        "Phase A consumed electronics [goods only, own block]": (ids("A", core), False),
        "PHASE A WAVE (tools + consumed, one order per vendor)": (ids("A-tool", core) | ids("A", core), False),
        "PHASE A WAVE, PPK2 borrowed": ((ids("A-tool", core) | ids("A", core)) - {"R2"}, False),
        "Phase B integrated electronics (first unit, ICs via JLC PCBA)": (ids("B", core), True),
        "Mechanical / enclosure / dock": (ids("Mech", core), False),
    }
    res = {}
    for k, (s, j) in blocks.items():
        L = landed(rows, s, j)
        tot = L["goods"] + L["ship"] + L["tax"]
        res[k] = (L, tot)
        print(f"{k}: goods {L['goods']:,.0f} + ship {L['ship']:,.0f} + tax {L['tax']:,.0f} "
              f"(range {L['tax_min']:,.0f}–{L['tax_max']:,.0f}) = {tot:,.0f}")
    a_full = res["PHASE A WAVE (tools + consumed, one order per vendor)"][1]
    a_bor = res["PHASE A WAVE, PPK2 borrowed"][1]
    print(f"Phase A landed: with PPK2 {a_full:,.0f}  (+{CONT_A:.0%} cont. = {a_full*(1+CONT_A):,.0f}); "
          f"PPK2 borrowed {a_bor:,.0f} (+cont. = {a_bor*(1+CONT_A):,.0f})")
    b = res["Phase B integrated electronics (first unit, ICs via JLC PCBA)"][1]
    m = res["Mechanical / enclosure / dock"][1]
    print(f"Phase B first unit: electronics {b:,.0f} + mech {m:,.0f} = {b+m:,.0f}; +{CONT_B:.0%} = {(b+m)*(1+CONT_B):,.0f}")
    # repeat unit at qty 10 (USD, ASSUMPTION built from qty-10 price breaks)
    rep = dict(module=5.47, panels=4 * 5.6, fpc_jlc=4 * 0.25, boosters=4 * 1.0, imu=3.62, mic=2.2, drv=1.69, lra=3.0,
               chg=2.25, fg=3.50, bb=2.55, ls=0.9, xtal=0.6, usbc=0.5, sw=0.5, esd=0.7, passives=3.0,
               pcb_pcba_share=14.0, battery=177 / FX_MXN_PER_USD * 0.85, enclosure=15.0, windows=3.0, mag_screws=2.0, dock=8.0)
    china = sum(rep[k] for k in ("panels", "fpc_jlc", "boosters", "pcb_pcba_share", "passives", "enclosure"))
    tot = sum(rep.values()) + china * TAX_CN + sum(rep[k] for k in ("module", "imu", "mic", "drv", "lra", "chg", "fg", "bb")) * TAX_DK[1]
    print(f"Repeat unit @10 pcs ≈ USD {tot:,.0f} = MXN {tot*FX_MXN_PER_USD:,.0f} (goods USD {sum(rep.values()):.0f})")


CART_HEADER = """# SHOPPING CART

> Generated by `python3 tools/cube_model.py --cart` from the BOM data in `tools/cube_model.py`.
> **Price checked: {checked}.** Planning FX **{fx} MXN/USD** (Banxico FIX 2026-10-01 = 18.3688 + card spread).
> **Nothing has been ordered.** Shipping and taxes are **not** in the unit prices — see the totals below and
> `bom/COST_BREAKDOWN.md`. `price_status = estimate` rows are not live-verified (marketplace anti-bot or quote-based).
> Digi-Key URLs are keyword searches on the exact Digi-Key part number / MPN (they resolve to the product page).

## How to buy (Phase A = buy now)
1. **Digi-Key MX order** — all `Digi-Key México` rows of Phase A + reusable. If the PPK2 is borrowed, the order is
   ≈ USD 97.5 → **add A13 (VEML7700, USD 4.95) to cross the USD 100 free-shipping line** (cheaper than USD 30 shipping).
2. **Waveshare order** — 4 × #12955 (+ optionally the 5 Phase B raw panels #12561 to share one shipment; they are cheap
   and let the team inspect the FPC tail early).
3. **Local** — Cyberpuerta (cell), Mercado Libre/Amazon MX/UNIT (second cell, breadboard, cables, keys, magnets).
4. Check JST polarity of every cell before connecting it to the Feather.

"""


def md_table(rows):
    cols = ["Category", "Component", "Manufacturer", "Exact MPN", "Distributor SKU", "Qty", "Unit price", "Extended price",
            "Currency", "Stock", "Vendor", "Purchase URL", "Datasheet URL", "Phase", "Required / Optional", "Alternate",
            "Selection rationale", "Price status"]
    out = ["| ID | " + " | ".join(cols) + " |", "|" + "---|" * (len(cols) + 1)]
    for r in rows:
        unit = f"{r['unit_price']:,.2f}"
        ext = f"{r['extended_price']:,.2f}"
        cells = [r["id"], r["category"], r["component"], r["manufacturer"], f"`{r['mpn']}`", r["distributor_sku"], str(r["qty"]),
                 unit, ext, r["currency"], r["stock"], r["vendor"], r["purchase_url"], r["datasheet_url"], r["phase"],
                 r["required"], r["alternate"], r["rationale"], r["price_status"]]
        out.append("| " + " | ".join(c.replace("|", "/") for c in cells) + " |")
    return "\n".join(out)


def write_cart(rows):
    sections = [
        ("1. Reusable development hardware — BUY NOW", "A-tool"),
        ("2. Phase A consumed electronics & bench parts — BUY NOW", "A"),
        ("3. Phase B integrated electronics — PRICE ONLY, order after schematic review", "B"),
        ("4. Mechanical / enclosure / dock", "Mech"),
    ]
    txt = CART_HEADER.format(checked=CHECKED, fx=FX_MXN_PER_USD)
    for title, ph in sections:
        sel = [r for r in rows if r["phase"] == ph]
        txt += f"## {title}\n\n" + md_table(sel) + "\n\n"
        req = sum(r["extended_mxn"] for r in sel if r["required"] in ("Required", "Required*"))
        rec = sum(r["extended_mxn"] for r in sel if r["required"] == "Recommended")
        opt = sum(r["extended_mxn"] for r in sel if r["required"] == "Optional")
        txt += (f"**Goods subtotal (MXN @ {FX_MXN_PER_USD}):** required {req:,.0f} · recommended {rec:,.0f} · "
                f"optional {opt:,.0f}\n\n")
    txt += """## 5. Totals, shipping/tax, contingency (planning)

| Wave | Goods | Shipping | Taxes/duties (planning; range) | Landed | Contingency | **Likely all-in** |
|---|---:|---:|---:|---:|---:|---:|
"""
    core = ("Required", "Required*", "Recommended")
    ids = lambda ph: {r["id"] for r in rows if r["phase"] == ph and r["required"] in core}
    waves = [
        ("Phase A, PPK2 **bought**", ids("A-tool") | ids("A"), False, CONT_A),
        ("Phase A, PPK2 **borrowed** (+A13 to reach free shipping)", (ids("A-tool") | ids("A") | {"A13"}) - {"R2"}, False, CONT_A),
        ("Phase B electronics, first unit (ICs via JLC PCBA)", ids("B"), True, CONT_B),
        ("Mechanical / enclosure / dock", ids("Mech"), False, CONT_B),
    ]
    for name, s, j, c in waves:
        L = landed(rows, s, j)
        tot = L["goods"] + L["ship"] + L["tax"]
        txt += (f"| {name} | {L['goods']:,.0f} | {L['ship']:,.0f} | {L['tax']:,.0f} ({L['tax_min']:,.0f}–{L['tax_max']:,.0f}) | "
                f"{tot:,.0f} | {c:.0%} | **{tot*(1+c):,.0f}** |\n")
    txt += """
Shipping/tax rules: Digi-Key MX free ≥ USD 100 (else USD 30), CPT → taxes on delivery, planning 25 % (16–33.5 %);
Waveshare shipping assumed USD 20 + 33.5 % China-origin courier rate; JLC DHL row included in Phase B goods, +33.5 %;
local MXN prices include IVA. **Unknowns:** exact Waveshare shipping, DK courier brokerage fee, marketplace prices.
"""
    path = os.path.join(ROOT, "bom", "SHOPPING_CART.md")
    with open(path, "w") as f:
        f.write(txt)
    print(f"wrote {path}")


def main():
    print(f"FX planning rate: {FX_MXN_PER_USD} MXN/USD\n")
    print("== 1. Size envelopes ==")
    print(f"display stack depth = {DISPLAY_DEPTH:.2f} mm; face A stack {FACE_A_STACK:.1f}; face B stack {FACE_B_STACK:.1f}")
    for W, D, H in ENVELOPES:
        for flex in (False, True):
            e = envelope(W, D, H, flex)
            parts, m = mass_estimate(e)
            # recommended cell = 803040 when it fits, else largest that fits
            rec = next((bb for bb in BATTERIES if bb[0].startswith("803040")), None)
            e2 = dict(e); e2["battery"] = rec if (e["battery"] and BATTERIES.index(e["battery"]) <= 1) else e["battery"]
            _, m_rec = mass_estimate(e2)
            b = e["battery"][0] if e["battery"] else "NONE"
            print(f"{W}x{D}x{H} flexAnt={flex!s:5} outerV={e['outer_v']:.0f}cm3 core={e['core']:.1f} axial={e['axial']:.1f} "
                  f"panelW={e['panel_fit_w']} panelH={e['panel_fit_h']} (minH {e['min_h_panel']:.1f}/{e['min_h_antenna']:.1f}) "
                  f"maxbatt={b} mass(max cell)≈{m:.0f} g mass(803040)≈{m_rec:.0f} g (shell {parts['shell']:.0f})")
    print("\nreference objects:")
    for n, d, m, s in REFERENCE_OBJECTS:
        v = d[0] * d[1] * d[2] / 1000
        print(f"  {n}: {d} vol={v:.0f} cm3 mass={m} g density={m/v:.2f} g/cm3 thick={min(d)}")

    print("\n== 2. Power ==")
    for c in BLE_CONN_EXTRA_MA:
        print(f"standby ({c}) = {standby_ma(c):.3f} mA from battery")
    for name, s in SCENARIOS.items():
        parts, tot = scenario_mah(s)
        print(f"{name}: {tot:.1f} mAh/day  " + ", ".join(f"{k}={v:.1f}" for k, v in parts.items()))
        for cap in (500, 700, 1000, 1200):
            print(f"     {cap} mAh -> {cap * USABLE / tot:.1f} days")
    # docked
    sys_ma = 30.0  # Wi-Fi modem-sleep avg + display duty (ASSUMPTION)
    ichg = 400
    print(f"Docked: system ≈{sys_ma} mA@3.3V + charge {ichg} mA -> charger loss at VBAT 3.6 V: {(5.0-3.6)*(ichg/1000)+ (5.0-4.5)*(sys_ma*3.3/4.5/1000):.2f} W")

    print("\n== 3. Cost ==")
    rows = bom_rows()
    for ph in ("A-tool", "A", "B", "Mech"):
        req = subtotal(rows, ph, ("Required", "Required*"))
        rec = subtotal(rows, ph, ("Recommended",))
        opt = subtotal(rows, ph, ("Optional",))
        print(f"{ph}: required {req:,.0f}  recommended {rec:,.0f}  optional {opt:,.0f}  MXN")
    disp_a = sum(r["extended_mxn"] for r in rows if r["id"] == "A1")
    cons_a = subtotal(rows, "A", ("Required", "Recommended"))
    disp_b = sum(r["extended_mxn"] for r in rows if r["id"] in ("B2", "B3", "B4")) - 5.99 * FX_MXN_PER_USD  # exclude spare
    comp_b = sum(r["extended_mxn"] for r in rows if r["phase"] == "B" and r["id"] not in ("B19", "B20", "B21", "B22"))
    print(f"display share Phase A consumed: {disp_a:,.0f}/{cons_a:,.0f} = {100*disp_a/cons_a:.0f}%")
    print(f"display share Phase B components: {disp_b:,.0f}/{comp_b:,.0f} = {100*disp_b/comp_b:.0f}%")
    cost_summary(rows)

    if "--cart" in sys.argv:
        write_cart(rows)

    if "--csv" in sys.argv:
        path = os.path.join(ROOT, "bom", "BOM.csv")
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
