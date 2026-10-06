# Research — IMU

Checked 2026-10-05. Decision: D-006.

## 1. Requirements
Reliable up-face detection among 4 faces, rotation/pickup/motion, low-power interrupts that wake
the MCU from deep sleep. Nice-to-have: tap, steps, activity. **No magnetometer** (dock magnets would
corrupt it, and heading is not needed).

## 2. Comparison

| | **BMI270** ✅ | **BMI323** | **ICM-42688-P** | **LSM6DSV16X** |
|---|---|---|---|---|
| Vendor | Bosch | Bosch | TDK InvenSense | ST |
| Full 6-axis current | 685 µA (DS) | 790 µA HP (DS T.10) | 0.88 mA LN (TDK) | 0.65 mA HP combo (ST) |
| Accel-only low power | **"down to 4 µA"** | 45 µA | WoM low-power (value not verified) | LPM1 (forum: ~70 µA avg in one report) |
| Suspend / power-down | **3.5 µA** | 15 µA | — | — |
| Orientation interrupt | No (MCU computes) | **Yes: orientation + flat** | No | **Yes: 6D/4D** |
| Any/no-motion, sig. motion | Yes | Yes | WoM, SMD | Yes |
| Tap | No | Yes (single/double/triple) | Yes (APEX) | Yes |
| Step counter | Yes | Yes | Yes (APEX) | Yes |
| Extras | activity recognition, wrist gestures | tilt | high-performance gyro, I3C | MLC, FSM, SFLP sensor fusion |
| Package | LGA-14 2.5 × 3 × 0.8 | LGA-14 2.5 × 3 × 0.83 | LGA-14 2.5 × 3 × 0.91 | LGA-14 2.5 × 3 × 0.83 |
| DK MX price / stock | **USD 4.23 / 52,386** | USD 3.91 / 31,554 | USD 4.86 / in stock | USD 5.75 / **0** |
| Breakout | SparkFun 22397 USD 18.50 (259) | none found at DK | various | SparkFun 21325 USD 24.54 (89) |
| Libraries | Bosch SensorAPI, ESP-IDF `espp/bmi270`, SparkFun Arduino | Bosch SensorAPI | TDK driver, community | ST STdC drivers |
| Documentation | very good | very good | good | very good |

## 3. Recommendation: BMI270
- Lowest always-on current — the IMU is the one sensor that is *always* on in Pocket Mode.
- Face classification in firmware is trivial and tunable: on any-motion → wake → read gravity
  vector at 25–50 Hz → when no-motion fires (stationary ≥ 0.5–1 s) pick the axis with |g| > 0.8 g
  with ≥ 15° hysteresis → update context. This is more controllable than a vendor 6D engine for a
  cube with non-standard axes.
- Pickup = any-motion while previous state was stationary-on-desk.
- Steps / activity come for free from the BMI270 config file.

**Mounting:** IMU Z axis parallel to the rotation axis; ±X/±Y map to the four display faces. Rigidly
on the main PCB, away from the LRA (haptic events will trip any-motion — firmware must mask
motion interrupts for ~150 ms around haptic playback).

## 4. Backups
- **BMI323** if the firmware approach is flaky (native orientation + tap) at +11 µA suspend.
- **LSM6DSV16X** if the MLC is wanted for desk/pocket classification and stock returns.
