"""
FixFlow – AI Bug-to-Fix Assistant
Streamlit home page (Milestone 4 – repository context mode).
"""

import os
from pathlib import Path

import streamlit as st

from analyzer.parser import analyze_log, parse_uploaded_file
from analyzer.repo_context import analyze_repo_context

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
    "Upload a `.txt` file **or** paste your error log below, then click **Analyze**."
)

uploaded_file = st.file_uploader(
    label="Drop your error log here (.txt)",
    type=["txt"],
    accept_multiple_files=False,
    help="Select a plain-text Python error log from your machine.",
)

# ── Paste / text area ─────────────────────────────────────────────────────────
pasted_log = st.text_area(
    label="Or paste your error log here",
    placeholder="Traceback (most recent call last):\n  File \"main.py\", line 5, in <module>\nModuleNotFoundError: No module named 'pandas'",
    height=180,
)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Repository Context (optional) ────────────────────────────────────────────
st.markdown("### 📁 Repository Context *(optional)*")
st.caption(
    "Upload your project's `.py` files so FixFlow can pinpoint which file and "
    "function caused the error. Skip this section to analyze the log only."
)

repo_py_files = st.file_uploader(
    label="Upload project Python files (.py)",
    type=["py"],
    accept_multiple_files=True,
    help="Select all .py files from your project. Hold Ctrl/Cmd to multi-select.",
)

local_repo_path = st.text_input(
    label="Or enter a local project directory path",
    placeholder=r"C:\my-project  or  /home/user/my-project",
    help="FixFlow will scan all .py files in this directory (and subdirectories).",
)

analyze_clicked = st.button("🔍 Analyze", type="primary", use_container_width=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Analysis ──────────────────────────────────────────────────────────────────
if analyze_clicked:
    # Determine input source — file takes priority over text area
    log_text = ""
    source_label = ""

    if uploaded_file is not None:
        log_text = parse_uploaded_file(uploaded_file.read())
        source_label = f"📄 **{uploaded_file.name}**"
    elif pasted_log.strip():
        log_text = pasted_log
        source_label = "📋 **Pasted log**"

    if not log_text.strip():
        st.warning("Please upload a file or paste an error log before analyzing.", icon="⚠️")
    else:
        st.markdown("### 🔍 Analysis Results")
        st.caption(f"Source: {source_label}")

        results = analyze_log(log_text)

        if not results:
            st.success(
                "No known Python errors detected in the provided log.",
                icon="✅",
            )
        else:
            st.error(
                f"**{len(results)} error type{'s' if len(results) > 1 else ''} detected.**",
                icon="🚨",
            )

            for err in results:
                line_refs = (
                    ", ".join(f"line {ln}" for ln in err.lines[:5])
                    + (" …" if len(err.lines) > 5 else "")
                )
                adv = err.advice

                # ── Card header ───────────────────────────────────────────
                st.markdown(
                    f"""
                    <div style="
                        background:#fff8f0;
                        border-left:4px solid #f97316;
                        border-radius:8px;
                        padding:0.9rem 1.1rem 0.5rem;
                        margin-bottom:0.25rem;
                    ">
                        <span style="font-size:1.1rem;font-weight:700;">{err.emoji} {err.name}</span>
                        &nbsp;<span style="font-size:0.78rem;color:#6b7280;">Found at: {line_refs}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                with st.expander("View details", expanded=True):
                    if adv:
                        # Explanation
                        st.markdown("**What does this mean?**")
                        st.markdown(adv.explanation)

                        # Root cause
                        st.markdown("**Most likely root cause**")
                        st.markdown(
                            f"""
                            <div style="
                                background:#fef9c3;
                                border-left:3px solid #ca8a04;
                                border-radius:4px;
                                padding:0.5rem 0.75rem;
                                margin-bottom:0.5rem;
                                color:#374151;
                            ">{adv.root_cause}</div>
                            """,
                            unsafe_allow_html=True,
                        )

                        # Fix steps
                        st.markdown("**Step-by-step fix**")
                        for i, step in enumerate(adv.steps, start=1):
                            st.markdown(f"{i}. {step}")

                        # Example fix
                        st.markdown("**Example fix**")
                        st.code(adv.example_fix, language="python")

                    else:
                        st.caption(err.description)

                st.markdown("&nbsp;", unsafe_allow_html=True)

        # Show the raw log in an expander so it doesn't clutter the page
        with st.expander("View raw log"):
            st.code(log_text, language="python")

        # ── Repository Context Results ─────────────────────────────────────
        # Collect project files from upload or local path
        project_files: dict[str, str] = {}

        if repo_py_files:
            for f in repo_py_files:
                try:
                    project_files[f.name] = parse_uploaded_file(f.read())
                except Exception:
                    project_files[f.name] = ""

        if local_repo_path.strip():
            repo_dir = Path(local_repo_path.strip())
            if repo_dir.is_dir():
                for py_path in repo_dir.rglob("*.py"):
                    try:
                        rel = str(py_path.relative_to(repo_dir))
                        project_files[rel] = py_path.read_text(encoding="utf-8", errors="replace")
                    except Exception:
                        project_files[str(py_path)] = ""
            else:
                st.warning(
                    f"Directory not found: `{local_repo_path.strip()}` — skipping context scan.",
                    icon="📁",
                )

        if project_files:
            context_matches = analyze_repo_context(log_text, project_files)

            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            st.markdown("### 📁 Repository Context")
            st.caption(
                f"Scanned **{len(project_files)} file{'s' if len(project_files) != 1 else ''}** · "
                f"**{len(context_matches)} match{'es' if len(context_matches) != 1 else ''}** found"
            )

            if not context_matches:
                st.info(
                    "No traceback frames matched the uploaded project files. "
                    "Check that the filenames in the error log match your project files.",
                    icon="🔍",
                )
            else:
                for match in context_matches:
                    _confidence_color = {
                        "High": "#16a34a",
                        "Medium": "#ca8a04",
                        "Low": "#6b7280",
                    }.get(match.confidence, "#6b7280")

                    _confidence_bg = {
                        "High": "#f0fdf4",
                        "Medium": "#fefce8",
                        "Low": "#f9fafb",
                    }.get(match.confidence, "#f9fafb")

                    lineno_str = f"Line {match.lineno}" if match.lineno else "Line unknown"
                    function_str = f"`{match.function}`" if match.function else "unknown"

                    # Card header
                    st.markdown(
                        f"""
                        <div style="
                            background:{_confidence_bg};
                            border-left:4px solid {_confidence_color};
                            border-radius:8px;
                            padding:0.9rem 1.1rem 0.6rem;
                            margin-bottom:0.25rem;
                        ">
                            <div style="display:flex;justify-content:space-between;align-items:center;">
                                <span style="font-size:1.05rem;font-weight:700;">📄 {match.filename}</span>
                                <span style="
                                    background:{_confidence_color};
                                    color:#fff;
                                    font-size:0.7rem;
                                    font-weight:700;
                                    padding:2px 9px;
                                    border-radius:999px;
                                    letter-spacing:0.05em;
                                ">{match.confidence.upper()} CONFIDENCE</span>
                            </div>
                            <div style="margin-top:0.35rem;font-size:0.88rem;color:#374151;">
                                <strong>Location:</strong> {lineno_str} &nbsp;|&nbsp;
                                <strong>Function:</strong> {function_str}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    with st.expander("Why this file?", expanded=True):
                        st.markdown(match.reason)

                        if match.snippet:
                            st.markdown("**Relevant code**")
                            st.code(match.snippet, language="python")

                    st.markdown("&nbsp;", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.caption(
    "FixFlow v0.4 · Built with ❤️ for IBM Bob 2.0 Hackathon · "
    "Powered by [IBM Bob](https://www.ibm.com)"
)
