"""
analyzer/detector.py

Rule-based Python error detector.
Scans a log string for known Python exception names and returns structured results.
No AI or external calls — pure regex pattern matching.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from analyzer.advice import ErrorAdvice, get_advice

# ── Error catalogue ───────────────────────────────────────────────────────────
# Each entry: (error_name, emoji, short description)
_ERROR_CATALOGUE: list[tuple[str, str, str]] = [
    ("ModuleNotFoundError", "📦", "A required module could not be found or is not installed."),
    ("ImportError",         "📦", "A module exists but something inside it could not be imported."),
    ("NameError",           "🔤", "A variable or function name is used before it is defined."),
    ("UnboundLocalError",   "🔤", "A local variable is referenced before assignment."),
    ("TypeError",           "🔀", "An operation is applied to an object of the wrong type."),
    ("ValueError",          "⚠️",  "A function received an argument of the right type but wrong value."),
    ("IndexError",          "📋", "A sequence index is out of range."),
    ("KeyError",            "🗝️",  "A dictionary key does not exist."),
    ("AttributeError",      "🔧", "An object does not have the expected attribute or method."),
    ("SyntaxError",         "🖊️",  "The Python code contains a syntax mistake."),
    ("IndentationError",    "🖊️",  "Code indentation is incorrect."),
    ("FileNotFoundError",   "📁", "A file or directory path does not exist."),
    ("PermissionError",     "🔒", "Insufficient permissions to perform a file/OS operation."),
    ("ZeroDivisionError",   "➗", "Division or modulo by zero was attempted."),
    ("RecursionError",      "🔁", "Maximum recursion depth was exceeded."),
    ("MemoryError",         "💾", "The program ran out of available memory."),
    ("OverflowError",       "📈", "A numeric result is too large to be represented."),
    ("RuntimeError",        "💥", "A generic runtime error occurred."),
    ("StopIteration",       "🔂", "An iterator has no more items to yield."),
    ("AssertionError",      "❌", "An assert statement failed."),
    ("OSError",             "🖥️",  "An OS-level error occurred (parent of IOError, FileNotFoundError, etc.)."),
    ("IOError",             "🖥️",  "An input/output error occurred."),
    ("ConnectionError",     "🌐", "A network connection could not be established."),
    ("TimeoutError",        "⏱️",  "An operation timed out."),
    ("NotImplementedError", "🚧", "A method or feature is not yet implemented."),
    ("Exception",           "❓", "A generic Python exception was raised."),
]

# Pre-compile one pattern per error name for speed
_PATTERNS: list[tuple[str, re.Pattern[str], str, str]] = [
    (name, re.compile(rf"\b{re.escape(name)}\b"), emoji, desc)
    for name, emoji, desc in _ERROR_CATALOGUE
]


@dataclass
class DetectedError:
    name: str
    emoji: str
    description: str
    # Line numbers (1-based) where the error name appears
    lines: list[int] = field(default_factory=list)
    # Advice fields — populated from analyzer.advice; None if no entry exists
    advice: ErrorAdvice | None = field(default=None)


def detect_errors(log_text: str) -> list[DetectedError]:
    """
    Scan *log_text* for known Python exception names.

    Returns a list of DetectedError (one per unique error type found),
    ordered by first occurrence in the text.
    Stops at "Exception" only if no more-specific error was found, because
    "Exception" is a base class that appears in many tracebacks.
    """
    if not log_text or not log_text.strip():
        return []

    lines = log_text.splitlines()
    found: dict[str, DetectedError] = {}

    for lineno, line in enumerate(lines, start=1):
        for name, pattern, emoji, desc in _PATTERNS:
            if pattern.search(line):
                if name not in found:
                    found[name] = DetectedError(
                        name=name,
                        emoji=emoji,
                        description=desc,
                        advice=get_advice(name),
                    )
                found[name].lines.append(lineno)

    results = list(found.values())

    # If both a specific error AND the generic "Exception" are present,
    # drop "Exception" to avoid noise — it almost always appears alongside.
    if len(results) > 1 and any(e.name != "Exception" for e in results):
        results = [e for e in results if e.name != "Exception"]

    return results
