"""
analyzer/parser.py

Ingests error log text from various sources (uploaded file bytes or a raw string)
and delegates detection to analyzer.detector.
"""

from __future__ import annotations

from analyzer.detector import DetectedError, detect_errors


def parse_uploaded_file(file_bytes: bytes, encoding: str = "utf-8") -> str:
    """Decode raw bytes from an uploaded file into a plain string."""
    try:
        return file_bytes.decode(encoding)
    except UnicodeDecodeError:
        return file_bytes.decode("latin-1")


def analyze_log(log_text: str) -> list[DetectedError]:
    """
    Public entry point used by app.py.

    Accepts a log string (from either upload or text-area paste),
    strips it, and returns detected error results.
    """
    return detect_errors(log_text.strip())
