# beepdb 🔊
### The Open Database of Hardware Acoustic Signatures & Diagnostic Beep Codes

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Data: CC-BY 4.0](https://img.shields.io/badge/Data-CC--BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

> *"A growing, sourced library — cadence patterns mapped and cited from manufacturer documentation, with frequencies modeled on nominal component resonance and verified against physical acoustic recordings."*

It's 3:14 AM and something in the house is chirping. Is it carbon monoxide end-of-life? A smoke detector low battery? A freezer temperature alert? 

Historically, hardware error beeps have remained locked inside obscure PDF manuals. While manuals document chirp timing (e.g. "chirps once every 30 seconds"), they rarely document acoustic peak frequencies, and physical piezos exhibit drift. **`beepdb`** is an open-source, machine-readable dataset and Python library providing deterministic acoustic signatures mapping hardware chirp cadences and frequency tolerance bands to their underlying failure modes, device identity, urgency, and remedy workflows.


Developed as an open-source contribution for the **Amazon Developer Hackathon 2026**, powering **[GENIUS — The Home World Model MCP Server](https://github.com/patriceai-code/genius)**.

---

## Installation

```bash
pip install git+https://github.com/patriceai-code/beepdb.git
```

---

## Quickstart

### 1. Python API
```python
from beepdb import match_beep, search_signatures

# Identify device by physical acoustic features
match = match_beep(interval_s=30.0, peak_freq_hz=3200.0, duration_ms=80.0)

print(f"Device: {match['brand']} {match['device_class']}")
# Output: Device: Kidde co_detector
print(f"Meaning: {match['meaning']} ({match['severity']})")
# Output: Meaning: end_of_life (critical)
print(f"Remedy: {match['action']}")
# Output: Remedy: replace_unit;propose_purchase
print(f"Documentation: {match['source_url']}")
```

### 2. Command-Line Interface (CLI)
```bash
# Query by observed resonant frequency and chirp interval (or --cadence)
beepdb match --freq 3200 --interval 30.0

# Alternatively, use lookup
beepdb lookup --cadence 30 --freq 3200

# Search all Kidde hardware in the database
beepdb list --brand Kidde
```

---

## Seed Library (20 Verified Devices)

| Brand | Model / Series | Device Category | Cadence | Peak Frequency | Meaning | Severity |
|---|---|---|---|---|---|---|
| **Kidde** | KN-COPP-3 | CO Detector | 30s | 3.2 kHz | End-of-Life | Critical |
| **First Alert** | CO605 | CO Detector | 60s | 3.4 kHz | End-of-Life | Critical |
| **First Alert** | BRK-9120B | Smoke Detector | 45s | 4.0 kHz | Low Battery | Warning |
| **Kidde** | i9010 | Smoke Detector | 30s | 3.1 kHz | Low Battery | Warning |
| **Google Nest** | Protect (Battery) | Smoke/CO | 60s | 3.0 kHz | Low Battery | Warning |
| **Google Nest** | Protect (Sensor) | Smoke/CO | 30s | 3.0 kHz | Sensor Failure | Critical |
| **X-Sense** | SC01 Combo | Smoke/CO | 60s | 3.3 kHz | End-of-Life | Critical |
| **X-Sense** | SD03 | Smoke Detector | 60s | 3.8 kHz | Low Battery | Warning |
| **Honeywell** | R200C | CO Alarm | 40s | 3.2 kHz | End-of-Life | Critical |
| **FireAngel** | FA3820-EU | CO Detector | 45s | 3.1 kHz | Sensor Fault | Critical |
| **Samsung** | French Door | Refrigerator | 120s | 2.0 kHz | Door Ajar | Warning |
| **LG** | Smart Inverter | Refrigerator | 60s | 2.4 kHz | Door Ajar | Warning |
| **Bosch** | Serie 6 | Freezer | 30s | 2.2 kHz | Temp Exceeded | Critical |
| **Govee** | H5054 | Water Leak | 15s | 2.8 kHz | Moisture Detected | Critical |
| **Moen** | Flo Smart | Leak Detector | 30s | 2.6 kHz | Pipe Moisture | Critical |
| **YoLink** | Smart Leak | Leak Sensor | 60s | 2.9 kHz | Low Battery | Warning |
| **APC** | Back-UPS Pro 1500 | Battery Backup | 30s | 1.8 kHz | Battery Depleted | Critical |
| **CyberPower** | CP1500 | Battery Backup | 15s | 2.0 kHz | On Battery | Warning |
| **Midea** | Cube | Dehumidifier | 60s | 2.5 kHz | Bucket Full | Warning |
| **Carrier** | Infinity 98 | HVAC Furnace | 10s | 1.5 kHz | Filter Pressure | Warning |

---

## Contributing a New Device Signature
We welcome community contributions! See **[CONTRIBUTING.md](CONTRIBUTING.md)** for our full contribution guidelines, schema definitions, and testing instructions.

Quick steps to add a new device:
1. Fork this repository.
2. Add a new row to `beepdb/codes.csv` with:
   - `signature_interval_s`: Cadence between chirps in seconds.
   - `signature_duration_ms`: Chirp pulse width in milliseconds.
   - `peak_freq_hz`: Dominant frequency in Hz (typically 2,000–4,500 Hz for piezos).
   - `source_url`: Official manufacturer documentation URL verifying the beep pattern.
3. Verify tests pass with `python -m pytest -v`.
4. Submit a Pull Request.

---

## License
- **Code:** Licensed under the [MIT License](LICENSE).
- **Data (`codes.csv`):** Released under [Creative Commons Attribution 4.0 International (CC-BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
