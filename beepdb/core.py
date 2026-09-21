"""
beepdb Core Engine
Lookup, filtering, and acoustic signature matching for hardware beep codes.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import os
import csv

CSV_PATH = os.path.join(os.path.dirname(__file__), "codes.csv")


@dataclass
class BeepSignature:
    signature_interval_s: float
    signature_duration_ms: float
    peak_freq_hz: float
    freq_tolerance_hz: float
    verification_status: str
    device_class: str
    brand: str
    meaning: str
    severity: str
    action: str
    source_url: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "signature_interval_s": self.signature_interval_s,
            "signature_duration_ms": self.signature_duration_ms,
            "peak_freq_hz": self.peak_freq_hz,
            "freq_tolerance_hz": self.freq_tolerance_hz,
            "verification_status": self.verification_status,
            "device_class": self.device_class,
            "brand": self.brand,
            "meaning": self.meaning,
            "severity": self.severity,
            "action": self.action,
            "source_url": self.source_url
        }


def load_database(csv_path: str = CSV_PATH) -> List[BeepSignature]:
    """Loads all hardware signatures from the database."""
    signatures = []
    if not os.path.exists(csv_path):
        return signatures

    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            signatures.append(BeepSignature(
                signature_interval_s=float(row["signature_interval_s"]),
                signature_duration_ms=float(row["signature_duration_ms"]),
                peak_freq_hz=float(row["peak_freq_hz"]),
                freq_tolerance_hz=float(row.get("freq_tolerance_hz", 350.0)),
                verification_status=row.get("verification_status", "cadence_verified_frequency_nominal"),
                device_class=row["device_class"],
                brand=row["brand"],
                meaning=row["meaning"],
                severity=row["severity"],
                action=row["action"],
                source_url=row["source_url"]
            ))
    return signatures


def search_signatures(
    brand: Optional[str] = None,
    device_class: Optional[str] = None,
    meaning: Optional[str] = None
) -> List[BeepSignature]:
    """Filters database by manufacturer brand, device class, or failure meaning."""
    all_sigs = load_database()
    results = all_sigs

    if brand:
        results = [s for s in results if brand.lower() in s.brand.lower()]
    if device_class:
        results = [s for s in results if device_class.lower() in s.device_class.lower()]
    if meaning:
        results = [s for s in results if meaning.lower() in s.meaning.lower()]

    return results


def match_beep(
    interval_s: float,
    peak_freq_hz: float,
    duration_ms: float = 0.0
) -> Optional[Dict[str, Any]]:
    """
    Finds the closest matching hardware device for an observed acoustic chirp.
    Prioritizes digital cadence intervals and scales frequency by component tolerance.
    """
    db = load_database()
    if not db:
        return None

    best_match = None
    best_score = -1.0

    for sig in db:
        tol_freq = sig.freq_tolerance_hz

        # 1. Cadence interval scoring (digital timer cadence)
        if interval_s > 0:
            interval_diff = abs(interval_s - sig.signature_interval_s)
            score_interval = max(0.0, 1.0 - (interval_diff / max(sig.signature_interval_s * 0.20, 3.0)))
        else:
            score_interval = 0.5

        # 2. Resonant peak frequency scoring
        freq_diff = abs(peak_freq_hz - sig.peak_freq_hz)
        score_freq = max(0.0, 1.0 - (freq_diff / tol_freq))

        # 3. Pulse duration scoring
        if duration_ms > 0:
            dur_diff = abs(duration_ms - sig.signature_duration_ms)
            score_dur = max(0.0, 1.0 - (dur_diff / 50.0))
        else:
            score_dur = 0.7

        # Composite score
        if interval_s > 0:
            composite = (score_interval * 0.55) + (score_freq * 0.35) + (score_dur * 0.10)
        else:
            composite = (score_freq * 0.75) + (score_dur * 0.25)

        if composite > best_score:
            best_score = composite
            best_match = sig

    if best_match:
        res = best_match.to_dict()
        res["confidence"] = round(min(best_score, 0.99), 2)
        return res
    return None
