"""
analyzer/repo_context.py

Repository Context Mode — Milestone 4.

Given:
  - A traceback string (the error log)
  - A collection of project Python files (names → source text)

Produces a list of ContextMatch objects that identify:
  - Which project file is likely responsible
  - Which function inside it is suspected
  - The line number (from the traceback or from a function scan)
  - A human-readable reason explaining why that file was flagged

Design note: all inputs and outputs are plain Python types / dataclasses.
No Streamlit, no I/O — easy to unit-test and easy to swap for AI-powered
matching in a future milestone.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from pathlib import PurePosixPath, PureWindowsPath


# ── Data types ────────────────────────────────────────────────────────────────

@dataclass
class TracebackFrame:
    """One frame parsed from a Python traceback."""
    raw_path: str          # exactly as it appears in the traceback
    filename: str          # basename only, e.g. "main.py"
    lineno: int | None     # line number from traceback, or None
    function: str | None   # function name from traceback, or None


@dataclass
class ContextMatch:
    """A project file matched against the traceback."""
    filename: str                  # basename of the matched project file
    full_path: str                 # full path as supplied (or basename if uploaded)
    lineno: int | None             # line number from traceback frame (if available)
    function: str | None           # function name — from traceback or AST scan
    reason: str                    # plain-English explanation of why this file was flagged
    confidence: str                # "High" | "Medium" | "Low"
    snippet: str | None = None     # relevant source lines around lineno (if source available)
    frame_index: int = 0           # position of the matching frame in the traceback (0 = innermost)


# ── Traceback parsing ─────────────────────────────────────────────────────────

# Matches:   File "path/to/file.py", line 42, in some_function
_FRAME_RE = re.compile(
    r'File\s+"([^"]+)",\s+line\s+(\d+),\s+in\s+(\S+)'
)

# Matches:   File "path/to/file.py", line 42   (no function — e.g. <module>)
_FRAME_NO_FN_RE = re.compile(
    r'File\s+"([^"]+)",\s+line\s+(\d+)'
)


def parse_traceback_frames(log_text: str) -> list[TracebackFrame]:
    """
    Extract all stack frames from a Python traceback string.

    Returns frames in traceback order (outermost first).
    The *last* frame before the exception line is typically the crash site.
    """
    frames: list[TracebackFrame] = []
    for match in _FRAME_RE.finditer(log_text):
        raw_path, lineno_str, func = match.groups()
        fname = _basename(raw_path)
        frames.append(TracebackFrame(
            raw_path=raw_path,
            filename=fname,
            lineno=int(lineno_str),
            function=func if func not in ("<module>", "<string>", "<stdin>") else None,
        ))

    if not frames:
        # Fallback: frames without a function name
        for match in _FRAME_NO_FN_RE.finditer(log_text):
            raw_path, lineno_str = match.groups()
            fname = _basename(raw_path)
            frames.append(TracebackFrame(
                raw_path=raw_path,
                filename=fname,
                lineno=int(lineno_str),
                function=None,
            ))

    return frames


def _basename(path: str) -> str:
    """Return just the filename from any path style."""
    # Try PurePosixPath first (covers Linux/Mac and most tracebacks),
    # then PureWindowsPath for Windows-style backslash paths.
    p = PurePosixPath(path)
    if p.suffix:
        return p.name
    return PureWindowsPath(path).name


# ── Project file index ────────────────────────────────────────────────────────

@dataclass
class ProjectFile:
    """Represents one Python file in the user's project."""
    filename: str        # basename, e.g. "utils.py"
    full_path: str       # as supplied by the caller
    source: str | None   # file contents, or None if not available


def build_file_index(files: dict[str, str]) -> dict[str, ProjectFile]:
    """
    Build a lookup index from filename → ProjectFile.

    Keys are lowercased basenames to enable case-insensitive matching.
    *files* is a mapping of {full_path_or_name: source_text}.
    When the same basename appears multiple times, the last entry wins.
    """
    index: dict[str, ProjectFile] = {}
    for path, source in files.items():
        fname = _basename(path) if "/" in path or "\\" in path else path
        index[fname.lower()] = ProjectFile(filename=fname, full_path=path, source=source)
    return index


# ── AST helpers ───────────────────────────────────────────────────────────────

def _functions_in_source(source: str) -> list[tuple[str, int, int]]:
    """
    Return (name, start_line, end_line) for every function/method in *source*.
    Returns [] if the source cannot be parsed.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    results: list[tuple[str, int, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            end = getattr(node, "end_lineno", node.lineno)
            results.append((node.name, node.lineno, end))
    return results


def _function_at_line(source: str, lineno: int) -> str | None:
    """Return the name of the innermost function that contains *lineno*."""
    fns = _functions_in_source(source)
    # Walk innermost first (largest start_line that is still ≤ lineno)
    candidates = [(name, start, end) for name, start, end in fns
                  if start <= lineno <= end]
    if not candidates:
        return None
    return max(candidates, key=lambda t: t[1])[0]


def _extract_snippet(source: str, lineno: int, context: int = 3) -> str:
    """Return up to *context* lines around *lineno* (1-based)."""
    src_lines = source.splitlines()
    start = max(0, lineno - context - 1)
    end = min(len(src_lines), lineno + context)
    numbered = []
    for i, line in enumerate(src_lines[start:end], start=start + 1):
        marker = "→" if i == lineno else " "
        numbered.append(f"{marker} {i:4d} │ {line}")
    return "\n".join(numbered)


# ── Matching engine ───────────────────────────────────────────────────────────

# Files that are part of the Python stdlib / installed packages — skip them
_STDLIB_PREFIXES = (
    "lib/python",
    "site-packages",
    "/usr/",
    "/opt/",
    "lib\\python",
    "Lib\\",
    "<frozen",
    "<string>",
    "<stdin>",
)


def _is_stdlib_path(raw_path: str) -> bool:
    return any(raw_path.startswith(p) or p in raw_path for p in _STDLIB_PREFIXES)


def match_context(
    frames: list[TracebackFrame],
    file_index: dict[str, ProjectFile],
) -> list[ContextMatch]:
    """
    Match traceback frames against the project file index.

    Strategy (in priority order):
    1. Exact filename match on a non-stdlib frame → High confidence
    2. Stem match (e.g. "utils" matches "utils.py") → Medium confidence
    3. No match found → no result for that frame

    Only user-owned frames (non-stdlib) are considered.
    Frames are deduplicated by filename so each project file appears at most once.
    The innermost matching frame (last in list) is ranked first.
    """
    matches: list[ContextMatch] = []
    seen_files: set[str] = set()

    # Process innermost frame first (reversed)
    for frame_idx, frame in enumerate(reversed(frames)):
        if _is_stdlib_path(frame.raw_path):
            continue

        # Case-insensitive exact match first (index keys are lowercased), then stem match
        proj_file = (
            file_index.get(frame.filename.lower())
            or _stem_match(frame.filename, file_index)
        )

        if proj_file is None or proj_file.filename in seen_files:
            continue

        seen_files.add(proj_file.filename)

        # Determine function name
        function = frame.function
        if function is None and proj_file.source and frame.lineno:
            function = _function_at_line(proj_file.source, frame.lineno)

        # Determine confidence
        if proj_file.filename == frame.filename:
            confidence = "High"
            reason = (
                f"**{proj_file.filename}** appears directly in the traceback "
                f"(frame {frame_idx + 1} from innermost)"
            )
        else:
            confidence = "Medium"
            reason = (
                f"**{proj_file.filename}** was matched by stem to traceback path "
                f"`{frame.raw_path}` (frame {frame_idx + 1} from innermost)"
            )

        if frame.lineno:
            reason += f" at **line {frame.lineno}**"
        if function:
            reason += f" inside function **`{function}`**"
        reason += "."

        # Extract snippet
        snippet = None
        if proj_file.source and frame.lineno:
            snippet = _extract_snippet(proj_file.source, frame.lineno)

        matches.append(ContextMatch(
            filename=proj_file.filename,
            full_path=proj_file.full_path,
            lineno=frame.lineno,
            function=function,
            reason=reason,
            confidence=confidence,
            snippet=snippet,
            frame_index=frame_idx,
        ))

    return matches


def _stem_match(
    target_filename: str,
    file_index: dict[str, ProjectFile],
) -> ProjectFile | None:
    """Match by stem when exact match fails. Index keys are already lowercased."""
    target_stem = PurePosixPath(target_filename).stem.lower()
    for key, proj_file in file_index.items():
        if PurePosixPath(key).stem == target_stem:
            return proj_file
    return None


# ── Public entry point ────────────────────────────────────────────────────────

def analyze_repo_context(
    log_text: str,
    project_files: dict[str, str],
) -> list[ContextMatch]:
    """
    Full pipeline: parse traceback → build index → match files.

    Args:
        log_text:      The raw error log / traceback string.
        project_files: Mapping of {filename_or_path: source_code}.
                       Source code may be an empty string if unavailable.

    Returns:
        List of ContextMatch, innermost/highest-confidence first.
        Empty list if no project files matched.
    """
    frames = parse_traceback_frames(log_text)
    if not frames:
        return []

    index = build_file_index(project_files)
    return match_context(frames, index)
