"""Tests for standalone beepdb package and bundled real acoustic corpus."""

import os
import json
import wave
import pytest
from beepdb import load_database, search_signatures, match_beep, match_description

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
# Check package-bundled corpus first, then root corpus fallback
CORPUS_DIR = os.path.join(REPO_ROOT, "beepdb", "corpus")
if not os.path.exists(CORPUS_DIR):
    CORPUS_DIR = os.path.join(REPO_ROOT, "corpus")
MANIFEST_PATH = os.path.join(CORPUS_DIR, "manifest.json")


def test_load_database():
    db = load_database()
    assert len(db) >= 20
    assert any(sig.brand == "Kidde" for sig in db)
    assert any(sig.brand == "First Alert" for sig in db)


def test_search_by_brand():
    results = search_signatures(brand="Kidde")
    assert len(results) >= 2
    for r in results:
        assert r.brand == "Kidde"


def test_match_kidde_co():
    match = match_beep(interval_s=30.0, peak_freq_hz=3200.0, duration_ms=80.0)
    assert match is not None
    assert match["brand"] == "Kidde"
    assert match["device_class"] == "co_detector"
    assert match["meaning"] == "end_of_life"
    assert match["confidence"] >= 0.90


def test_match_description_voice_native():
    match = match_description(interval_s=30.0, brand="Kidde", pitch="high")
    assert match is not None
    assert match["brand"] == "Kidde"
    assert match["meaning"] == "end_of_life"
    assert match["confidence"] >= 0.85


def test_real_corpus_manifest_and_wav_integrity():
    """Verifies that all bundled CC0/CC-BY physical piezo and ESC-50 WAV clips exist and are valid PCM WAVs."""
    assert os.path.exists(MANIFEST_PATH), "corpus/manifest.json must exist"
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    assert len(manifest["calibrated_smoke_piezos"]) == 2
    assert len(manifest["hardware_tone_dsp_checks"]) == 3
    assert len(manifest["esc50_domestic_non_alarm_clips"]) == 6

    all_entries = (
        manifest["calibrated_smoke_piezos"]
        + manifest["hardware_tone_dsp_checks"]
        + manifest["esc50_domestic_non_alarm_clips"]
    )
    for entry in all_entries:
        wav_path = os.path.join(CORPUS_DIR, entry["filename"])
        assert os.path.exists(wav_path), f"Missing corpus WAV file: {entry['filename']}"
        with wave.open(wav_path, "rb") as wf:
            assert wf.getnframes() > 0
            assert wf.getframerate() >= 8000


def test_calibrated_physical_piezo_peaks_match_beepdb():
    """Verifies that the empirical peak frequencies from Bloofrzo CC0 smoke detector piezos match beepdb."""
    # #819808 measured at 3368.1 Hz, 101.5 ms with 30s cadence
    m1 = match_beep(interval_s=30.0, peak_freq_hz=3368.1, duration_ms=101.5)
    assert m1 is not None
    assert m1["brand"] == "Kidde"
    assert m1["confidence"] >= 0.85

    # #819807 measured at 3122.3 Hz, 17.0 ms with 60s cadence
    m2 = match_beep(interval_s=60.0, peak_freq_hz=3122.3, duration_ms=17.0)
    assert m2 is not None
    assert m2["confidence"] >= 0.70


def test_cli_match(capsys, monkeypatch):
    import sys
    from beepdb.cli import main
    monkeypatch.setattr(sys, "argv", ["beepdb", "match", "--freq", "3200", "--interval", "30.0"])
    main()
    captured = capsys.readouterr()
    assert "Kidde" in captured.out
    assert "End Of Life" in captured.out


def test_cli_lookup(capsys, monkeypatch):
    import sys
    from beepdb.cli import main
    monkeypatch.setattr(sys, "argv", ["beepdb", "lookup", "--freq", "3200", "--cadence", "30.0"])
    main()
    captured = capsys.readouterr()
    assert "Kidde" in captured.out
    assert "End Of Life" in captured.out


def test_cli_describe_and_corpus(capsys, monkeypatch):
    import sys
    from beepdb.cli import main
    monkeypatch.setattr(sys, "argv", ["beepdb", "describe", "--interval", "30", "--brand", "Kidde"])
    main()
    out1 = capsys.readouterr().out
    assert "Kidde" in out1

    monkeypatch.setattr(sys, "argv", ["beepdb", "corpus"])
    main()
    out2 = capsys.readouterr().out
    assert "Calibrated Smoke Piezos: 2 clips" in out2
    assert "ESC-50 Domestic Clips:   6 clips" in out2
