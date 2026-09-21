"""
beepdb — Open Database of Hardware Acoustic Signatures & Diagnostic Beep Codes
"""

from .core import (
    BeepSignature,
    load_database,
    search_signatures,
    match_beep
)

__version__ = "0.1.0"
__all__ = ["BeepSignature", "load_database", "search_signatures", "match_beep"]
