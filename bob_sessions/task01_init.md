# /init

---

**Status:** active  **Date:** 2026-09-25

---

### 👤 User

<task>
Please analyze this codebase and create an AGENTS.md file containing:
1. Build/lint/test commands - especially for running a single test
2. Code style guidelines including imports, formatting, types, naming conventions, error handling, etc.
</task>

<initialization>
  <purpose>
    Create (or update) a concise AGENTS.md file that enables immediate productivity for AI assistants.
    Focus ONLY on project-specific, non-obvious information that you had to discover by reading files.

    CRITICAL: Only include information that is:
    - Non-obvious (couldn't be guessed from standard practices)
    - Project-specific (not generic to the framework/language)
    - Discovered by reading files (config files, code patterns, custom utilities)
    - Essential for avoiding mistakes or following project conventions

    Usage notes:
    - The file you create will be given to agentic coding agents (such as yourself) that operate in this repository
    - Keep the main AGENTS.md concise - aim for about 20 lines, but use more if the project complexity requires it
    - If there's already an AGENTS.md, improve it
    - If there are Claude Code rules (in CLAUDE.md), Cursor rules (in .cursor/rules/ or .cursorrules), or Copilot rules (in .github/copilot-instructions.md), make sure to include them
    - Be sure to prefix the file with: "# AGENTS.md\n\nThis file provides guidance to agents when working with code in this repository."
  </purpose>

  <todo_list_creation>
    If the update_todo_list tool is available, create a todo list with these focused analysis steps:

    1. Check for existing AGENTS.md files
       CRITICAL - Check these EXACT paths IN THE PROJECT ROOT:
       - AGENTS.md (in project root directory)
       - .bob/rules-agent/AGENTS.md (relative to project root)
       - .bob/rules-ask/AGENTS.md (relative to project root)
       - .bob/rules-plan/AGENTS.md (relative to project root)

       IMPORTANT: All paths are relative to the project/workspace root, NOT system root!

       If ANY of these exist:
       - Read them thoroughly
       - CRITICALLY EVALUATE: Remove ALL obvious information
       - DELETE entries that are standard practice or framework defaults
       - REMOVE anything that could be guessed without reading files
       - Only KEEP truly non-obvious, project-specific discoveries
       - Then add any new non-obvious patterns you discover

       Also check for other AI assistant rules:
       - .cursorrules, CLAUDE.md, .roorules
       - .cursor/rules/, .github/copilot-instructions.md

    2. Identify stack
       - Language, framework, build tools
       - Package manager and dependencies

    3. Extract commands
       - Build, test, lint, run
       - Critical directory-specific commands

    4. Map core architecture
       - Main components and flow
       - Key entry points

    5. Document critical patterns
       - Project-specific utilities (that you discovered by reading code)
       - Non-standard approaches (that differ from typical patterns)
       - Custom conventions (that aren't obvious from file structure)

    6. Extract code style
       - From config files only
       - Key conventions

    7. Testing specifics
       - Framework and run commands
       - Directory requirements

    8. Compile/Update AGENTS.md files
       - If files exist: AGGRESSIVELY clean them up
         * DELETE all obvious information (even if it was there before)
         * REMOVE standard practices, framework defaults, common patterns
         * STRIP OUT anything derivable from file structure or names
         * ONLY KEEP truly non-obvious discoveries
         * Then add newly discovered non-obvious patterns
         * Result should be SHORTER and MORE FOCUSED than before
       - If creating new: Follow the non-obvious-only principle
       - Create mode-specific files in .bob/rules-*/ directories (IN PROJECT ROOT)

    Note: If update_todo_list is not available, proceed with the analysis workflow directly without creating a todo list.
  </todo_list_creation>
</initialization>

<analysis_workflow>
  Follow the comprehensive analysis workflow to:

  1. **Discovery Phase**:
     CRITICAL - First check for existing AGENTS.md files at these EXACT locations IN PROJECT ROOT:
     - AGENTS.md (in project/workspace root)
     - .bob/rules-agent/AGENTS.md (relative to project root)
     - .bob/rules-ask/AGENTS.md (relative to project root)
     - .bob/rules-plan/AGENTS.md (relative to project root)

     IMPORTANT: The .bob folder should be created in the PROJECT ROOT, not system root!

     If found, perform CRITICAL analysis:
     - What information is OBVIOUS and must be DELETED?
     - What violates the non-obvious-only principle?
     - What would an experienced developer already know?
     - DELETE first, then consider what to add
     - The file should get SHORTER, not longer

     Also find other AI assistant rules and documentation

  2. **Project Identification**: Identify language, stack, and build system
  3. **Command Extraction**: Extract and verify essential commands
  4. **Architecture Mapping**: Create visual flow diagrams of core processes
  5. **Component Analysis**: Document key components and their interactions
  6. **Pattern Analysis**: Identify project-specific patterns and conventions
  7. **Code Style Extraction**: Extract formatting and naming conventions
  8. **Security & Performance**: Document critical patterns if relevant
  9. **Testing Discovery**: Understand testing setup and practices
  10. **Example Extraction**: Find real examples from the codebase
</analysis_workflow>

<output_structure>
  <main_file>
    Create or deeply improve AGENTS.md with ONLY non-obvious information:

    If AGENTS.md exists:
    - FIRST: Delete ALL obvious information
    - REMOVE: Standard commands, framework defaults, common patterns
    - STRIP: Anything that doesn't require file reading to know
    - EVALUATE: Each line - would an experienced dev be surprised?
    - If not surprised, DELETE IT
    - THEN: Add only truly non-obvious new discoveries
    - Goal: File should be SHORTER and MORE VALUABLE

    Content should include:
    - Header: "# AGENTS.md\n\nThis file provides guidance to agents when working with code in this repository."
    - Build/lint/test commands - ONLY if they differ from standard package.json scripts
    - Code style - ONLY project-specific rules not covered by linter configs
    - Custom utilities or patterns discovered by reading the code
    - Non-standard directory structures or file organizations
    - Project-specific conventions that violate typical practices
    - Critical gotchas that would cause errors if not followed

    EXCLUDE obvious information like:
    - Standard npm/yarn commands visible in package.json
    - Framework defaults (e.g., "React uses JSX")
    - Common patterns (e.g., "tests go in __tests__ folders")
    - Information derivable from file extensions or directory names

    Keep it concise (aim for ~20 lines, but expand as needed for complex projects).
    Include existing AI assistant rules from CLAUDE.md, Cursor rules (.cursor/rules/ or .cursorrules), or Copilot rules (.github/copilot-instructions.md).
  </main_file>

  <mode_specific_files>
    Create or deeply improve mode-specific AGENTS.md files IN THE PROJECT ROOT.

    CRITICAL: For each of these paths (RELATIVE TO PROJECT ROOT), check if the file exists FIRST:
    - .bob/rules-agent/AGENTS.md (relative to project root)
    - .bob/rules-ask/AGENTS.md (relative to project root)
    - .bob/rules-plan/AGENTS.md (relative to project root)

    IMPORTANT: The .bob directory must be created in the current project/workspace root directory,
    NOT at the system root (/) or home directory. All paths are relative to where the project is located.

    If files exist:
    - AGGRESSIVELY DELETE obvious information
    - Remove EVERYTHING that's standard practice
    - Strip out framework defaults and common patterns
    - Each remaining line must be surprising/non-obvious
    - Only then add new non-obvious discoveries
    - Files should become SHORTER, not longer

    Example structure (ALL IN PROJECT ROOT):
    ```
    project-root/
    ├── AGENTS.md                    # General project guidance
    ├── .bob/                        # IN PROJECT ROOT, NOT SYSTEM ROOT!
    │   ├── rules-agent/
    │   │   └── AGENTS.md           # Advance mode specific instructions
    │   ├── rules-ask/
    │   │   └── AGENTS.md           # Ask mode specific instructions
    │   └── rules-plan/
    │       └── AGENTS.md           # Plan mode specific instructions
    ├── src/
    ├── package.json
    └── ... other project files
    ```

    .bob/rules-agent/AGENTS.md - ONLY non-obvious advance coding rules discoveries:
    - Custom utilities that replace standard approaches
    - Non-standard patterns unique to this project
    - Hidden dependencies or coupling between components
    - Required import orders or naming conventions not enforced by linters
    - Access to tools like MCP and Browser

    Example of non-obvious rules worth documenting:
    ```
    # Project Coding Rules (Non-Obvious Only)
    - Always use safeWriteJson() from src/utils/ instead of JSON.stringify for file writes (prevents corruption)
    - API retry mechanism in src/api/providers/utils/ is mandatory (not optional as it appears)
    - Database queries MUST use the query builder in packages/evals/src/db/queries/ (raw SQL will fail)
    - Provider interface in packages/types/src/ has undocumented required methods
    - Test files must be in same directory as source for vitest to work (not in separate test folder)
    ```

    .bob/rules-ask/AGENTS.md - ONLY non-obvious documentation context:
    - Hidden or misnamed documentation
    - Counterintuitive code organization
    - Misleading folder names or structures
    - Important context not evident from file structure

    Example of non-obvious documentation rules worth documenting:
    ```
    # Project Documentation Rules (Non-Obvious Only)
    - "src/" contains VSCode extension code, not source for web apps (counterintuitive)
    - Provider examples in src/api/providers/ are the canonical reference (docs are outdated)
    - UI runs in VSCode webview with restrictions (no localStorage, limited APIs)
    - Package.json scripts must be run from specific directories, not root
    - Locales in root are for extension, webview-ui/src/i18n for UI (two separate systems)
    ```

    .bob/rules-plan/AGENTS.md - ONLY non-obvious architectural constraints:
    - Hidden coupling between components
    - Undocumented architectural decisions
    - Non-standard patterns that must be followed
    - Performance bottlenecks discovered through investigation

    Example of non-obvious architecture rules worth documenting:
    ```
    # Project Architecture Rules (Non-Obvious Only)
    - Providers MUST be stateless - hidden caching layer assumes this
    - Webview and extension communicate through specific IPC channel patterns only
    - Database migrations cannot be rolled back - forward-only by design
    - React hooks required because external state libraries break webview isolation
    - Monorepo packages have circular dependency on types package (intentional)
    ```
  </mode_specific_files>
</output_structure>

<quality_criteria>
  - ONLY include non-obvious information discovered by reading files
  - Exclude anything that could be guessed from standard practices
  - Focus on gotchas, hidden requirements, and counterintuitive patterns
  - Include specific file paths when referencing custom utilities
  - Be extremely concise - if it's obvious, don't include it
  - Every line should prevent a potential mistake or confusion
  - Test: Would an experienced developer be surprised by this information?
  - If updating existing files: DELETE obvious info first, files should get SHORTER
  - Measure success: Is the file more concise and valuable than before?
</quality_criteria>

Remember: The goal is to create documentation that enables AI assistants to be immediately productive in this codebase, focusing on project-specific knowledge that isn't obvious from the code structure alone.

---

### 🤖 Assistant

> 🔧 called: update_todo_list



> 🔧 **update_todo_list** — 
[-] Check for existing AGENTS.md and AI assistant rules files
[ ] Identify stack, language, framework, build tools
[ ] Extract commands (build, test, lint, run)
[ ] Map core architecture and entry points
[ ] Document critical patterns and code style
[ ] Compile AGENTS.md and mode-specific files


### 🤖 Assistant

> 🔧 called: glob, glob, glob



> 🔧 **glob** — .bob/rules-*/AGENTS.md

> 🔧 **glob** — {CLAUDE.md,.cursorrules,.roorules,.github/copilot-instructions.md}

> 🔧 **glob** — AGENTS.md

### 🤖 Assistant

> 🔧 called: list_files



> 🔧 **list_files** — .

### 🤖 Assistant

> 🔧 called: read_file



> 🔧 **read_file** — README.md

### 🤖 Assistant

> 🔧 called: read_file

The repository has virtually no code yet — just a README and `.gitignore`. Let me check `.gitignore` for any hints about the intended stack, and also explore if there's anything deeper.

> 🔧 **read_file** — .gitignore

### 🤖 Assistant

> 🔧 called: update_todo_list



> 🔧 **update_todo_list** — 
[x] Check for existing AGENTS.md and AI assistant rules files
[-] Identify stack, language, framework, build tools
[ ] Extract commands (build, test, lint, run)
[ ] Map core architecture and entry points
[ ] Document critical patterns and code style
[ ] Compile AGENTS.md and mode-specific files


### 🤖 Assistant

> 🔧 called: update_todo_list

The repository is a **Python** project (based on the `.gitignore` which includes Python-specific patterns: `__pycache__`, pytest, ruff, mypy, etc.) named **FixFlow** — an AI Bug-to-Fix Assistant built for the IBM Bob 2.0 Hackathon. It is essentially empty at this stage (only README + .gitignore committed).

Key stack signals from `.gitignore`:
- **Language**: Python
- **Package managers hinted**: pip, uv, poetry, pdm, pipenv (uv most modern)
- **Test runner**: pytest (`.pytest_cache/` ignored)
- **Linter**: ruff (`.ruff_cache/` ignored)
- **Type checker**: mypy (`.mypy_cache/` ignored)
- **Frameworks hinted**: Django, Flask, Streamlit (`.streamlit/secrets.toml` ignored), Marimo
- **Infrastructure hinted**: Redis (`.rdb`), RabbitMQ, ActiveMQ, Celery
- **Virtual env**: `.venv` (standard)

> 🔧 **update_todo_list** — 
[x] Check for existing AGENTS.md and AI assistant rules files
[x] Identify stack, language, framework, build tools
[x] Extract commands (build, test, lint, run)
[x] Map core architecture and entry points
[x] Document critical patterns and code style
[-] Compile AGENTS.md and mode-specific files


### 🤖 Assistant

> 🔧 called: write_file

Now I'll create the AGENTS.md and mode-specific files. Since the project is at inception with no source code yet, the AGENTS.md should document what's known from the gitignore signals and leave room for future additions.

> 🔧 **write_file** — AGENTS.md

### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — .bob/rules-agent/AGENTS.md

### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — # Ask Mode Rules

This file provides guidance to agents when working with code in this repository.

## Documentation Context (Non-Obvious)

- **FixFlow** is an IBM Bob 2.0 Hackathon project — "IBM Bob" refers to the IBM AI coding assistant platform, not an individual.
- The project is at **inception** (only README + .gitignore exist) — no architecture docs or source to reference yet.
- Stack signals come entirely from `.gitignore` patterns — treat them as intent, not fact, until `pyproject.toml` exists.
- Streamlit and Flask/Django are both hinted in `.gitignore`; the actual chosen framework is not yet committed.
- Redis/Celery/RabbitMQ/ActiveMQ ignore entries suggest planned async or messaging components, but none are implemented.


### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — # Plan Mode Rules

This file provides guidance to agents when working with code in this repository.

## Architectural Constraints (Non-Obvious)

- **Project is empty** — no coupling, no modules, no DB schema yet. Architecture is greenfield.
- `.gitignore` reveals planned infrastructure: Redis (cache/broker), Celery (task queue), RabbitMQ or ActiveMQ (message broker). Plan for async from the start if these are needed.
- Both Streamlit and Flask/Django are gitignored — choose one UI framework and commit to it; mixing them is a smell.
- `uv` is the implied package manager; plan `pyproject.toml` as the single source of truth for deps, scripts, and tool config (`[tool.ruff]`, `[tool.mypy]`, `[tool.pytest.ini_options]`).
- Hackathon context: IBM Bob 2.0 — the AI assistant platform may provide tools/APIs; plan integration points accordingly.
- Secrets architecture: `.env` for local, `.streamlit/secrets.toml` for Streamlit deploy — plan for both from day one.


### 🤖 Assistant

> 🔧 called: update_todo_list



> 🔧 **update_todo_list** — 
[x] Check for existing AGENTS.md and AI assistant rules files
[x] Identify stack, language, framework, build tools
[x] Extract commands (build, test, lint, run)
[x] Map core architecture and entry points
[x] Document critical patterns and code style
[x] Compile AGENTS.md and mode-specific files


### 🤖 Assistant

Four files created. Here's what was discovered and documented:

---

### What the analysis found

The repository is essentially **empty** (only [`README.md`](README.md) and [`.gitignore`](.gitignore) exist). All stack signals were reverse-engineered from `.gitignore` patterns:

| Signal | Evidence |
|---|---|
| Python | `__pycache__`, `*.py[codz]`, pytest/mypy/ruff cache dirs |
| **uv** preferred | Dedicated `# UV` section in `.gitignore` (above pip/poetry/pdm) |
| **pytest** for tests | `.pytest_cache/` ignored |
| **ruff** for lint+format | `.ruff_cache/` ignored |
| **mypy** for types | `.mypy_cache/` ignored |
| Streamlit likely UI | `.streamlit/secrets.toml` ignored |
| Async infra planned | Redis, Celery, RabbitMQ, ActiveMQ all ignored |

### Files created

- [`AGENTS.md`](AGENTS.md) — general project guidance with inferred stack + commands
- [`.bob/rules-agent/AGENTS.md`](.bob/rules-agent/AGENTS.md) — coding gotchas (uv preference, ruff over black/isort, secrets handling, single-test command)
- [`.bob/rules-ask/AGENTS.md`](.bob/rules-ask/AGENTS.md) — documentation context (stack is intent-not-fact, IBM Bob platform note)
- [`.bob/rules-plan/AGENTS.md`](.bob/rules-plan/AGENTS.md) — architectural constraints (greenfield, planned async infra, single `pyproject.toml` approach)

> **Note**: Once you scaffold `pyproject.toml` and add source files, update `AGENTS.md` with actual commands, module structure, and confirmed framework choices.

---

### 👤 User

We are a 2-member team building FixFlow – AI Bug-to-Fix Assistant for the IBM Bob 2.0 Hackathon.
Milestone 1: Create a clean Streamlit project structure.
Requirements:
Create app.py
Create requirements.txt
Create folders: analyzer, assets, reports, bob_sessions
Add placeholder files where necessary.
Create a simple Streamlit home page with:
Title: FixFlow – AI Bug-to-Fix Assistant
Short description of the problem
An "Upload Error Log" section (UI only for now)
A clean professional layout
Don't implement the error analysis yet. Focus only on setting up a well-organized MVP foundation for the hackathon.

---

### 🤖 Assistant

> 🔧 called: update_todo_list



> 🔧 **update_todo_list** — 
[-] Create project structure (folders + placeholder files)
[ ] Create requirements.txt
[ ] Create app.py with Streamlit home page
[ ] Update AGENTS.md with confirmed stack


### 🤖 Assistant

> 🔧 called: update_todo_list



> 🔧 **update_todo_list** — 
[x] Check for existing AGENTS.md and AI assistant rules files
[x] Identify stack, language, framework, build tools
[x] Extract commands (build, test, lint, run)
[x] Map core architecture and entry points
[x] Document critical patterns and code style
[x] Compile AGENTS.md and mode-specific files
[-] Create project structure (folders + placeholder files)
[ ] Create requirements.txt
[ ] Create app.py with Streamlit home page
[ ] Update AGENTS.md with confirmed stack


### 🤖 Assistant

> 🔧 called: write_file, write_file, write_file, write_file, write_file, write_file

Creating all folders and placeholder files in parallel:

> 🔧 **write_file** — analyzer/__init__.py

> 🔧 **write_file** — analyzer/fixer.py

> 🔧 **write_file** — analyzer/parser.py

> 🔧 **write_file** — assets/.gitkeep

> 🔧 **write_file** — reports/.gitkeep

> 🔧 **write_file** — bob_sessions/.gitkeep

### 🤖 Assistant

> 🔧 called: update_todo_list



> 🔧 **update_todo_list** — 
[x] Check for existing AGENTS.md and AI assistant rules files
[x] Identify stack, language, framework, build tools
[x] Extract commands (build, test, lint, run)
[x] Map core architecture and entry points
[x] Document critical patterns and code style
[x] Compile AGENTS.md and mode-specific files
[x] Create project structure (folders + placeholder files)
[-] Create requirements.txt
[ ] Create app.py with Streamlit home page
[ ] Update AGENTS.md with confirmed stack


### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — streamlit>=1.35.0


### 🤖 Assistant

> 🔧 called: update_todo_list



> 🔧 **update_todo_list** — 
[x] Check for existing AGENTS.md and AI assistant rules files
[x] Identify stack, language, framework, build tools
[x] Extract commands (build, test, lint, run)
[x] Map core architecture and entry points
[x] Document critical patterns and code style
[x] Compile AGENTS.md and mode-specific files
[x] Create project structure (folders + placeholder files)
[x] Create requirements.txt
[-] Create app.py with Streamlit home page
[ ] Update AGENTS.md with confirmed stack


### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — """
FixFlow – AI Bug-to-Fix Assistant
Streamlit home page (Milestone 1 – UI scaffold only).
"""

import streamlit as st

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FixFlow – AI Bug-to-Fix Assistant",
    page_icon="🔧",
    layout="centered",
    initial_sidebar_state="auto",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Subtle top accent bar */
    .main > div:first-child {
        padding-top: 2rem;
    }
    .stFileUploader label {
        font-weight: 600;
    }
    .badge {
        display: inline-block;
        background: #1a56db;
        color: #ffffff;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        padding: 2px 10px;
        border-radius: 999px;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .divider {
        border: none;
        border-top: 1px solid #e5e7eb;
        margin: 1.5rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<span class="badge">IBM Bob 2.0 Hackathon</span>', unsafe_allow_html=True)
st.title("🔧 FixFlow")
st.subheader("AI Bug-to-Fix Assistant")

st.markdown(
    """
    Debugging is the most time-consuming part of software development.
    **FixFlow** cuts that time dramatically by letting you paste or upload an error log
    and receive an AI-powered root-cause analysis with concrete fix suggestions —
    all powered by **IBM Bob**.

    > _Upload an error log → get a diagnosis → apply the fix._
    """
)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── How it works ──────────────────────────────────────────────────────────────
st.markdown("### How it works")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("#### 📂 1. Upload")
    st.caption("Drop in your error log, stack trace, or crash report.")
with col2:
    st.markdown("#### 🤖 2. Analyze")
    st.caption("IBM Bob reads the log and identifies root causes.")
with col3:
    st.markdown("#### ✅ 3. Fix")
    st.caption("Get actionable code-level fix suggestions instantly.")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Upload Error Log ──────────────────────────────────────────────────────────
st.markdown("### Upload Error Log")
st.caption(
    "Supported formats: plain text (`.txt`, `.log`), Python tracebacks, "
    "JSON crash reports. Max 5 MB."
)

uploaded_file = st.file_uploader(
    label="Drop your error log here",
    type=["txt", "log", "json"],
    accept_multiple_files=False,
    help="Select a log file from your machine. Analysis will run automatically.",
)

if uploaded_file is not None:
    st.info(
        f"**{uploaded_file.name}** uploaded successfully "
        f"({uploaded_file.size / 1024:.1f} KB). "
        "Analysis coming in the next milestone! 🚀",
        icon="📄",
    )
else:
    st.markdown(
        """
        <div style="
            border: 2px dashed #d1d5db;
            border-radius: 10px;
            padding: 2rem 1.5rem;
            text-align: center;
            color: #6b7280;
            font-size: 0.9rem;
            margin-top: 0.5rem;
        ">
            No file uploaded yet.<br>
            <span style="font-size: 1.5rem;">📋</span><br>
            Use the file picker above to get started.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.caption(
    "FixFlow v0.1 · Built with ❤️ for IBM Bob 2.0 Hackathon · "
    "Powered by [IBM Bob](https://www.ibm.com)"
)


### 🤖 Assistant

> 🔧 called: write_file

Now update AGENTS.md to reflect the confirmed stack:

> 🔧 **write_file** — # AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project

**FixFlow** — AI Bug-to-Fix Assistant, built for the IBM Bob 2.0 Hackathon. Streamlit + Python.

## Stack

- **Language**: Python, virtual environment at `.venv`
- **UI**: Streamlit (`app.py` is the single entry point)
- **Package manager**: pip (`requirements.txt`); uv also supported
- **Linter/formatter**: ruff
- **Type checker**: mypy
- **Test runner**: pytest

## Commands

```bash
# Install
pip install -r requirements.txt          # or: uv pip install -r requirements.txt

# Run app
streamlit run app.py

# Lint / format
ruff check .
ruff format .

# Type check
mypy .

# Run a single test
pytest path/to/test_file.py::TestClass::test_method
```

## Project Layout

```
app.py                  # Streamlit entry point (home page)
requirements.txt        # Runtime dependencies
analyzer/
  __init__.py
  parser.py             # TODO: log parsing logic
  fixer.py              # TODO: IBM Bob API integration
assets/                 # Static assets (images, CSS overrides)
reports/                # Generated fix reports (gitkeep placeholder)
bob_sessions/           # IBM Bob session data (gitkeep placeholder)
```

## Conventions

- All Streamlit page config (`set_page_config`) must be the **first** Streamlit call in any page file.
- Custom CSS is injected via `st.markdown(..., unsafe_allow_html=True)` — keep styles in the same file, not external CSS.
- Secrets (API keys) go in `.streamlit/secrets.toml` (gitignored) — access via `st.secrets["key"]`.
- `assets/`, `reports/`, `bob_sessions/` contain only `.gitkeep` now; remove `.gitkeep` when real files are added.

## Notes

- `tempCodeRunnerFile.py` is gitignored (VS Code Code Runner artefact — do not commit).
- `.env` / `.envrc` are also gitignored — use `.streamlit/secrets.toml` for Streamlit deployments.


### 🤖 Assistant

> 🔧 called: update_todo_list



> 🔧 **update_todo_list** — 
[x] Check for existing AGENTS.md and AI assistant rules files
[x] Identify stack, language, framework, build tools
[x] Extract commands (build, test, lint, run)
[x] Map core architecture and entry points
[x] Document critical patterns and code style
[x] Compile AGENTS.md and mode-specific files
[x] Create project structure (folders + placeholder files)
[x] Create requirements.txt
[x] Create app.py with Streamlit home page
[x] Update AGENTS.md with confirmed stack


### 🤖 Assistant

Milestone 1 is done. Here's everything that was created:

---

### Project structure

```
FixFlow/
├── app.py                  ← Streamlit home page
├── requirements.txt        ← streamlit>=1.35.0
├── AGENTS.md               ← updated with confirmed stack
├── analyzer/
│   ├── __init__.py
│   ├── parser.py           ← TODO stub: log parsing
│   └── fixer.py            ← TODO stub: Bob API integration
├── assets/                 ← .gitkeep (static assets)
├── reports/                ← .gitkeep (generated reports)
└── bob_sessions/           ← .gitkeep (Bob session data)
```

### Home page features ([`app.py`](app.py))

- **Title + badge** — "FixFlow" with an IBM Bob 2.0 Hackathon pill
- **Problem description** — concise elevator pitch + tagline
- **3-column "How it works"** — Upload → Analyze → Fix
- **Upload Error Log section** — `st.file_uploader` accepting `.txt`, `.log`, `.json`, with a friendly placeholder state and a success message when a file is picked
- **Custom CSS** — dashed upload placeholder, accent bar, dividers — no external dependencies
- **Footer** — version + hackathon credit

### To run

```bash
pip install -r requirements.txt
streamlit run app.py
```