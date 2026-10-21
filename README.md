# beepdb 🔊
### The Open Database of Hardware Acoustic Signatures & Diagnostic Beep Codes

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Data: CC-BY 4.0](https://img.shields.io/badge/Data-CC--BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

> *"A growing, sourced library — cadence patterns mapped and cited from manufacturer documentation, with frequencies modeled on nominal component resonance and calibrated against physical acoustic recordings."*

It's 3:14 AM and something in the house is chirping. Is it carbon monoxide end-of-life? A smoke detector low battery? A freezer temperature alert? 

Historically, hardware error beeps have remained locked inside obscure PDF manuals. While manuals document chirp timing (e.g. "chirps once every 30 seconds"), they rarely document acoustic peak frequencies, and physical piezos exhibit drift. **`beepdb`** is an open-source, machine-readable dataset, reference audio corpus, and zero-dependency Python library providing deterministic acoustic signatures mapping hardware chirp cadences and frequency tolerance bands to their underlying failure modes, device identity, urgency, and remedy workflows.

Developed as an open-source contribution for the **Amazon Developer Hackathon 2026**, powering **[GENIUS — The Home World Model MCP Server](https://github.com/patriceai-code/genius)**.

---

## Installation

```bash
pip install git+https://github.com/patriceai-code/beepdb.git
```

---

## Quickstart

### 1. Python API (Acoustic Feature Matching & Conversational Description Matching)
```python
from beepdb import match_beep, match_description, search_signatures

# 1. Identify device by physical acoustic features (cadence + FFT peak + pulse duration)
match = match_beep(interval_s=30.0, peak_freq_hz=3200.0, duration_ms=80.0)
print(f"Device: {match['brand']} {match['device_class']} -> {match['meaning']} ({match['severity']})")

# 2. Identify device from spoken conversational description (no raw audio required)
voice_match = match_description(interval_s=30.0, brand="Kidde", pitch="high")
print(f"Voice Match: {voice_match['brand']} ({voice_match['confidence'] * 100:.0f}% confidence)")
```

### 2. Command-Line Interface (CLI)
```bash
# Query by observed resonant frequency and chirp interval (or --cadence)
beepdb match --freq 3200 --interval 30.0

# Query by spoken conversational description (interval + optional brand)
beepdb describe --interval 30 --brand Kidde

# Inspect bundled CC0/CC-BY physical piezo & ESC-50 reference audio corpus
beepdb corpus

# Search all Kidde hardware in the database
beepdb list --brand Kidde
```

---

## Seed Library (20 Sourced Devices)

| Brand | Model / Series | Device Category | Cadence | Peak Frequency | Tolerance | Meaning | Severity |
|---|---|---|---|---|---|---|---|
| **Kidde** | KN-COPP-3 | CO Detector | 30s | 3,200 Hz | ±350 Hz | End-of-Life | Critical |
| **First Alert** | CO605 | CO Detector | 60s | 3,400 Hz | ±350 Hz | End-of-Life | Critical |
| **First Alert** | BRK-9120B | Smoke Detector | 45s | 4,000 Hz | ±400 Hz | Low Battery | Warning |
| **Kidde** | i9010 | Smoke Detector | 30s | 3,368 Hz* | ±350 Hz | Low Battery | Warning |
| **Google Nest** | Protect (Battery) | Smoke/CO | 60s | 3,000 Hz | ±350 Hz | Low Battery | Warning |
| **Google Nest** | Protect (Sensor) | Smoke/CO | 30s | 3,000 Hz | ±350 Hz | Sensor Failure | Critical |
| **X-Sense** | SC01 Combo | Smoke/CO | 60s | 3,321 Hz* | ±350 Hz | End-of-Life | Critical |
| **X-Sense** | SD03 | Smoke Detector | 60s | 3,800 Hz | ±350 Hz | Low Battery | Warning |
| **Honeywell** | R200C | CO Alarm | 40s | 3,200 Hz | ±350 Hz | End-of-Life | Critical |
| **FireAngel** | FA3820-EU | CO Detector | 45s | 3,100 Hz | ±350 Hz | Sensor Fault | Critical |
| **Samsung** | French Door | Refrigerator | 120s | 2,048 Hz | ±250 Hz | Door Ajar | Warning |
| **LG** | Smart Inverter | Refrigerator | 60s | 2,400 Hz | ±250 Hz | Door Ajar | Warning |
| **Bosch** | Serie 6 | Freezer | 30s | 2,200 Hz | ±250 Hz | Temp Exceeded | Critical |
| **Govee** | H5054 | Water Leak | 15s | 2,800 Hz | ±300 Hz | Moisture Detected | Critical |
| **Moen** | Flo Smart | Leak Detector | 30s | 2,600 Hz | ±300 Hz | Pipe Moisture | Critical |
| **YoLink** | Smart Leak | Leak Sensor | 60s | 2,900 Hz | ±300 Hz | Low Battery | Warning |
| **APC** | Back-UPS Pro 1500 | Battery Backup | 30s | 1,800 Hz | ±250 Hz | Battery Depleted | Critical |
| **CyberPower** | CP1500 | Battery Backup | 15s | 2,000 Hz | ±250 Hz | On Battery | Warning |
| **Midea** | Cube | Dehumidifier | 60s | 2,500 Hz | ±250 Hz | Bucket Full | Warning |
| **Carrier** | Infinity 98 | HVAC Furnace | 10s | 1,500 Hz | ±250 Hz | Filter Pressure | Warning |

*\*Calibrated against physical smoke detector piezo recordings (`Bloofrzo` CC0 `#819808` and `#819807`).*

---

## Bundled Real Hardware & ESC-50 Reference Corpus (`corpus/`)

To support reproducible acoustic DSP benchmarking without copyleft restrictions, this repository includes 11 real-world CC0 / CC-BY WAV recordings in [`corpus/`](corpus/) alongside [`corpus/manifest.json`](corpus/manifest.json):

1. **Calibrated Physical Smoke Detector Piezos (`2 clips`, CC0 1.0):**
   - `real_smoke_detector_chirp_819808.wav` (Freesound `#819808` by Bloofrzo — measured peak `3,368.1 Hz`, `101.5 ms` pulse width)
   - `real_smoke_detector_chirp_819807.wav` (Freesound `#819807` by Bloofrzo — measured peak `3,122.3 Hz`, `17.0 ms` pulse width)
2. **Real Hardware Tone DSP Reference Clips (`3 clips`, CC0 / CC-BY 4.0):**
   - `real_hardware_post_beep_cc0.wav` (NEC PC-9801VX POST beep, `~2,000 Hz`)
   - `real_microwave_beep_144227.wav` (Appliance microwave button beep, `~2,090 Hz`)
   - `real_buzzer.wav` (Electromechanical warning buzzer, `~2,478 Hz`)
3. **ESC-50 Domestic Non-Alarm Specificity Set (`6 clips`, CC-BY, Piczak ACM MM 2015):**
   - `esc50_washing_machine_21896.wav` (`1-21896-A-35.wav`)
   - `esc50_vacuum_cleaner_100210.wav` (`1-100210-A-36.wav`)
   - `esc50_pouring_water_118559.wav` (`1-118559-A-17.wav`)
   - `esc50_door_knock_101336.wav` (`1-101336-A-30.wav`)
   - `esc50_footsteps_155858.wav` (`1-155858-A-25.wav`)
   - `esc50_clock_tick_21934.wav` (`1-21934-A-38.wav`)

---

## Contributing a New Device Signature
We welcome community contributions! See **[CONTRIBUTING.md](CONTRIBUTING.md)** for our full contribution guidelines, schema definitions, and testing instructions.

```bash
python -m pytest -v
```

---

## License
- **Code:** Licensed under the [MIT License](LICENSE).
- **Data (`codes.csv`, `corpus/manifest.json`):** Released under [Creative Commons Attribution 4.0 International (CC-BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
