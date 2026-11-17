# FixFlow – AI Bug-to-Fix Assistant
## Hackathon Project Report · IBM Bob 2.0 Hackathon

---

> **Team:** Impana · Harshitha G  
> **Event:** IBM Bob 2.0 Hackathon  
> **Version:** FixFlow v1.0  
> **Repository:** [github.com/impana122005/FixFlow](https://github.com/impana122005/FixFlow)  
> **Stack:** Python 3.10+ · Streamlit · fpdf2  

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Solution Overview](#3-solution-overview)
4. [Architecture](#4-architecture)
5. [Features & Implementation](#5-features--implementation)
6. [Technology Stack](#6-technology-stack)
7. [Project Structure](#7-project-structure)
8. [User Flow](#8-user-flow)
9. [Development Journey](#9-development-journey)
10. [IBM Bob Integration](#10-ibm-bob-integration)
11. [Future Roadmap](#11-future-roadmap)
12. [Team](#12-team)

---

## 1. Executive Summary

**FixFlow** is an AI-powered bug-to-fix assistant that transforms a raw Python error log into a structured, actionable fix report in seconds. A developer uploads a traceback or pastes it directly — FixFlow detects the error type, explains it in plain English, identifies the responsible file and function inside the user's own codebase, suggests a numbered fix plan with runnable code examples, and exports a professional PDF report ready to share with a team.

The project was built entirely within the IBM Bob 2.0 Hackathon, using IBM Bob as the primary coding assistant across every milestone from initial scaffolding to the final login-gated release.

---

## 2. Problem Statement

Debugging is the most time-consuming phase of software development. Developers routinely lose hours to:

- **Opaque tracebacks** — a wall of stack frames with no plain-English context
- **Stack Overflow archaeology** — searching for the right answer buried in a thread from 2015
- **File-hunting** — not knowing which source file in a large codebase caused the crash
- **Knowledge gaps** — junior developers unable to interpret certain exception types at all
- **Report overhead** — manually writing up a bug for a ticket or team communication

These pain points compound under hackathon and production-deadline pressure, where the cost of every lost hour is highest.

**FixFlow** addresses all five problems with a single interface: paste or upload your log, and receive a complete diagnostic package immediately.

---

## 3. Solution Overview

FixFlow is a **Streamlit web application** with a modular Python backend. Its core pipeline:

```
Error Log (upload / paste)
        │
        ▼
  analyzer/parser.py        ← decode bytes, strip whitespace
        │
        ▼
  analyzer/detector.py      ← regex scan → DetectedError list (26 exception types)
        │
        ▼
  analyzer/advice.py        ← rule-based advice DB → ErrorAdvice (explanation,
        │                      root cause, fix steps, example code)
        │
  analyzer/repo_context.py  ← (optional) traceback frame parser + Python AST
        │                      file matcher → ContextMatch list
        ▼
  reports/report_generator.py ← fpdf2 PDF builder → bytes
        │
        ▼
  app.py (Streamlit UI)     ← render results + st.download_button
```

The application is deliberately **layered**: the `analyzer/` and `reports/` packages contain no Streamlit or file-I/O dependencies, making them independently testable and straightforward to extend with AI-powered backends.

---

## 4. Architecture

### 4.1 Module Responsibilities

| Module | Responsibility | Key Types |
|---|---|---|
| `app.py` | UI orchestration, Streamlit widgets, CSS theme, session state | — |
| `auth.py` | Session-based login / sign-up / forgot-password gate | `ff_*` session keys |
| `analyzer/detector.py` | Regex scanner against a 26-entry error catalogue | `DetectedError` |
| `analyzer/advice.py` | Rule-based advice database; designated AI swap point | `ErrorAdvice` |
| `analyzer/parser.py` | Public entry point: bytes → string, delegates to detector | — |
| `analyzer/repo_context.py` | Traceback frame parser + Python AST file matcher | `TracebackFrame`, `ContextMatch` |
| `analyzer/fixer.py` | **Stub** — reserved for IBM Bob API integration | — |
| `reports/report_generator.py` | fpdf2 PDF builder; latin-1 safe; built-in fonts only | `BugReportData`, `ContextInfo` |

### 4.2 Layer Isolation

A strict layering rule is enforced across the codebase:

- `analyzer/` modules import **nothing** from Streamlit or fpdf2 — they are pure Python data-transformation functions.
- `reports/report_generator.py` does **not** import from `analyzer/` — it accepts plain `list` parameters to avoid circular imports.
- `app.py` is the **only** integration layer, importing from all modules and wiring them together.

This means the entire analysis pipeline can be called, tested, and replaced without touching the UI.

### 4.3 State Management

Streamlit re-runs the entire script on every interaction. FixFlow uses `st.session_state` for two purposes:

| Key | Type | Purpose |
|---|---|---|
| `pdf_bytes` | `bytes` | Persist the generated PDF across reruns so the download button stays visible |
| `pdf_ready` | `bool` | Gate the download section rendering |
| `ff_authenticated` | `bool` | Auth gate flag |
| `ff_current_user` | `str` | Email of the logged-in user |
| `ff_auth_view` | `str` | Which auth screen is active: `"login"` / `"signup"` / `"forgot"` |
| `ff_users` | `dict` | In-session credential store `{email: sha256_hash}` |

---

## 5. Features & Implementation

### 5.1 Error Detection

**File:** `analyzer/detector.py`

The detector scans a log string for 26 known Python exception names using pre-compiled word-boundary regex patterns (`\bExceptionName\b`). Each match records the 1-based line numbers where the exception name appears.

**Catalogue of detected exceptions (26 total):**

| Severity | Exceptions |
|---|---|
| **High** | `SyntaxError`, `IndentationError`, `ModuleNotFoundError`, `ImportError`, `RecursionError`, `MemoryError` |
| **Medium** | `NameError`, `UnboundLocalError`, `TypeError`, `AttributeError`, `RuntimeError`, `NotImplementedError`, `PermissionError`, `FileNotFoundError`, `ConnectionError`, `TimeoutError`, `OSError`, `IOError` |
| **Low** | `IndexError`, `KeyError`, `ValueError`, `ZeroDivisionError`, `AssertionError`, `StopIteration`, `OverflowError`, `Exception` |

A deduplication rule removes the generic `Exception` entry when any more-specific error is also detected, preventing noise in results.

Results are returned as `DetectedError` dataclasses, each carrying the error name, emoji, short description, line numbers, and a linked `ErrorAdvice` object.

---

### 5.2 Plain-English Advice

**File:** `analyzer/advice.py`

For every detected error type, FixFlow looks up a pre-authored `ErrorAdvice` entry containing four fields:

| Field | Content |
|---|---|
| `explanation` | Plain-English description of what the exception means |
| `root_cause` | The single most likely reason it was raised |
| `steps` | An ordered list of numbered fix actions |
| `example_fix` | A before/after Python code snippet demonstrating the fix |

Full advice entries exist for all 26 exception types. The `get_advice()` function is intentionally the **single designated replacement point** for future AI-generated advice — swapping the dict lookup for an IBM Bob API call requires changing exactly this one function, with no changes to callers.

---

### 5.3 Repository Context Analysis

**File:** `analyzer/repo_context.py`

When the user supplies their project's Python source files (via upload or local path), FixFlow cross-references the traceback against them using a two-step pipeline:

**Step 1 — Traceback frame parsing**

A regex (`File "path", line N, in function`) extracts every stack frame from the traceback, recording the raw path, basename, line number, and function name. Frames from the Python standard library or installed packages are filtered out using a set of well-known path prefixes.

**Step 2 — File matching + AST function resolution**

The remaining user-owned frames are matched against the uploaded files using:

1. **Exact match** (case-insensitive basename) → **High** confidence
2. **Stem match** (e.g. `utils` matches `utils.py`) → **Medium** confidence

When a match is found, the Python `ast` module walks the matched source file to identify the innermost function that contains the reported line number. A ±3-line code snippet is extracted and displayed alongside the match.

Results are `ContextMatch` dataclasses, ordered innermost-first (highest-confidence crash site first).

---

### 5.4 PDF Bug Report Generation

**File:** `reports/report_generator.py`

On every successful analysis, FixFlow builds a PDF report and stores it in `st.session_state` so the download button persists across Streamlit reruns. The report is generated entirely in memory using `fpdf2` — no temporary files, no system font installation required.

**Report contents:**

| Section | Content |
|---|---|
| Header | IBM Bob 2.0 Hackathon badge |
| Metadata table | Report ID (e.g. `FF-2025-4821`), Generated By, Generated On, Severity |
| Error banner | Detected error type with orange callout bar |
| Error message | Last non-empty line of the raw traceback |
| What does this mean? | Plain-English explanation |
| Most Likely Root Cause | Amber callout box |
| Step-by-Step Fix | Numbered steps with blue accent numbers |
| Example Fix | Dark-background monospace code block |
| Repository Context | One callout row per matched file (when available) |
| Raw Error Log | Truncated to 1,500 characters in a dark code block |
| Footer | "FixFlow Bug Report · Page N" |

A `_safe()` function handles the `fpdf2` latin-1 character limitation — all text is sanitised before rendering to prevent crashes on em-dashes, curly quotes, or other Unicode characters.

---

### 5.5 Authentication

**File:** `auth.py`

A lightweight session-based authentication gate was added in Milestone 7. All credentials are stored in `st.session_state` for the current browser session — there is no database or file storage.

**Three screens:**

| Screen | Behaviour |
|---|---|
| **Login** | Validates email + SHA-256(password) against the in-session user registry |
| **Sign Up** | Creates a new entry in the registry; enforces minimum 6-character password and duplicate-email check |
| **Forgot Password** | Resets the stored hash for any registered email |

A built-in demo account (`demo@fixflow.ai` / `fixflow2025`) is always pre-registered. The gate uses `st.stop()` to halt script execution — all existing app features are downstream and unaffected.

---

### 5.6 Dual Input Mode

Users can provide an error log in two ways:

- **File upload** — drag-and-drop or file picker accepting `.txt` files; decoded from bytes with UTF-8 fallback to latin-1
- **Text area paste** — direct traceback paste with a live placeholder example

If both are provided, the uploaded file takes precedence.

---

### 5.7 Severity Classification

Every detected error is rated **High**, **Medium**, or **Low** based on a static severity map in `reports/report_generator.py`. The rating appears in:

- The PDF metadata table with a colour swatch
- The PDF error banner background colour (red / orange / yellow)

The classification logic: High = errors that prevent the program from starting; Medium = runtime crashes that are fixable in code; Low = logic errors that are typically caught and handled.

---

### 5.8 Dark Theme UI

The entire UI is styled via a single `st.markdown(..., unsafe_allow_html=True)` block at the top of `app.py`. All styles use CSS custom properties (`--bg-page`, `--purple`, `--border`, etc.) defined in a `:root` block, making theme-wide changes a one-line edit.

Custom CSS classes use a consistent `ff-` prefix: `ff-err-card`, `ff-step`, `ff-ctx-card`, `ff-badge`, `ff-dl-card`, etc.

---

## 6. Technology Stack

| Layer | Technology | Version | Why |
|---|---|---|---|
| **UI** | [Streamlit](https://streamlit.io/) | ≥ 1.35.0 | Rapid Python-native web app; no HTML/JS boilerplate |
| **PDF generation** | [fpdf2](https://py-pdf.github.io/fpdf2/) | ≥ 2.7.9 | Pure Python, zero system dependencies, works in any deploy env |
| **Error detection** | Python `re` | stdlib | Pre-compiled word-boundary patterns; no external NLP needed |
| **AST analysis** | Python `ast` | stdlib | Walk source files to find the function at a given line number |
| **Auth hashing** | Python `hashlib` | stdlib | SHA-256 for in-session credential storage |
| **Path handling** | Python `pathlib` | stdlib | Cross-platform file paths for local directory scan |
| **Language** | Python | 3.10+ | Type hints (`X \| Y` union syntax), `dataclasses`, `from __future__ import annotations` |

**Total runtime dependencies: 2** (`streamlit`, `fpdf2`). Everything else is Python standard library.

---

## 7. Project Structure

```
FixFlow/
│
├── app.py                        # Streamlit entry point — UI, orchestration, CSS theme
├── auth.py                       # Session-based login / sign-up / forgot-password
├── requirements.txt              # streamlit>=1.35.0, fpdf2>=2.7.9
│
├── analyzer/                     # Core analysis logic — zero Streamlit / I/O imports
│   ├── __init__.py
│   ├── detector.py               # Regex scanner → DetectedError dataclasses
│   ├── parser.py                 # Public entry point: analyze_log() + parse_uploaded_file()
│   ├── advice.py                 # Rule-based advice DB (AI swap point: get_advice())
│   ├── repo_context.py           # Traceback parser + AST matcher → ContextMatch dataclasses
│   └── fixer.py                  # Stub — reserved for IBM Bob API integration
│
├── reports/
│   ├── __init__.py
│   └── report_generator.py      # fpdf2 PDF builder: BugReportData → bytes
│
├── assets/
│   └── screenshots/             # UI screenshots (01_home, 02_error_card, 03_repo_context)
│
├── bob_sessions/                # IBM Bob session logs for each milestone
│   ├── task01_init.md
│   ├── task01_setup_m1_m2.md
│   └── ...
│
├── AGENTS.md                    # AI assistant coding guidance
├── REPORT.md                    # This document
└── .bob/                        # IBM Bob mode-specific rules
    ├── rules-agent/AGENTS.md
    ├── rules-ask/AGENTS.md
    └── rules-plan/AGENTS.md
```

---

## 8. User Flow

```
┌─────────────────────────────────────────────────────────────┐
│                      BROWSER SESSION                        │
│                                                             │
│  ┌──────────────┐   Login / Sign Up / Forgot Password       │
│  │  auth.py     │──────────────────────────────────────┐    │
│  └──────────────┘                                       │    │
│         │ authenticated                                 │    │
│         ▼                                               ▼    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    app.py (FixFlow UI)                │   │
│  │                                                      │   │
│  │  1. Upload .txt error log  OR  paste traceback       │   │
│  │  2. (Optional) Upload .py files / enter repo path    │   │
│  │  3. Click Analyze                                    │   │
│  │                                                      │   │
│  │  ┌──────────────┐   ┌───────────────────────────┐   │   │
│  │  │ detector.py  │──▶│ advice.py (get_advice())  │   │   │
│  │  └──────────────┘   └───────────────────────────┘   │   │
│  │         │                                            │   │
│  │  ┌──────────────┐                                   │   │
│  │  │repo_context  │ (if project files supplied)        │   │
│  │  └──────────────┘                                   │   │
│  │         │                                            │   │
│  │  ┌──────────────────────┐                           │   │
│  │  │ report_generator.py  │──▶ PDF bytes in           │   │
│  │  └──────────────────────┘    session_state          │   │
│  │                                                      │   │
│  │  4. View results (error cards + repo context)        │   │
│  │  5. Download PDF Bug Report                          │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 9. Development Journey

The project was built milestone by milestone using IBM Bob 2.0 as the primary coding assistant. Each milestone added a complete, working feature layer on top of the previous one.

| Milestone | Feature Delivered | Key Files |
|---|---|---|
| **M1** | Project scaffolding — `app.py` skeleton, Streamlit page config, dark CSS theme | `app.py` |
| **M2** | File upload widget + text-area paste input; `.txt` decoding with UTF-8/latin-1 fallback | `analyzer/parser.py` |
| **M3** | Rule-based error detection (26 exceptions); `DetectedError` dataclass; plain-English advice DB | `analyzer/detector.py`, `analyzer/advice.py` |
| **M4** | Repository context mode — traceback frame parsing, AST-based file matching, code snippet extraction | `analyzer/repo_context.py` |
| **M5** | PDF bug report generation — full fpdf2 builder, severity classification, `BugReportData` contract | `reports/report_generator.py` |
| **M6** | UI polish — error cards, advice sub-sections, context cards, download card, responsive CSS | `app.py` (CSS block) |
| **M7** | Login gate — sign-up, forgot-password, SHA-256 credential storage, logout button | `auth.py` |

---

## 10. IBM Bob Integration

### 10.1 Role in Development

IBM Bob 2.0 served as the primary coding assistant throughout the entire project lifecycle:

- **Architecture decisions** — module boundaries, layer isolation, circular-import prevention
- **Code generation** — all seven modules were scaffolded and implemented with Bob's assistance
- **Code review** — each milestone was reviewed for correctness, style (ruff), and type safety (mypy) before commit
- **Debugging** — edge cases in the traceback parser and fpdf2 latin-1 handling were identified and resolved with Bob
- **Documentation** — `AGENTS.md` and mode-specific `.bob/rules-*/AGENTS.md` files were maintained to give Bob accurate project context across sessions

### 10.2 Planned API Integration

`analyzer/fixer.py` is the designated stub for IBM Bob API integration. The planned flow:

```
detect_errors(log_text)          ← already live (rule-based)
        │
        ▼
get_advice(error_name)           ← TODAY: dict lookup in advice.py
                                   FUTURE: IBM Bob API call
        │  Send: error_name + raw traceback + repo context
        │  Receive: AI-generated explanation, root cause,
        │           tailored fix steps, example code
        ▼
generate_pdf(report_data)        ← unchanged; same BugReportData contract
```

The `get_advice()` function signature and `ErrorAdvice` return type are intentionally frozen — the entire UI and PDF pipeline will continue working without modification after the AI swap.

---

## 11. Future Roadmap

| Priority | Feature | Notes |
|---|---|---|
| 🔴 **High** | IBM Bob AI explanations | Replace `get_advice()` dict with a Bob API call; all callers unchanged |
| 🔴 **High** | Multi-language support | Extend `_ERROR_CATALOGUE` and advice DB to JavaScript, Java, Go exceptions |
| 🟠 **Medium** | Fix auto-apply | Generate a unified diff and write patched files back to disk |
| 🟠 **Medium** | CI/CD integration | GitHub Action that runs FixFlow on test failures and posts analysis as a PR comment |
| 🟠 **Medium** | Session history | Persist past analyses with a lightweight SQLite or JSON store |
| 🟡 **Low** | VS Code extension | Run FixFlow analysis from inside the editor via a command palette action |
| 🟡 **Low** | Slack / Teams bot | Post a traceback in chat and receive the fix report inline |
| 🟡 **Low** | Team dashboard | Aggregate error frequency and type statistics across a project over time |

---

## 12. Team

| Member | Contribution |
|---|---|
| **Impana** | Project lead, architecture, full-stack implementation |
| **Harshitha G** | Co-development, testing, UI design |

> Built with ❤️ at the **IBM Bob 2.0 Hackathon**  
> Powered by [IBM Bob](https://www.ibm.com/) · [Streamlit](https://streamlit.io/) · [fpdf2](https://py-pdf.github.io/fpdf2/)

---

*FixFlow v1.0 · IBM Bob 2.0 Hackathon · MIT License*
