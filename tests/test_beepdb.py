"""Tests for standalone beepdb package."""

import pytest
from beepdb import load_database, search_signatures, match_beep


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
