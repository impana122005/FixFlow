"""
analyzer/confidence.py

Rule-based confidence scoring and fix-time estimation for FixFlow.

Public API:
    score_confidence(log_text, results, context_matches) -> int   (0–100)
    estimate_fix_time(error_name: str) -> str                     (e.g. "2–5 min")

Both functions are pure (no Streamlit, no I/O) so they can be unit-tested
and later swapped for AI-backed estimates without touching app.py.
"""

from __future__ import annotations

import re


# ---------------------------------------------------------------------------
# Fix-time estimates  (min_minutes – max_minutes per error type)
# ---------------------------------------------------------------------------

_FIX_TIME_MAP: dict[str, str] = {
    "NameError":           "2–5 min",
    "UnboundLocalError":   "2–5 min",
    "IndexError":          "2–5 min",
    "AssertionError":      "2–5 min",
    "StopIteration":       "2–5 min",
    "ZeroDivisionError":   "2–5 min",
    "ValueError":          "2–8 min",
    "KeyError":            "3–8 min",
    "OverflowError":       "3–8 min",
    "ModuleNotFoundError": "3–10 min",
    "ImportError":         "3–10 min",
    "TypeError":           "5–10 min",
    "AttributeError":      "5–10 min",
    "FileNotFoundError":   "5–10 min",
    "PermissionError":     "5–10 min",
    "OSError":             "5–10 min",
    "IOError":             "5–10 min",
    "RuntimeError":        "5–15 min",
    "SyntaxError":         "5–15 min",
    "IndentationError":    "5–15 min",
    "NotImplementedError": "10–20 min",
    "RecursionError":      "10–20 min",
    "ConnectionError":     "10–20 min",
    "TimeoutError":        "10–20 min",
    "MemoryError":         "15–30 min",
}

_DEFAULT_FIX_TIME = "5–15 min"


def estimate_fix_time(error_name: str) -> str:
    """Return a human-readable estimated time to fix for *error_name*."""
    return _FIX_TIME_MAP.get(error_name, _DEFAULT_FIX_TIME)


# ---------------------------------------------------------------------------
# Confidence scoring
# ---------------------------------------------------------------------------
# Score is built from three components (each 0–100), then averaged:
#
#   1. Traceback completeness  — does the log look like a real Python traceback?
#   2. Error detection certainty — how specific is the detected error?
#   3. Repository context quality — did a project file match (optional)?
#
# The final score is clamped to [0, 100].


# Patterns that indicate a well-formed Python traceback
_TB_HEADER    = re.compile(r"Traceback \(most recent call last\)", re.IGNORECASE)
_TB_FILE_LINE = re.compile(r'File ".+", line \d+')
_TB_EXCEPTION = re.compile(
    r"\b(ModuleNotFoundError|ImportError|NameError|TypeError|ValueError|"
    r"IndexError|KeyError|AttributeError|SyntaxError|IndentationError|"
    r"FileNotFoundError|PermissionError|ZeroDivisionError|RecursionError|"
    r"RuntimeError|OSError|IOError|ConnectionError|TimeoutError|"
    r"NotImplementedError|AssertionError|OverflowError|MemoryError|"
    r"StopIteration|UnboundLocalError)\b"
)

# Generic / less certain errors get a lower certainty bonus
_LOW_CERTAINTY = {"Exception", "RuntimeError", "OSError", "IOError"}


def _traceback_completeness(log_text: str) -> int:
    """Score 0–100 based on how complete the traceback looks."""
    score = 0

    if _TB_HEADER.search(log_text):
        score += 40          # has the standard header

    file_matches = len(_TB_FILE_LINE.findall(log_text))
    if file_matches >= 1:
        score += 25          # at least one File/line frame
    if file_matches >= 2:
        score += 15          # multiple frames → richer context

    if _TB_EXCEPTION.search(log_text):
        score += 20          # contains a recognisable exception name

    return min(score, 100)


def _detection_certainty(results: list) -> int:
    """Score 0–100 based on how specific and unambiguous the detection is."""
    if not results:
        return 10            # nothing detected

    primary = results[0]

    if primary.name in _LOW_CERTAINTY:
        base = 45
    else:
        base = 80            # specific, well-known error

    # Bonus for having advice (means the error is in our catalogue)
    if primary.advice is not None:
        base += 10

    # Small penalty for multiple detected errors (ambiguous log)
    if len(results) > 1:
        base -= 10 * (len(results) - 1)

    return max(10, min(base, 100))


def _context_quality(context_matches: list) -> int:
    """Score 0–100 based on repository context match quality."""
    if not context_matches:
        return 50            # neutral — no context provided, neither helps nor hurts

    best = context_matches[0]   # innermost / best match
    conf_scores = {"High": 100, "Medium": 70, "Low": 40}
    return conf_scores.get(best.confidence, 50)


def score_confidence(
    log_text: str,
    results: list,
    context_matches: list,
) -> int:
    """
    Return an overall confidence score (0–100) for the analysis.

    Weights:
      - Traceback completeness : 40 %
      - Detection certainty    : 40 %
      - Repository context     : 20 %
    """
    tb   = _traceback_completeness(log_text)
    det  = _detection_certainty(results)
    ctx  = _context_quality(context_matches)

    weighted = int(tb * 0.40 + det * 0.40 + ctx * 0.20)
    return max(0, min(weighted, 100))
