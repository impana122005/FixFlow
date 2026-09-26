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

---

### 👤 User

Implement Milestone 2 without changing the existing UI.
Requirements:
Allow users to upload a .txt file containing a Python error log.
Allow users to paste an error into the text area.
When the Analyze button is clicked, read the input and detect common Python errors such as:
ModuleNotFoundError
NameError
TypeError
ValueError
IndexError
KeyError
AttributeError
SyntaxError
Display the detected error type.
Keep the code modular by creating logic inside the analyzer folder.
Do not use AI explanations yet. Return simple rule-based detection with clean Streamlit output.

---

### 🤖 Assistant

> 🔧 called: read_file, read_file



> 🔧 **read_file** — app.py

> 🔧 **read_file** — analyzer/parser.py

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
[-] Implement analyzer/parser.py — rule-based error detection
[ ] Implement analyzer/detector.py — error type definitions & matching logic
[ ] Update app.py — add text area, Analyze button, results display


### 🤖 Assistant

> 🔧 called: write_file

I'll build the detection logic in `analyzer/` as a clean two-module split — `detector.py` holds the rules, `parser.py` orchestrates the extraction — then wire it into `app.py`.

> 🔧 **write_file** — """
analyzer/detector.py

Rule-based Python error detector.
Scans a log string for known Python exception names and returns structured results.
No AI or external calls — pure regex pattern matching.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

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
                    found[name] = DetectedError(name=name, emoji=emoji, description=desc)
                found[name].lines.append(lineno)

    results = list(found.values())

    # If both a specific error AND the generic "Exception" are present,
    # drop "Exception" to avoid noise — it almost always appears alongside.
    if len(results) > 1 and any(e.name != "Exception" for e in results):
        results = [e for e in results if e.name != "Exception"]

    return results


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
[x] Implement analyzer/detector.py — error type definitions & matching logic
[-] Implement analyzer/parser.py — rule-based error detection
[ ] Update app.py — add text area, Analyze button, results display


### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — """
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


### 🤖 Assistant

> 🔧 called: apply_diff

Now update `app.py` — replace only the Upload section and add the analysis results section, leaving all existing UI intact:

> 🔧 **apply_diff** — app.py

### 🤖 Assistant

> 🔧 called: execute_command

Now verify the app runs without import errors:

> 🔧 **execute_command** — pip install streamlit --quiet; python -c "from analyzer.parser import analyze_log, parse_uploaded_file; from analyzer.detector import detect_errors; r = analyze_log('ModuleNotFoundError: No module named pandas\nNameError: name x is not defined'); print([e.name for e in r])"

### 🤖 Assistant

> 🔧 called: execute_command

Detection works correctly. Let me run a broader smoke test covering all 8 required error types:

> 🔧 **execute_command** — python -c "
from analyzer.parser import analyze_log

sample = '''
Traceback (most recent call last):
  File 'app.py', line 3, in <module>
    import pandas
ModuleNotFoundError: No module named 'pandas'
NameError: name 'x' is not defined
TypeError: unsupported operand type(s) for +: 'int' and 'str'
ValueError: invalid literal for int() with base 10: 'abc'
IndexError: list index out of range
KeyError: 'missing_key'
AttributeError: 'NoneType' object has no attribute 'split'
SyntaxError: invalid syntax
'''

results = analyze_log(sample)
for r in results:
    print(f'{r.emoji} {r.name} — lines: {r.lines}')
print(f'Total: {len(results)} errors detected')
"


### 🤖 Assistant

> 🔧 called: execute_command

That's just a Windows console encoding issue with emoji — not a code bug. Let me confirm without emoji:

> 🔧 **execute_command** — python -c "
from analyzer.parser import analyze_log

sample = 'ModuleNotFoundError: No module named pandas\nNameError: name x\nTypeError: wrong type\nValueError: bad value\nIndexError: out of range\nKeyError: missing\nAttributeError: no attr\nSyntaxError: bad syntax'

results = analyze_log(sample)
names = [r.name for r in results]
print(names)
expected = ['ModuleNotFoundError','NameError','TypeError','ValueError','IndexError','KeyError','AttributeError','SyntaxError']
assert all(e in names for e in expected), f'Missing: {set(expected)-set(names)}'
print('All 8 required error types detected correctly.')
"


### 🤖 Assistant

> 🔧 called: update_todo_list

All 8 pass. Mark everything done:

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
[x] Implement analyzer/detector.py — error type definitions & matching logic
[x] Implement analyzer/parser.py — rule-based error detection
[x] Update app.py — add text area, Analyze button, results display


### 🤖 Assistant

Milestone 2 is complete. Here's a summary of what was built:

---

### New files

**[`analyzer/detector.py`](analyzer/detector.py)**  
The rule engine. Holds a catalogue of 25 Python exception types (the 8 required + common extras). Each entry has a name, emoji, and plain-English description. Pre-compiled regex patterns scan the log line-by-line and return `DetectedError` dataclasses with the matched line numbers. A de-noising rule automatically drops the generic `Exception` if any more-specific error is also found.

**[`analyzer/parser.py`](analyzer/parser.py)** (replaced stub)  
Thin orchestration layer. `parse_uploaded_file()` safely decodes bytes (UTF-8 → Latin-1 fallback). `analyze_log()` is the single public entry point called by `app.py`.

---

### Changes to [`app.py`](app.py)

The existing header, description, and "How it works" section are **untouched**. The upload section was extended with:

| Addition | Detail |
|---|---|
| **Text area** | Paste a log directly; pre-filled with a `ModuleNotFoundError` example as placeholder |
| **Analyze button** | Primary-style, full-width; file input takes priority over text area |
| **Results section** | Orange left-border cards per detected error — shows name, description, line refs |
| **"No errors" state** | Green success banner when the log is clean |
| **Raw log expander** | Collapsible `st.code` block so the page stays uncluttered |

---

### To run

```bash
streamlit run app.py
```

---

### 👤 User

Continue the FixFlow project with Milestone 3.
Enhance the existing error detection without breaking current functionality.
Requirements:
For each detected Python error, show:
A plain-English explanation.
The most likely root cause.
Step-by-step fix suggestions.
A small "Example Fix" code snippet.
Keep the logic modular inside the analyzer folder.
Display the results in clean Streamlit cards.
Keep this rule-based for now, with code structured so AI integration can be added later.

---

### 🤖 Assistant

> 🔧 called: read_file, read_file



> 🔧 **read_file** — analyzer/detector.py

> 🔧 **read_file** — analyzer/parser.py

### 🤖 Assistant

> 🔧 called: read_file



> 🔧 **read_file** — app.py

### 🤖 Assistant

> 🔧 called: update_todo_list

Good — I have a clear picture of the full codebase. The plan:

1. **`analyzer/advice.py`** — new module, pure data: per-error `explanation`, `root_cause`, `steps`, `example_fix`. Structured as a dict keyed by error name so AI can later override by name.
2. **`analyzer/detector.py`** — extend `DetectedError` with the four new fields; populate them from `advice.py` during detection.
3. **`analyzer/parser.py`** — no change needed (interface stays stable).
4. **`app.py`** — replace only the card rendering block with rich cards; everything else untouched.

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
[x] Implement analyzer/detector.py — error type definitions & matching logic
[x] Implement analyzer/parser.py — rule-based error detection
[x] Update app.py — add text area, Analyze button, results display
[-] Create analyzer/advice.py — per-error explanation, root cause, steps, example fix
[ ] Extend DetectedError dataclass with new advice fields
[ ] Update app.py card rendering — rich cards with all 4 new fields


### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — """
analyzer/advice.py

Rule-based advice database for known Python errors.

Each entry maps an exception name to an ErrorAdvice object containing:
  - explanation : plain-English description of what the error means
  - root_cause  : the most likely reason it occurred
  - steps       : ordered list of fix steps (strings)
  - example_fix : a short before/after code snippet string

Design note: this module is intentionally self-contained and has no
Streamlit or I/O dependencies, making it straightforward to swap the
rule-based content for AI-generated advice in a later milestone.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ErrorAdvice:
    explanation: str
    root_cause: str
    steps: list[str]
    example_fix: str


# ---------------------------------------------------------------------------
# Advice database — add / edit entries here; keys must match exception names
# in analyzer/detector.py exactly.
# ---------------------------------------------------------------------------
ADVICE: dict[str, ErrorAdvice] = {

    "ModuleNotFoundError": ErrorAdvice(
        explanation=(
            "Python cannot locate a module you are trying to import. "
            "This usually means the package is not installed in the current environment, "
            "or the module name is misspelled."
        ),
        root_cause=(
            "The package is missing from the active virtual environment, "
            "or the import statement contains a typo."
        ),
        steps=[
            "Check the exact package name on PyPI (it may differ from the import name, "
            "e.g. `pip install Pillow` but `import PIL`).",
            "Install the missing package: `pip install <package-name>`.",
            "Confirm you are using the correct virtual environment: `which python` / `where python`.",
            "If the module is a local file, ensure it is on `sys.path` or in the same directory.",
        ],
        example_fix=(
            "# Before (raises ModuleNotFoundError)\n"
            "import pandas\n\n"
            "# Fix — install first, then import\n"
            "# $ pip install pandas\n"
            "import pandas as pd"
        ),
    ),

    "ImportError": ErrorAdvice(
        explanation=(
            "The module exists and can be found, but Python could not import "
            "a specific name or attribute from it."
        ),
        root_cause=(
            "The name being imported does not exist in the module, "
            "the module has a circular import, or a C extension failed to load."
        ),
        steps=[
            "Verify the exported name exists: open the module or check its `__all__`.",
            "Check for circular imports between your modules.",
            "Ensure compiled extensions (`.pyd` / `.so`) are built for the current Python version.",
            "Update or reinstall the package if it may be corrupt: `pip install --force-reinstall <pkg>`.",
        ],
        example_fix=(
            "# Before (raises ImportError)\n"
            "from os.path import doesnt_exist\n\n"
            "# Fix — import what actually exists\n"
            "from os.path import join, exists"
        ),
    ),

    "NameError": ErrorAdvice(
        explanation=(
            "Python encountered a name (variable, function, or class) that has not been "
            "defined in the current scope at the point where it is used."
        ),
        root_cause=(
            "The variable was never assigned, is defined after it is used, "
            "or is misspelled."
        ),
        steps=[
            "Check the spelling of the variable name — Python is case-sensitive.",
            "Make sure the variable is assigned before the line that uses it.",
            "If the name comes from an import, add the missing `import` statement.",
            "Check that the variable is not defined inside an `if` block that may not have run.",
        ],
        example_fix=(
            "# Before (raises NameError)\n"
            "print(total)\n\n"
            "# Fix — define before use\n"
            "total = 0\n"
            "print(total)"
        ),
    ),

    "UnboundLocalError": ErrorAdvice(
        explanation=(
            "A local variable is referenced inside a function before it has been assigned "
            "a value. Python decides a variable is local if it is assigned anywhere in the "
            "function, even after the reference."
        ),
        root_cause=(
            "A variable with the same name exists in an outer scope, but an assignment "
            "inside the function makes Python treat it as local — creating a reference "
            "before the assignment."
        ),
        steps=[
            "Move the assignment above the first use of the variable.",
            "If you intend to use an outer-scope variable, declare it with `global` or `nonlocal`.",
            "Consider passing the value as a function argument instead of relying on closures.",
        ],
        example_fix=(
            "# Before (raises UnboundLocalError)\n"
            "x = 10\n"
            "def update():\n"
            "    print(x)   # UnboundLocalError — x is assigned below\n"
            "    x = 20\n\n"
            "# Fix — use global or reorder\n"
            "def update():\n"
            "    global x\n"
            "    print(x)\n"
            "    x = 20"
        ),
    ),

    "TypeError": ErrorAdvice(
        explanation=(
            "An operation or function was applied to an object of an inappropriate type. "
            "For example, trying to add a string and an integer, or calling a non-callable."
        ),
        root_cause=(
            "A variable holds a different type than expected — often `None` is returned "
            "from a function when a value was expected, or user input was not converted."
        ),
        steps=[
            "Print or log `type(variable)` to inspect the actual type at runtime.",
            "Convert the value to the expected type explicitly (e.g. `int(x)`, `str(y)`).",
            "Check that functions return a value and do not accidentally return `None`.",
            "Review function signatures to ensure callers pass the correct number of arguments.",
        ],
        example_fix=(
            "# Before (raises TypeError)\n"
            "age = input('Enter age: ')   # input() returns str\n"
            "print(age + 1)\n\n"
            "# Fix — convert to int\n"
            "age = int(input('Enter age: '))\n"
            "print(age + 1)"
        ),
    ),

    "ValueError": ErrorAdvice(
        explanation=(
            "A function received an argument of the correct type but with an "
            "unacceptable value — for example, converting a non-numeric string to int, "
            "or unpacking the wrong number of items."
        ),
        root_cause=(
            "Unexpected or malformed input data that does not satisfy the function's "
            "value constraints."
        ),
        steps=[
            "Validate input before passing it to functions (e.g. check `s.isdigit()` before `int(s)`).",
            "Use `try / except ValueError` to handle bad input gracefully.",
            "When unpacking, confirm the iterable has exactly the expected number of items.",
            "Log the actual value that caused the error to understand the data problem.",
        ],
        example_fix=(
            "# Before (raises ValueError)\n"
            "number = int('abc')\n\n"
            "# Fix — validate first\n"
            "raw = 'abc'\n"
            "if raw.lstrip('-').isdigit():\n"
            "    number = int(raw)\n"
            "else:\n"
            "    number = 0   # or raise a descriptive error"
        ),
    ),

    "IndexError": ErrorAdvice(
        explanation=(
            "A sequence (list, tuple, string) was accessed with an index that is outside "
            "its valid range. Valid indices are `0` to `len(seq) - 1`, or `-len(seq)` to `-1`."
        ),
        root_cause=(
            "The list is shorter than expected, an off-by-one error in a loop, "
            "or the list is empty."
        ),
        steps=[
            "Check the list length before indexing: `if index < len(my_list):`.",
            "Use `enumerate()` in loops to avoid manual index arithmetic.",
            "Guard against empty lists: `if my_list:` before accessing elements.",
            "Consider using `.get()` on dicts (not applicable to lists) or slicing with defaults.",
        ],
        example_fix=(
            "# Before (raises IndexError)\n"
            "items = [1, 2, 3]\n"
            "print(items[5])\n\n"
            "# Fix — guard with length check\n"
            "idx = 5\n"
            "if idx < len(items):\n"
            "    print(items[idx])\n"
            "else:\n"
            "    print('Index out of range')"
        ),
    ),

    "KeyError": ErrorAdvice(
        explanation=(
            "A dictionary lookup used a key that does not exist in the dictionary."
        ),
        root_cause=(
            "The key was never added to the dict, the data source returned unexpected "
            "keys, or there is a typo in the key name."
        ),
        steps=[
            "Use `dict.get(key, default)` to return a default instead of raising.",
            "Check membership before access: `if key in my_dict:`.",
            "Print `my_dict.keys()` to inspect available keys at runtime.",
            "When parsing external data (JSON, API), validate expected keys exist first.",
        ],
        example_fix=(
            "# Before (raises KeyError)\n"
            "data = {'name': 'Alice'}\n"
            "print(data['age'])\n\n"
            "# Fix — use .get() with a default\n"
            "print(data.get('age', 'unknown'))"
        ),
    ),

    "AttributeError": ErrorAdvice(
        explanation=(
            "An attribute or method was accessed on an object that does not have it. "
            "A very common variant is accessing an attribute on `None`."
        ),
        root_cause=(
            "The object is `None` (a function returned nothing), the wrong type was passed, "
            "or there is a typo in the attribute name."
        ),
        steps=[
            "Add a `None` guard: `if obj is not None:` before accessing attributes.",
            "Use `hasattr(obj, 'attr_name')` to check existence at runtime.",
            "Check that the function or method actually returns the expected object.",
            "Verify spelling — attribute names are case-sensitive.",
        ],
        example_fix=(
            "# Before (raises AttributeError)\n"
            "result = some_function()   # returns None on failure\n"
            "print(result.name)\n\n"
            "# Fix — guard against None\n"
            "result = some_function()\n"
            "if result is not None:\n"
            "    print(result.name)\n"
            "else:\n"
            "    print('No result returned')"
        ),
    ),

    "SyntaxError": ErrorAdvice(
        explanation=(
            "Python's parser could not understand the source code. "
            "The file will not run at all until the syntax is fixed."
        ),
        root_cause=(
            "Missing colon after `if`/`for`/`def`, unmatched brackets or quotes, "
            "incorrect indentation, or use of a Python 2 construct in Python 3."
        ),
        steps=[
            "Look at the line number reported in the traceback — the actual mistake is "
            "often one line earlier.",
            "Check for mismatched parentheses, brackets, or quotes.",
            "Ensure every `if`, `for`, `while`, `def`, `class` ends with a colon `:`.",
            "Run `python -m py_compile your_file.py` to catch syntax errors without executing.",
        ],
        example_fix=(
            "# Before (SyntaxError — missing colon)\n"
            "if x > 0\n"
            "    print(x)\n\n"
            "# Fix\n"
            "if x > 0:\n"
            "    print(x)"
        ),
    ),

    "IndentationError": ErrorAdvice(
        explanation=(
            "Python requires consistent indentation to define code blocks. "
            "Mixing tabs and spaces, or inconsistent indent levels, causes this error."
        ),
        root_cause=(
            "Mixed tabs and spaces, copy-pasted code with different indentation, "
            "or a block that is accidentally un-indented."
        ),
        steps=[
            "Configure your editor to use spaces only (4 spaces per level is standard).",
            "Run `python -tt your_file.py` to flag tab/space mixing.",
            "Re-indent the offending block — don't just add spaces by eye.",
            "Use an auto-formatter like `ruff format` or `black` to fix indentation project-wide.",
        ],
        example_fix=(
            "# Before (IndentationError — mixed tabs/spaces)\n"
            "def greet():\n"
            "    print('Hello')  # spaces\n"
            "\tprint('World')   # tab\n\n"
            "# Fix — use spaces consistently\n"
            "def greet():\n"
            "    print('Hello')\n"
            "    print('World')"
        ),
    ),

    "FileNotFoundError": ErrorAdvice(
        explanation=(
            "Python tried to open or access a file or directory that does not exist "
            "at the given path."
        ),
        root_cause=(
            "The path is wrong (relative vs absolute), the file was deleted, "
            "or the working directory is not what you expect."
        ),
        steps=[
            "Print `os.getcwd()` to confirm the working directory.",
            "Use `os.path.exists(path)` to check before opening.",
            "Prefer `pathlib.Path` for cross-platform path handling.",
            "Use absolute paths or `__file__` relative paths in scripts.",
        ],
        example_fix=(
            "# Before (raises FileNotFoundError)\n"
            "with open('data.csv') as f:\n"
            "    content = f.read()\n\n"
            "# Fix — check existence first\n"
            "from pathlib import Path\n"
            "p = Path('data.csv')\n"
            "if p.exists():\n"
            "    content = p.read_text()\n"
            "else:\n"
            "    raise FileNotFoundError(f'File not found: {p.resolve()}')"
        ),
    ),

    "ZeroDivisionError": ErrorAdvice(
        explanation=(
            "The code attempted to divide a number by zero, which is mathematically undefined."
        ),
        root_cause=(
            "A divisor variable is zero due to empty data, a calculation bug, "
            "or unvalidated user input."
        ),
        steps=[
            "Add a guard: `if denominator != 0:` before dividing.",
            "Return a sensible default (e.g. `0` or `float('inf')`) when the denominator is zero.",
            "Trace back why the denominator is zero — the real bug is usually upstream.",
        ],
        example_fix=(
            "# Before (raises ZeroDivisionError)\n"
            "result = total / count\n\n"
            "# Fix — guard against zero\n"
            "result = total / count if count != 0 else 0"
        ),
    ),

    "RecursionError": ErrorAdvice(
        explanation=(
            "The call stack exceeded Python's recursion limit (default 1000). "
            "A function called itself too many times without reaching a base case."
        ),
        root_cause=(
            "Missing or unreachable base case in a recursive function, "
            "or accidentally infinite mutual recursion."
        ),
        steps=[
            "Verify the base case is correct and reachable for all inputs.",
            "Add a print/log to trace the recursion depth during debugging.",
            "Consider rewriting deep recursion as an iterative loop.",
            "As a last resort, increase the limit: `sys.setrecursionlimit(2000)` — but fix the root cause first.",
        ],
        example_fix=(
            "# Before (infinite recursion — missing base case)\n"
            "def factorial(n):\n"
            "    return n * factorial(n - 1)\n\n"
            "# Fix — add base case\n"
            "def factorial(n):\n"
            "    if n <= 1:\n"
            "        return 1\n"
            "    return n * factorial(n - 1)"
        ),
    ),

    "PermissionError": ErrorAdvice(
        explanation=(
            "The operating system denied access to a file or resource "
            "because the process lacks the required permissions."
        ),
        root_cause=(
            "The file is owned by another user, is read-only, or the process "
            "is not running with sufficient privileges."
        ),
        steps=[
            "Check file permissions: `ls -l file` (Linux/Mac) or Properties → Security (Windows).",
            "Run the script with elevated privileges only if absolutely necessary.",
            "Ensure no other process has the file locked.",
            "Write to a directory you own (e.g. the user's home directory) instead.",
        ],
        example_fix=(
            "# Before (raises PermissionError)\n"
            "with open('/etc/hosts', 'w') as f:\n"
            "    f.write('...')\n\n"
            "# Fix — write to a user-writable path\n"
            "from pathlib import Path\n"
            "dest = Path.home() / 'output.txt'\n"
            "dest.write_text('...')"
        ),
    ),

    "RuntimeError": ErrorAdvice(
        explanation=(
            "A generic error that does not fit any more-specific category. "
            "Typically raised explicitly by library code to signal an invalid state."
        ),
        root_cause=(
            "Library or framework code detected an inconsistent or unexpected program state. "
            "The full traceback message is the key clue."
        ),
        steps=[
            "Read the full error message carefully — it often explains the specific issue.",
            "Search the traceback for the first frame inside your own code.",
            "Check the library's documentation or GitHub issues for known causes.",
            "Ensure you are not calling async code from a synchronous context (common in web frameworks).",
        ],
        example_fix=(
            "# RuntimeError messages vary widely — read the traceback message.\n"
            "# Common pattern: async called from sync\n\n"
            "# Before\n"
            "import asyncio\n"
            "async def fetch(): ...\n"
            "fetch()  # RuntimeError: coroutine was never awaited\n\n"
            "# Fix\n"
            "asyncio.run(fetch())"
        ),
    ),

    "NotImplementedError": ErrorAdvice(
        explanation=(
            "A method or function stub was called but has not been implemented yet. "
            "It is intentionally raised to signal that a subclass must override it."
        ),
        root_cause=(
            "An abstract base class method was called on the base class directly, "
            "or a subclass forgot to implement a required method."
        ),
        steps=[
            "Identify the class and method in the traceback.",
            "Implement the method in your subclass.",
            "If it is an ABC, ensure your class inherits from it and overrides all abstract methods.",
            "Use `abc.ABC` and `@abstractmethod` to enforce implementation at class-definition time.",
        ],
        example_fix=(
            "# Before (raises NotImplementedError)\n"
            "class Base:\n"
            "    def process(self):\n"
            "        raise NotImplementedError\n\n"
            "obj = Base()\n"
            "obj.process()\n\n"
            "# Fix — implement in subclass\n"
            "class Concrete(Base):\n"
            "    def process(self):\n"
            "        return 'done'"
        ),
    ),

    "AssertionError": ErrorAdvice(
        explanation=(
            "An `assert` statement evaluated to `False`. "
            "Assertions are used to verify assumptions during development."
        ),
        root_cause=(
            "A precondition or invariant in the code is violated — "
            "the actual value did not match the expected value."
        ),
        steps=[
            "Read the assertion message (if any) for clues about what was expected.",
            "Add a descriptive message: `assert condition, 'Expected X but got Y'`.",
            "Trace the value that failed the assertion back to where it was set.",
            "Do not use assertions for input validation in production — use `if / raise` instead.",
        ],
        example_fix=(
            "# Before (AssertionError with no message)\n"
            "assert len(results) > 0\n\n"
            "# Fix — add a descriptive message\n"
            "assert len(results) > 0, f'Expected results but got empty list. Query: {query}'"
        ),
    ),

    "ConnectionError": ErrorAdvice(
        explanation=(
            "A network connection could not be established to a remote host."
        ),
        root_cause=(
            "The remote server is down, the URL/host is wrong, "
            "there is no internet connection, or a firewall is blocking the request."
        ),
        steps=[
            "Verify the URL and port are correct.",
            "Test connectivity: `ping <host>` or `curl <url>` from the terminal.",
            "Wrap the call in a `try / except` and implement retry logic with back-off.",
            "Check firewall or proxy settings if running in a corporate environment.",
        ],
        example_fix=(
            "# Before (may raise ConnectionError)\n"
            "import requests\n"
            "r = requests.get('https://api.example.com/data')\n\n"
            "# Fix — handle network errors gracefully\n"
            "import requests\n"
            "try:\n"
            "    r = requests.get('https://api.example.com/data', timeout=10)\n"
            "    r.raise_for_status()\n"
            "except requests.exceptions.ConnectionError as e:\n"
            "    print(f'Connection failed: {e}')"
        ),
    ),

    "TimeoutError": ErrorAdvice(
        explanation=(
            "An operation took longer than the allotted time and was cancelled."
        ),
        root_cause=(
            "Slow network, overloaded server, or no timeout was set and "
            "the operation waited indefinitely."
        ),
        steps=[
            "Always set explicit timeouts on network and I/O calls.",
            "Increase the timeout if the operation is legitimately slow.",
            "Add retry logic with exponential back-off.",
            "Investigate server-side performance if timeouts are frequent.",
        ],
        example_fix=(
            "# Before (no timeout — hangs indefinitely)\n"
            "import requests\n"
            "r = requests.get('https://slow-api.example.com')\n\n"
            "# Fix — set a timeout\n"
            "r = requests.get('https://slow-api.example.com', timeout=30)"
        ),
    ),

    "OSError": ErrorAdvice(
        explanation=(
            "A system-level error occurred, typically related to file I/O, "
            "process management, or operating-system resources. "
            "`FileNotFoundError` and `PermissionError` are subclasses."
        ),
        root_cause=(
            "The OS rejected the operation due to a missing file, permissions issue, "
            "full disk, or unavailable device."
        ),
        steps=[
            "Check `errno` or the error message for the specific OS code.",
            "Verify the path exists and is accessible.",
            "Ensure there is sufficient disk space.",
            "Catch the specific subclass (`FileNotFoundError`, `PermissionError`) when possible.",
        ],
        example_fix=(
            "# Generic OSError handling\n"
            "try:\n"
            "    with open('file.txt') as f:\n"
            "        data = f.read()\n"
            "except FileNotFoundError:\n"
            "    print('File not found')\n"
            "except PermissionError:\n"
            "    print('Access denied')\n"
            "except OSError as e:\n"
            "    print(f'OS error: {e}')"
        ),
    ),

    "MemoryError": ErrorAdvice(
        explanation=(
            "The Python process ran out of available RAM and could not allocate more."
        ),
        root_cause=(
            "Loading an excessively large dataset into memory at once, "
            "a memory leak, or insufficient RAM for the workload."
        ),
        steps=[
            "Process large files in chunks / streams instead of loading them whole.",
            "Use generators instead of materialising large lists.",
            "Profile memory usage with `tracemalloc` or `memory_profiler`.",
            "Consider using `numpy` or `pandas` with chunking for large datasets.",
        ],
        example_fix=(
            "# Before (loads entire file into RAM)\n"
            "with open('huge.csv') as f:\n"
            "    lines = f.readlines()\n\n"
            "# Fix — iterate line by line\n"
            "with open('huge.csv') as f:\n"
            "    for line in f:\n"
            "        process(line)"
        ),
    ),

    "StopIteration": ErrorAdvice(
        explanation=(
            "An iterator has been exhausted and `next()` was called on it "
            "outside of a loop or generator context."
        ),
        root_cause=(
            "Manually calling `next()` without a default, or a generator "
            "function returning early, causing a `StopIteration` that "
            "propagates unexpectedly."
        ),
        steps=[
            "Use `next(iterator, default)` to supply a fallback instead of raising.",
            "Use a `for` loop instead of manual `next()` calls.",
            "In generators, ensure `return` (not `raise StopIteration`) is used to exit.",
        ],
        example_fix=(
            "# Before (raises StopIteration)\n"
            "it = iter([1, 2, 3])\n"
            "while True:\n"
            "    val = next(it)   # raises when exhausted\n\n"
            "# Fix — use default sentinel\n"
            "it = iter([1, 2, 3])\n"
            "_DONE = object()\n"
            "while (val := next(it, _DONE)) is not _DONE:\n"
            "    print(val)"
        ),
    ),

    "OverflowError": ErrorAdvice(
        explanation=(
            "A numeric calculation produced a result too large to be represented "
            "by the float type (Python ints are arbitrary precision and rarely overflow)."
        ),
        root_cause=(
            "Very large exponentiation or math operations on `float` values, "
            "often in scientific or financial calculations."
        ),
        steps=[
            "Use Python's arbitrary-precision `int` arithmetic instead of `float` where possible.",
            "Use the `decimal` module for high-precision decimal arithmetic.",
            "Check for runaway loops or recursive calculations producing huge numbers.",
        ],
        example_fix=(
            "# Before (OverflowError with float)\n"
            "import math\n"
            "print(math.exp(1000))  # float overflow\n\n"
            "# Fix — use Decimal for large values\n"
            "from decimal import Decimal\n"
            "import decimal\n"
            "decimal.getcontext().prec = 50\n"
            "print(Decimal(1000).exp())"
        ),
    ),

    "IOError": ErrorAdvice(
        explanation=(
            "An alias for `OSError` in Python 3. Indicates a file I/O or OS-level failure."
        ),
        root_cause="See OSError — the cause is the same.",
        steps=[
            "Treat identically to `OSError`.",
            "Catch `OSError` (which covers `IOError`) in new code.",
        ],
        example_fix=(
            "# IOError is an alias for OSError in Python 3\n"
            "try:\n"
            "    with open('missing.txt') as f:\n"
            "        data = f.read()\n"
            "except OSError as e:\n"
            "    print(f'I/O error: {e}')"
        ),
    ),

    # Fallback for any error not in the catalogue above
    "Exception": ErrorAdvice(
        explanation=(
            "A generic Python exception was raised. "
            "This is the base class for most built-in exceptions."
        ),
        root_cause=(
            "See the full error message and traceback for the specific cause."
        ),
        steps=[
            "Read the complete traceback to find the line that raised the error.",
            "Search for the specific exception class name for targeted advice.",
            "Add logging to capture the error context in production.",
        ],
        example_fix=(
            "# Always catch specific exceptions when possible\n"
            "try:\n"
            "    risky_operation()\n"
            "except ValueError as e:\n"
            "    handle_value_error(e)\n"
            "except TypeError as e:\n"
            "    handle_type_error(e)\n"
            "except Exception as e:\n"
            "    log_unexpected_error(e)\n"
            "    raise"
        ),
    ),
}


def get_advice(error_name: str) -> ErrorAdvice | None:
    """
    Return advice for *error_name*, or None if not in the catalogue.

    This is the single function AI integration will override in a later milestone:
    replace the dict lookup with an LLM call while keeping the same return type.
    """
    return ADVICE.get(error_name)


### 🤖 Assistant

> 🔧 called: update_todo_list

Now extend `DetectedError` with the new fields and wire in advice lookup during detection:

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
[x] Implement analyzer/detector.py — error type definitions & matching logic
[x] Implement analyzer/parser.py — rule-based error detection
[x] Update app.py — add text area, Analyze button, results display
[x] Create analyzer/advice.py — per-error explanation, root cause, steps, example fix
[-] Extend DetectedError dataclass with new advice fields
[ ] Update app.py card rendering — rich cards with all 4 new fields


### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — """
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


### 🤖 Assistant

> 🔧 called: apply_diff

Now replace only the card-rendering block in `app.py`:

> 🔧 **apply_diff** — app.py

### 🤖 Assistant

> 🔧 called: execute_command

Now verify the full pipeline end-to-end:

> 🔧 **execute_command** — python -c "
from analyzer.parser import analyze_log

sample = '''
Traceback (most recent call last):
  File 'app.py', line 3, in <module>
    import pandas
ModuleNotFoundError: No module named 'pandas'
'''

results = analyze_log(sample)
err = results[0]
adv = err.advice

assert err.name == 'ModuleNotFoundError'
assert adv is not None
assert adv.explanation
assert adv.root_cause
assert len(adv.steps) > 0
assert adv.example_fix

print('name        :', err.name)
print('lines       :', err.lines)
print('explanation :', adv.explanation[:60], '...')
print('root_cause  :', adv.root_cause[:60], '...')
print('steps       :', len(adv.steps), 'steps')
print('example_fix : present, first line:', adv.example_fix.splitlines()[0])
print()
print('All assertions passed.')
"


### 🤖 Assistant

> 🔧 called: execute_command



> 🔧 **execute_command** — python -c "
from analyzer.parser import analyze_log
from analyzer.advice import ADVICE

# Test all 8 required errors have full advice
required = ['ModuleNotFoundError','NameError','TypeError','ValueError','IndexError','KeyError','AttributeError','SyntaxError']
log = '\n'.join(f'{e}: test' for e in required)
results = analyze_log(log)

for r in results:
    adv = r.advice
    assert adv is not None, f'{r.name} missing advice'
    assert adv.explanation, f'{r.name} missing explanation'
    assert adv.root_cause, f'{r.name} missing root_cause'
    assert adv.steps, f'{r.name} missing steps'
    assert adv.example_fix, f'{r.name} missing example_fix'
    print(f'OK  {r.name} ({len(adv.steps)} steps)')

print()
print(f'Total advice entries in catalogue: {len(ADVICE)}')
print('All required errors verified.')
"


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
[x] Implement analyzer/detector.py — error type definitions & matching logic
[x] Implement analyzer/parser.py — rule-based error detection
[x] Update app.py — add text area, Analyze button, results display
[x] Create analyzer/advice.py — per-error explanation, root cause, steps, example fix
[x] Extend DetectedError dataclass with new advice fields
[x] Update app.py card rendering — rich cards with all 4 new fields


### 🤖 Assistant

Milestone 3 is done. Here's what changed and how it all fits together:

---

### New file: [`analyzer/advice.py`](analyzer/advice.py)

A self-contained advice database — 26 entries (8 required + extras), each an `ErrorAdvice` frozen dataclass with:

| Field | Content |
|---|---|
| `explanation` | Plain-English: what the error *means* |
| `root_cause` | The single most likely reason it occurred |
| `steps` | Ordered list of concrete fix steps |
| `example_fix` | Before/after Python code snippet |

The public entry point is `get_advice(error_name) -> ErrorAdvice | None`. That's the exact function to replace with an LLM call in a future milestone — same signature, same return type, nothing else changes.

---

### Changed: [`analyzer/detector.py`](analyzer/detector.py)

`DetectedError` gains one new field:
```python
advice: ErrorAdvice | None = field(default=None)
```
Populated automatically from `get_advice()` during detection. Existing callers that don't use `.advice` are unaffected.

---

### Changed: [`app.py`](app.py) — card rendering only

Each detected error now renders a two-part card:

```
┌─────────────────────────────────────────────────┐
│ 📦 ModuleNotFoundError   Found at: line 4        │  ← orange-left-border header
└─────────────────────────────────────────────────┘
  ▼ View details (expanded by default)
    What does this mean?       ← explanation
    Most likely root cause     ← yellow highlighted box
    Step-by-step fix           ← numbered list
    Example fix                ← st.code block (syntax-highlighted)
```

The "View raw log" expander and all upstream UI (header, how-it-works, upload, text area, Analyze button) are **unchanged**.

---

### 👤 User

Continue the FixFlow project.
Milestone 4: Repository Context Mode.
Requirements:
Allow users to upload a project folder or select a local project directory.
Scan Python files in the repository.
Match traceback filenames with project files.
Display:
Likely affected file.
Suspected function.
Line number (if available).
Why this file is likely responsible.
Show the result in a professional Streamlit card.
Keep the implementation modular inside the analyzer folder.

---

### 🤖 Assistant

> 🔧 called: read_file, read_file



> 🔧 **read_file** — app.py

> 🔧 **read_file** — analyzer/__init__.py

### 🤖 Assistant

> 🔧 called: update_todo_list

Good. I have the full picture. Let me plan precisely before writing a single line:

**Architecture decisions:**
- Streamlit has no folder-picker widget — the practical approach for a hackathon is `st.file_uploader(accept_multiple_files=True)` with `type=["py"]`, letting users multi-select all their `.py` files. This works in-browser with zero OS permissions. Add an optional text input for a local directory path as a secondary option (path-based scan using `pathlib`).
- New module: `analyzer/repo_context.py` — parses the traceback for frame references, indexes the uploaded files, and produces `ContextMatch` results.
- `app.py` gets a new collapsible "Repository Context" section between the existing upload and the Analyze button.

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
[x] Implement analyzer/detector.py — error type definitions & matching logic
[x] Implement analyzer/parser.py — rule-based error detection
[x] Update app.py — add text area, Analyze button, results display
[x] Create analyzer/advice.py — per-error explanation, root cause, steps, example fix
[x] Extend DetectedError dataclass with new advice fields
[x] Update app.py card rendering — rich cards with all 4 new fields
[-] Create analyzer/repo_context.py — traceback parser + file index + match logic
[ ] Update app.py — repo context UI section + context result cards


### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — """
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

    *files* is a mapping of {full_path_or_name: source_text}.
    When the same basename appears multiple times, the last entry wins
    (callers should deduplicate if needed).
    """
    index: dict[str, ProjectFile] = {}
    for path, source in files.items():
        fname = _basename(path) if "/" in path or "\\" in path else path
        index[fname] = ProjectFile(filename=fname, full_path=path, source=source)
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

        proj_file = (
            file_index.get(frame.filename)
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
    """Match by stem (filename without extension) when exact match fails."""
    target_stem = PurePosixPath(target_filename).stem.lower()
    for fname, proj_file in file_index.items():
        if PurePosixPath(fname).stem.lower() == target_stem:
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


### 🤖 Assistant

> 🔧 called: apply_diff

Now wire the new module into `app.py`. I need to add: (1) the import, (2) a "Repository Context" section with file uploader + local path input, (3) context result cards rendered after the existing error cards — all without touching any existing UI:

> 🔧 **apply_diff** — app.py

### 🤖 Assistant

> 🔧 called: execute_command

Now run a thorough end-to-end test simulating real traceback + project files:

> 🔧 **execute_command** — python -c "
from analyzer.repo_context import analyze_repo_context

# Simulate a real traceback referencing two project files
traceback = '''
Traceback (most recent call last):
  File \"main.py\", line 12, in <module>
    result = processor.run(data)
  File \"processor.py\", line 34, in run
    return self._transform(data)
  File \"processor.py\", line 58, in _transform
    return utils.clean(value)
AttributeError: 'NoneType' object has no attribute 'clean'
'''

processor_source = '''
class Processor:
    def run(self, data):
        return self._transform(data)

    def _transform(self, data):
        import utils
        return utils.clean(data)
'''

main_source = '''
from processor import Processor
import utils

def main():
    data = load_data()
    processor = Processor()
    result = processor.run(data)
    print(result)

def load_data():
    return None

if __name__ == '__main__':
    main()
'''

project_files = {
    'main.py': main_source,
    'processor.py': processor_source,
}

matches = analyze_repo_context(traceback, project_files)
print(f'Matches found: {len(matches)}')
for m in matches:
    print(f'  file={m.filename!r}  line={m.lineno}  fn={m.function!r}  conf={m.confidence}')
    print(f'  reason: {m.reason[:80]}...')
    if m.snippet:
        print(f'  snippet lines: {len(m.snippet.splitlines())}')
    print()

assert len(matches) >= 1
assert matches[0].filename == 'processor.py'  # innermost frame
assert matches[0].lineno == 58
assert matches[0].function == '_transform'
assert matches[0].confidence == 'High'
print('All assertions passed.')
"


### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — from analyzer.repo_context import analyze_repo_context

traceback = (
    "Traceback (most recent call last):\n"
    '  File "main.py", line 12, in <module>\n'
    "    result = processor.run(data)\n"
    '  File "processor.py", line 34, in run\n'
    "    return self._transform(data)\n"
    '  File "processor.py", line 58, in _transform\n'
    "    return utils.clean(value)\n"
    "AttributeError: 'NoneType' object has no attribute 'clean'\n"
)

processor_source = (
    "class Processor:\n"
    "    def run(self, data):\n"
    "        return self._transform(data)\n"
    "\n"
    "    def _transform(self, data):\n"
    "        import utils\n"
    "        return utils.clean(data)\n"
)

main_source = (
    "from processor import Processor\n"
    "import utils\n"
    "\n"
    "def main():\n"
    "    data = load_data()\n"
    "    processor = Processor()\n"
    "    result = processor.run(data)\n"
    "    print(result)\n"
    "\n"
    "def load_data():\n"
    "    return None\n"
    "\n"
    "if __name__ == '__main__':\n"
    "    main()\n"
)

project_files = {
    "main.py": main_source,
    "processor.py": processor_source,
}

matches = analyze_repo_context(traceback, project_files)
print(f"Matches found: {len(matches)}")
for m in matches:
    print(f"  file={m.filename!r}  line={m.lineno}  fn={m.function!r}  conf={m.confidence}")
    print(f"  reason: {m.reason[:90]}")
    if m.snippet:
        print(f"  snippet lines: {len(m.snippet.splitlines())}")
    print()

assert len(matches) >= 1, f"Expected matches, got {len(matches)}"
assert matches[0].filename == "processor.py", f"Expected processor.py, got {matches[0].filename}"
assert matches[0].lineno == 58, f"Expected line 58, got {matches[0].lineno}"
assert matches[0].function == "_transform", f"Expected _transform, got {matches[0].function}"
assert matches[0].confidence == "High"

# Test: no matches when no project files provided
empty = analyze_repo_context(traceback, {})
assert empty == []

# Test: stdlib frames ignored
stdlib_tb = (
    "Traceback (most recent call last):\n"
    '  File "lib/python3.11/site-packages/requests/api.py", line 59, in get\n'
    "    return request('get', url, params=params, **kwargs)\n"
    "ConnectionError: Failed to connect\n"
)
stdlib_matches = analyze_repo_context(stdlib_tb, {"api.py": "def get(): pass\n"})
assert stdlib_matches == [], f"Expected no match for stdlib path, got {stdlib_matches}"

print("All assertions passed.")


### 🤖 Assistant

> 🔧 called: execute_command



> 🔧 **execute_command** — python _test_repo_context.py

### 🤖 Assistant

> 🔧 called: execute_command

All assertions pass. Clean up the temp test file:

> 🔧 **execute_command** — Remove-Item _test_repo_context.py

### 🤖 Assistant

> 🔧 called: execute_command

Also verify the full import chain from `app.py` is intact:

> 🔧 **execute_command** — python -c "import ast, pathlib; src = pathlib.Path('app.py').read_text(); ast.parse(src); print('app.py parses cleanly')"

### 🤖 Assistant

> 🔧 called: execute_command



> 🔧 **execute_command** — python -c "import ast, pathlib; src = pathlib.Path('app.py').read_text(encoding='utf-8'); ast.parse(src); print('app.py parses cleanly')"

### 🤖 Assistant

> 🔧 called: execute_command



> 🔧 **execute_command** — python -c "import ast, pathlib; [ast.parse(pathlib.Path(f).read_text(encoding='utf-8')) or print(f'OK {f}') for f in ['analyzer/repo_context.py','analyzer/detector.py','analyzer/parser.py','analyzer/advice.py']]"

### 🤖 Assistant

> 🔧 called: execute_command



> 🔧 **execute_command** — python -c "
import ast, pathlib
for f in ['analyzer/repo_context.py','analyzer/detector.py','analyzer/parser.py','analyzer/advice.py']:
    ast.parse(pathlib.Path(f).read_text(encoding='utf-8'))
    print('OK', f)
"

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
[x] Implement analyzer/detector.py — error type definitions & matching logic
[x] Implement analyzer/parser.py — rule-based error detection
[x] Update app.py — add text area, Analyze button, results display
[x] Create analyzer/advice.py — per-error explanation, root cause, steps, example fix
[x] Extend DetectedError dataclass with new advice fields
[x] Update app.py card rendering — rich cards with all 4 new fields
[x] Create analyzer/repo_context.py — traceback parser + file index + match logic
[x] Update app.py — repo context UI section + context result cards


### 🤖 Assistant

Milestone 4 is done. Here's exactly what was built:

---

### New file: [`analyzer/repo_context.py`](analyzer/repo_context.py)

A fully self-contained, no-Streamlit module with a clean public interface:

```
analyze_repo_context(log_text, project_files) → list[ContextMatch]
```

**Internal pipeline:**

| Step | What it does |
|---|---|
| `parse_traceback_frames()` | Regex-extracts every `File "…", line N, in fn` frame |
| `build_file_index()` | Indexes uploaded files by basename for O(1) lookup |
| `match_context()` | Matches frames → project files; skips stdlib/site-packages paths |
| `_function_at_line()` | AST-walks source to find the function containing a given line |
| `_extract_snippet()` | Returns ±3 lines of context around the crash line with `→` marker |

Each `ContextMatch` carries: `filename`, `full_path`, `lineno`, `function`, `reason`, `confidence` (High/Medium/Low), and an optional `snippet`.

---

### Changes to [`app.py`](app.py)

Two new UI blocks added **above** the Analyze button (existing sections untouched):

1. **Repository Context section** — multi-file `.py` uploader (Ctrl/Cmd multi-select) + local directory path text input
2. **Context result cards** — rendered after the existing error cards, only when project files are provided:

```
┌─────────────────────────────── processor.py ──── HIGH CONFIDENCE ┐
│ Location: Line 58  |  Function: `_transform`                      │
└───────────────────────────────────────────────────────────────────┘
  ▼ Why this file? (expanded)
    processor.py appears directly in the traceback …
    Relevant code
     → 58 │ return utils.clean(value)
```

Confidence badge colour: **green** = High, **amber** = Medium, **grey** = Low. The "Why this file?" explanation text is the hook for AI-generated reasoning in a future milestone — same field, just replace with an LLM call.