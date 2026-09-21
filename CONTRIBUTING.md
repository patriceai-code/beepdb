# Contributing to beepdb 🔊

Thank you for your interest in contributing to **`beepdb`**!

`beepdb` is an open-source, machine-readable dataset and diagnostic library for hardware acoustic signatures and diagnostic beep codes. Our goal is to catalog the acoustic error signals of residential infrastructure, home appliances, and life-safety sensors so that smart homes and voice assistants can identify failures deterministically.

---

## Split Licensing Model

To maximize utility for both open-source developers and commercial integrations, `beepdb` is released under a split licensing model:
- **Source Code (Python library, CLI, tests):** Licensed under the **[MIT License](LICENSE)**.
- **Dataset (`beepdb/codes.csv`):** Licensed under the **[Creative Commons Attribution 4.0 International (CC-BY 4.0)](https://creativecommons.org/licenses/by/4.0/)** license.

By contributing to this repository, you agree that your code contributions will be licensed under MIT and your data contributions under CC-BY 4.0.

---

## How to Add a Hardware Signature

We welcome contributions of new acoustic signatures from physical recordings or verified manufacturer manuals!

### 1. Fork & Branch
```bash
git clone https://github.com/<your-username>/beepdb.git
cd beepdb
git checkout -b add-signature-<brand>-<model>
```

### 2. Add Your Entry to `beepdb/codes.csv`
Open `beepdb/codes.csv` and append your verified hardware signature adhering to the schema:

| Column | Type | Description | Example |
|---|---|---|---|
| `brand` | string | Hardware manufacturer | `Kidde` |
| `device_class` | string | Device category | `co_detector`, `smoke_detector`, `refrigerator`, `hvac` |
| `meaning` | string | Failure mode or alert meaning | `end_of_life`, `low_battery`, `door_ajar`, `filter_pressure` |
| `signature_interval_s` | float | Cadence interval between chirps in seconds | `30.0` |
| `signature_duration_ms` | float | Typical duration of each beep pulse in ms | `80.0` |
| `peak_freq_hz` | float | Resonant center frequency in Hz (typically 2,000–4,500 Hz for piezos) | `3200.0` |
| `freq_tolerance_hz` | float | Allowed tolerance band around peak frequency | `350.0` |
| `action` | string | Remediation workflow semicolon-delimited | `replace_unit;propose_purchase` |
| `severity` | string | Urgency level: `critical`, `warning`, or `info` | `critical` |
| `source_url` | string | Citation URL to official manual, support article, or datasheet | `https://www.kidde.com/...` |

### 3. Verify Local Tests Pass
Install the package in development mode and run the test suite:
```bash
python -m pip install -e .
python -m pytest -v
```

Test your new signature with the CLI:
```bash
python -m beepdb.cli match --freq 3200 --interval 30.0
python -m beepdb.cli list --brand <YourBrand>
```

### 4. Submit a Pull Request
- Create a clear PR title: `feat(signatures): add <Brand> <Model> <Alert Meaning>`
- In your PR description, include:
  1. The device model and manufacturer documentation link.
  2. How frequency was determined (nominal spec from manual, audio spectrum analysis, or empirical recording).
  3. Confirmation that all 5 tests pass.

---

## Sourcing & Ground-Truth Standards

To prevent hallucinated or inaccurate signatures from entering the database:
- **Cadence Interval (`signature_interval_s`):** Must be documented in the manufacturer's user manual or technical bulletin.
- **Frequency (`peak_freq_hz`):** Should be verified either via manufacturer component specs (piezoceramic resonant frequency) or an empirical audio recording analyzed with FFT.
- **Citations:** Every entry must include a valid, publicly accessible `source_url`.
