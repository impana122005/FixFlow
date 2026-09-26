"""
reports/report_generator.py

Generates a professional PDF bug report from FixFlow analysis results.
Uses fpdf2 (pure Python, no system font dependencies).

Public entry point:
    generate_pdf(report_data: BugReportData) -> bytes
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from fpdf import FPDF

# ---------------------------------------------------------------------------
# Data contract — all inputs to the PDF generator
# ---------------------------------------------------------------------------

@dataclass
class ContextInfo:
    filename: str
    lineno: int | None
    function: str | None
    confidence: str


@dataclass
class BugReportData:
    timestamp: str                          # pre-formatted, e.g. "2025-06-15 14:32:07 UTC"
    error_type: str                         # e.g. "ModuleNotFoundError"
    error_message: str                      # raw last line of the traceback
    explanation: str
    root_cause: str
    fix_steps: list[str]
    example_fix: str
    context_matches: list[ContextInfo] = field(default_factory=list)
    raw_log: str = ""
    report_id: str = ""                     # auto-generated, e.g. "FF-2026-0001"
    severity: str = "Medium"               # "High" | "Medium" | "Low"


# ---------------------------------------------------------------------------
# Severity mapping
# ---------------------------------------------------------------------------

_SEVERITY_MAP: dict[str, str] = {
    # High — errors that prevent the program from running at all
    "SyntaxError":          "High",
    "IndentationError":     "High",
    "ModuleNotFoundError":  "High",
    "ImportError":          "High",
    "RecursionError":       "High",
    "MemoryError":          "High",
    "SystemExit":           "High",
    # Medium — runtime errors that crash the program but are often fixable
    "NameError":            "Medium",
    "UnboundLocalError":    "Medium",
    "TypeError":            "Medium",
    "AttributeError":       "Medium",
    "RuntimeError":         "Medium",
    "NotImplementedError":  "Medium",
    "PermissionError":      "Medium",
    "FileNotFoundError":    "Medium",
    "ConnectionError":      "Medium",
    "TimeoutError":         "Medium",
    "OSError":              "Medium",
    "IOError":              "Medium",
    # Low — logic errors that are usually caught and handled
    "IndexError":           "Low",
    "KeyError":             "Low",
    "ValueError":           "Low",
    "ZeroDivisionError":    "Low",
    "AssertionError":       "Low",
    "StopIteration":        "Low",
    "OverflowError":        "Low",
}

_SEVERITY_COLOURS: dict[str, tuple[tuple[int, int, int], tuple[int, int, int]]] = {
    # (background, bar/text accent)
    "High":   ((255, 241, 242), (220,  38,  38)),   # red tones
    "Medium": ((255, 247, 237), (234,  88,  12)),   # orange tones
    "Low":    ((254, 252, 232), (161, 138,   0)),   # yellow tones
}


def get_severity(error_type: str) -> str:
    """Return 'High', 'Medium', or 'Low' for a Python exception name."""
    return _SEVERITY_MAP.get(error_type, "Medium")


def _generate_report_id() -> str:
    """Return a unique report ID of the form FF-YYYY-NNNN."""
    import random
    now = datetime.utcnow()
    seq = random.randint(1, 9999)
    return f"FF-{now.year}-{seq:04d}"


# ---------------------------------------------------------------------------
# PDF builder
# ---------------------------------------------------------------------------

# Colours (R, G, B)
_C_BLACK        = (31,  35,  40)
_C_MUTED        = (87,  96, 106)
_C_ACCENT       = (59, 130, 212)
_C_ORANGE_BG    = (255, 248, 240)
_C_ORANGE_BAR   = (249, 115,  22)
_C_YELLOW_BG    = (254, 252, 195)
_C_YELLOW_BAR   = (202, 138,   4)
_C_GREEN_BG     = (240, 253, 244)
_C_GREEN_BAR    = ( 22, 163,  74)
_C_AMBER_BG     = (254, 252, 195)
_C_AMBER_BAR    = (202, 138,   4)
_C_LIGHT_GREY   = (247, 248, 250)
_C_BORDER       = (229, 231, 235)
_C_WHITE        = (255, 255, 255)
_C_CODE_BG      = ( 39,  39,  42)   # dark bg for code blocks
_C_CODE_FG      = (212, 212, 216)   # light text on dark bg

_PAGE_W         = 210   # A4 width mm
_MARGIN         = 18
_CONTENT_W      = _PAGE_W - 2 * _MARGIN


# ---------------------------------------------------------------------------
# Text sanitisation — fpdf2 with core fonts only supports latin-1
# ---------------------------------------------------------------------------

_UNICODE_REPLACEMENTS: dict[str, str] = {
    "\u2014": "--",    # em dash
    "\u2013": "-",     # en dash
    "\u2018": "'",     # left single quote
    "\u2019": "'",     # right single quote
    "\u201c": '"',     # left double quote
    "\u201d": '"',     # right double quote
    "\u2026": "...",   # ellipsis
    "\u2022": "*",     # bullet
    "\u00a0": " ",     # non-breaking space
    "\u2192": "->",    # rightwards arrow
    "\u2190": "<-",    # leftwards arrow
    "\u2248": "~=",    # almost equal
    "\u00b0": "deg",   # degree sign
}


def _safe(text: str) -> str:
    """Replace non-latin-1 characters so fpdf core fonts don't crash."""
    for char, replacement in _UNICODE_REPLACEMENTS.items():
        text = text.replace(char, replacement)
    # Final fallback: encode to latin-1, replacing anything still unmappable
    return text.encode("latin-1", errors="replace").decode("latin-1")


class _PDF(FPDF):
    """Custom FPDF subclass with helpers for FixFlow report styling."""

    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_margins(_MARGIN, _MARGIN, _MARGIN)
        self.set_auto_page_break(auto=True, margin=_MARGIN)
        self.add_page()
        self._page_number = 0

    # ── Header / Footer ───────────────────────────────────────────────────

    def header(self):
        # Top accent bar
        self.set_fill_color(*_C_ACCENT)
        self.rect(0, 0, _PAGE_W, 3, "F")

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*_C_MUTED)
        self.cell(0, 4, "FixFlow Bug Report  -  Page " + str(self.page_no()), align="C")

    # ── Typography helpers ────────────────────────────────────────────────

    def h1(self, text: str):
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(*_C_BLACK)
        self.ln(2)
        self.multi_cell(_CONTENT_W, 9, _safe(text))
        self.ln(1)

    def h2(self, text: str):
        self.ln(4)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*_C_ACCENT)
        self.multi_cell(_CONTENT_W, 6, _safe(text))
        # Underline rule
        self.set_draw_color(*_C_BORDER)
        self.set_line_width(0.3)
        self.line(_MARGIN, self.get_y(), _PAGE_W - _MARGIN, self.get_y())
        self.ln(3)

    def body(self, text: str):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*_C_BLACK)
        self.multi_cell(_CONTENT_W, 5.5, _safe(text))

    def caption(self, text: str):
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*_C_MUTED)
        self.multi_cell(_CONTENT_W, 5, _safe(text))

    # ── Coloured callout box ──────────────────────────────────────────────

    def callout(
        self,
        text: str,
        bg: tuple[int, int, int],
        bar: tuple[int, int, int],
        padding: float = 3.0,
    ):
        """Render a left-bar callout box with background fill."""
        text = _safe(text)
        # Measure text height first using a dry-run
        text_lines = self._split_text(text, _CONTENT_W - 8)
        line_h = 5.5
        box_h = len(text_lines) * line_h + padding * 2

        # Draw background + left bar
        self.set_fill_color(*bg)
        self.set_draw_color(*bg)
        self.rect(self.get_x(), self.get_y(), _CONTENT_W, box_h, "F")
        self.set_fill_color(*bar)
        self.rect(self.get_x(), self.get_y(), 2.5, box_h, "F")

        # Text inside
        self.set_xy(self.get_x() + 6, self.get_y() + padding)
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*_C_BLACK)
        self.multi_cell(_CONTENT_W - 8, line_h, text)
        self.ln(padding)

    def _split_text(self, text: str, width: float) -> list[str]:
        """Return lines as fpdf would wrap them (approximate)."""
        self.set_font("Helvetica", "", 9.5)
        return self.multi_cell(width, 5.5, _safe(text), dry_run=True, output="LINES")

    # ── Code block ───────────────────────────────────────────────────────

    def code_block(self, code: str):
        """Dark-background monospace code block."""
        code = _safe(code)
        lines = code.splitlines() or [""]
        line_h = 4.8
        box_h = len(lines) * line_h + 5

        # Background
        self.set_fill_color(*_C_CODE_BG)
        self.set_draw_color(*_C_CODE_BG)
        self.rect(self.get_x(), self.get_y(), _CONTENT_W, box_h, "F")

        self.set_xy(self.get_x() + 4, self.get_y() + 2.5)
        self.set_font("Courier", "", 8)
        self.set_text_color(*_C_CODE_FG)
        self.multi_cell(_CONTENT_W - 6, line_h, code)
        self.ln(1)
        # Reset text colour
        self.set_text_color(*_C_BLACK)

    # ── Inline badge ─────────────────────────────────────────────────────

    def badge(self, label: str, bg: tuple[int, int, int], fg: tuple[int, int, int] = _C_WHITE):
        self.set_font("Helvetica", "B", 7.5)
        w = self.get_string_width(_safe(label)) + 6
        self.set_fill_color(*bg)
        self.set_text_color(*fg)
        self.cell(w, 5, _safe(label), fill=True, align="C")
        self.set_text_color(*_C_BLACK)


# ---------------------------------------------------------------------------
# Report assembly
# ---------------------------------------------------------------------------

def generate_pdf(data: BugReportData) -> bytes:
    """
    Build and return the PDF as raw bytes ready for st.download_button.

    All styling uses built-in Helvetica/Courier — no external font files needed.
    """
    pdf = _PDF()

    # ── Report header ─────────────────────────────────────────────────────────
    sev_bg, sev_bar = _SEVERITY_COLOURS.get(data.severity, _SEVERITY_COLOURS["Medium"])

    pdf.ln(6)

    # ── Hackathon badge (top-left) ────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_fill_color(*_C_ACCENT)
    pdf.set_text_color(*_C_WHITE)
    badge_w = pdf.get_string_width("IBM BOB 2.0 HACKATHON") + 8
    pdf.cell(badge_w, 6, "IBM BOB 2.0 HACKATHON", fill=True, align="C")
    pdf.ln(10)

    # ── Title ─────────────────────────────────────────────────────────────────
    pdf.h1("FixFlow Bug Report")
    pdf.ln(1)

    # ── Metadata table — a clean two-column grid ──────────────────────────────
    # Each row: label (bold, muted) on the left | value on the right
    ROW_H  = 7.0    # row height
    LBL_W  = 40.0   # label column width
    VAL_W  = _CONTENT_W - LBL_W
    LBL_SZ = 8.5
    VAL_SZ = 9.0

    # Outer box
    table_top = pdf.get_y()
    table_h   = ROW_H * 4          # 4 rows
    pdf.set_fill_color(247, 248, 250)
    pdf.set_draw_color(*_C_BORDER)
    pdf.set_line_width(0.25)
    pdf.rect(_MARGIN, table_top, _CONTENT_W, table_h, "FD")

    def _meta_row(label: str, value: str, y: float):
        # Label cell
        pdf.set_xy(_MARGIN + 3, y + 1.5)
        pdf.set_font("Helvetica", "B", LBL_SZ)
        pdf.set_text_color(*_C_MUTED)
        pdf.cell(LBL_W - 3, ROW_H - 3, _safe(label))
        # Value cell
        pdf.set_xy(_MARGIN + LBL_W, y + 1.5)
        pdf.set_font("Helvetica", "", VAL_SZ)
        pdf.set_text_color(*_C_BLACK)
        pdf.cell(VAL_W, ROW_H - 3, _safe(value))
        # Thin separator line (skip on last row)
        pdf.set_draw_color(*_C_BORDER)
        pdf.set_line_width(0.2)
        pdf.line(_MARGIN, y + ROW_H, _MARGIN + _CONTENT_W, y + ROW_H)

    _meta_row("Report ID:",     data.report_id,              table_top + ROW_H * 0)
    _meta_row("Generated By:",  "FixFlow v1.0",              table_top + ROW_H * 1)
    _meta_row("Generated On:",  data.timestamp,              table_top + ROW_H * 2)
    _meta_row("Severity:",      data.severity,               table_top + ROW_H * 3)

    # Severity colour swatch — small filled rect inside the Severity value cell
    swatch_y = table_top + ROW_H * 3 + 2.5
    swatch_x = _MARGIN + LBL_W + pdf.get_string_width(data.severity) + 4
    pdf.set_fill_color(*sev_bar)
    pdf.rect(swatch_x, swatch_y, 14, 3, "F")

    pdf.set_y(table_top + table_h + 5)

    # ── Error type banner ─────────────────────────────────────────────────────
    pdf.callout(
        f"Error Detected: {data.error_type}",
        bg=_C_ORANGE_BG,
        bar=_C_ORANGE_BAR,
    )
    pdf.ln(1)

    if data.error_message:
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(*_C_MUTED)
        # Truncate very long messages
        raw_msg = data.error_message[:220] + ("..." if len(data.error_message) > 220 else "")
        pdf.multi_cell(_CONTENT_W, 5, _safe(f'"{raw_msg}"'))
        pdf.set_text_color(*_C_BLACK)
        pdf.ln(2)

    # ── Explanation ───────────────────────────────────────────────────────────
    pdf.h2("What does this mean?")
    pdf.body(data.explanation)

    # ── Root cause ────────────────────────────────────────────────────────────
    pdf.h2("Most Likely Root Cause")
    pdf.callout(data.root_cause, bg=_C_YELLOW_BG, bar=_C_YELLOW_BAR)

    # ── Fix steps ─────────────────────────────────────────────────────────────
    # Rendering approach: write the number badge, then write the step text in a
    # multi_cell that is indented by the badge width.  We save/restore X so that
    # every step starts at the left margin regardless of how many lines the
    # previous step wrapped to.
    pdf.h2("Step-by-Step Fix")
    LINE_H   = 5.5   # line height (mm)
    NUM_W    = 9.0   # fixed indent width for the number column (mm)
    TEXT_W   = _CONTENT_W - NUM_W

    for i, step in enumerate(data.fix_steps, start=1):
        # --- record where this step starts ---
        step_top = pdf.get_y()
        step_x   = pdf.get_x()   # should be _MARGIN

        # --- number badge (stays on step_top line) ---
        pdf.set_font("Helvetica", "B", 9.5)
        pdf.set_text_color(*_C_ACCENT)
        pdf.set_xy(step_x, step_top)
        pdf.cell(NUM_W, LINE_H, f"{i}.")

        # --- step text, indented by NUM_W ---
        pdf.set_font("Helvetica", "", 9.5)
        pdf.set_text_color(*_C_BLACK)
        pdf.set_xy(step_x + NUM_W, step_top)
        pdf.multi_cell(TEXT_W, LINE_H, _safe(step))

        # --- ensure next step starts below the tallest element ---
        # get_y() is now below the last wrapped line of the text;
        # that is always >= step_top + LINE_H, so no extra work needed.
        pdf.set_x(step_x)   # reset X to left margin for next iteration
        pdf.ln(1)            # small gap between steps

    pdf.ln(1)

    # ── Example fix ───────────────────────────────────────────────────────────
    pdf.h2("Example Fix")
    pdf.code_block(data.example_fix)

    # ── Repository context ────────────────────────────────────────────────────
    if data.context_matches:
        pdf.h2("Repository Context")
        for ctx in data.context_matches:
            conf_colors = {
                "High":   (_C_GREEN_BG,  _C_GREEN_BAR),
                "Medium": (_C_AMBER_BG,  _C_AMBER_BAR),
            }
            bg, bar = conf_colors.get(ctx.confidence, (_C_LIGHT_GREY, _C_MUTED))

            lineno_str = f"Line {ctx.lineno}" if ctx.lineno else "Line unknown"
            fn_str = ctx.function if ctx.function else "unknown"
            detail = (
                f"File: {ctx.filename}  |  {lineno_str}  |  "
                f"Function: {fn_str}  |  Confidence: {ctx.confidence}"
            )
            pdf.callout(detail, bg=bg, bar=bar)
            pdf.ln(1)

    # ── Raw log (truncated) ───────────────────────────────────────────────────
    if data.raw_log:
        pdf.h2("Raw Error Log")
        truncated = data.raw_log[:1500]
        if len(data.raw_log) > 1500:
            truncated += "\n... (truncated)"
        pdf.code_block(truncated)

    # ── Return bytes ──────────────────────────────────────────────────────────
    # fpdf2 >= 2.7: output() returns bytes when called with no argument
    return bytes(pdf.output())


# ---------------------------------------------------------------------------
# Convenience builder
# ---------------------------------------------------------------------------

def build_report_data(
    log_text: str,
    results: list,          # list[DetectedError] — avoid circular import
    context_matches: list,  # list[ContextMatch]
) -> BugReportData:
    """
    Assemble a BugReportData from FixFlow analysis outputs.
    Takes the first detected error as the primary error for the report.
    """
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    report_id = _generate_report_id()

    # Extract raw error message: last non-empty line of the log
    last_line = next(
        (l.strip() for l in reversed(log_text.splitlines()) if l.strip()),
        "",
    )

    if not results:
        return BugReportData(
            timestamp=ts,
            report_id=report_id,
            severity="Medium",
            error_type="Unknown",
            error_message=last_line,
            explanation="No recognised Python error was detected in the log.",
            root_cause="Review the raw log for clues.",
            fix_steps=["Inspect the full traceback manually."],
            example_fix="# No automated fix suggestion available.",
            raw_log=log_text,
        )

    primary = results[0]
    adv = primary.advice
    severity = get_severity(primary.name)

    ctx_infos = [
        ContextInfo(
            filename=m.filename,
            lineno=m.lineno,
            function=m.function,
            confidence=m.confidence,
        )
        for m in context_matches
    ]

    return BugReportData(
        timestamp=ts,
        report_id=report_id,
        severity=severity,
        error_type=primary.name,
        error_message=last_line,
        explanation=adv.explanation if adv else primary.description,
        root_cause=adv.root_cause if adv else "See the raw log for details.",
        fix_steps=adv.steps if adv else ["Review the traceback manually."],
        example_fix=adv.example_fix if adv else "# No example available.",
        context_matches=ctx_infos,
        raw_log=log_text,
    )
