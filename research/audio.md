# Research — Audio (push-to-talk capture)

Checked 2026-10-05. Decision: D-008.

## 1. Requirements
PTT only (hold → speak → release). Near-field speech, 10–40 cm, often handheld; sometimes from a
pocket-adjacent position (user lifts the cube). 16 kHz mono is enough for cloud STT. No wake word,
no always-on recording in V1.

## 2. I2S vs PDM on ESP32-S3

| | I2S MEMS | PDM MEMS |
|---|---|---|
| ESP32-S3 support | I2S standard RX | **Hardware PDM-RX → PCM** (I2S0) |
| Pins | 3 (BCLK, WS, SD) | **2 (CLK, DATA)** |
| Mic contains | ADC + decimation | modulator only (decimation in the S3) |
| Robustness over a flex/long trace | good | clock 1–3.2 MHz, fine over ≤ 50 mm |
| Part availability | ICS-43434 **obsolete** (DK last-time stock 94,290); SPH0645 has an ESP32 timing quirk | wide: Infineon IM69D130, TDK T5837/T5838 (1.8 V only), Knowles |

**Best architecture for Phase B: PDM** (2 pins, active parts, native S3 support).
**Phase A uses the I2S breakout** (#6049, in stock, fastest bring-up) **plus** a cheap PDM breakout
(#3492, MP34DT01-M) to validate the PDM path before committing the PCB.

## 3. Candidate mics

| Part | IF | SNR | Sens. | Supply | Current | Size | DK MX |
|---|---|---|---|---|---|---|---|
| ICS-43434 | I2S | 64–65 dB | −26 dBFS | 1.65–3.63 V | 550 µA | 3.5 × 2.65 × 0.98, bottom | USD 3.92, **obsolete** |
| **IM69D130** ✅ | PDM | 69 dB(A) | −36 dBFS | **1.62–3.6 V** | ~980 µA (verify) | 4 × 3 × 1.2, bottom | USD 2.66 |
| TDK T5838 (MMICT5838-00-012) | PDM | 68 dB | −41 dBFS | **1.65–1.98 V only** | 330 µA | 3.5 × 2.65 × 1.11 | USD 2.83, 67,466 |
| TDK T5837 (MMICT5837-00-012) | PDM | 68 dB | −36 dBFS | 1.65–1.98 V only | 340 µA | 3.5 × 2.65 × 1.11 | USD 2.76, 5,811 |
| ST MP34DT06J | PDM | 64 dB | −26 dBFS | 1.8 V | 650 µA | 3 × 4 × 1.1 top | **obsolete** |

IM69D130 is chosen because it runs straight from 3.3 V (no extra 1.8 V rail, no level shifters).
Its higher current is irrelevant: the mic rail is gated and only on during PTT (~8 s × 20/day).

## 4. Is one microphone enough? — Yes for V1
Near-field PTT with a user-initiated window gives high SNR without beamforming. A 2-mic array helps
far-field and noise suppression, which V1 explicitly does not target. Keep a second-mic footprint?
**No** — pins are at 34/36; revisit in V2 with T5838 + 1.8 V rail.

## 5. Acoustic design
- Bottom-port mic on the main PCB under face A; **acoustic port Ø0.8–1.0 mm** through PCB, sealed
  to the enclosure with a gasket (die-cut foam or PSA ring) so sound enters only through the port.
- Hydrophobic acoustic mesh (Saati/GORE-type) over the port: dust and lint from pockets.
- Port on face A, near the PTT key but offset ≥ 10 mm so the thumb does not cover it.
- Keep the mic ≥ 15 mm from the LRA; never record during haptic playback (mask 150 ms).

## 6. Noise risks
- **Rubbing / handling noise** (thumb on face A, fabric): mitigate with the gasket, a recessed port,
  a high-pass filter (~100 Hz) and start-of-PTT trimming (~80 ms click of the key).
- **Wind**: mesh + small port helps; V1 accepts degradation outdoors.
- **Pocket**: no capture happens in the pocket (PTT requires deliberate hold; see risk R-21).
- **Key click**: the PTS526 actuation click couples into the mic — trim first/last 80 ms.

## 7. Streaming
PCM 16 kHz/16-bit = 256 kbps — too much for reliable iOS BLE throughput. Encode **Opus ~16–24 kbps**
(or IMA-ADPCM 64 kbps as a simpler fallback) on the S3 and stream over a GATT notify characteristic
to the phone app. PSRAM buffers the utterance if the link stalls.
