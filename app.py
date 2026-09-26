"""
FixFlow – AI Bug-to-Fix Assistant
Streamlit home page (Milestone 7 – login gate + PDF download restore).
"""

import os
from pathlib import Path

import streamlit as st

from analyzer.parser import analyze_log, parse_uploaded_file
from analyzer.repo_context import analyze_repo_context
from auth import init_auth, is_authenticated, render_auth_page
from reports.report_generator import build_report_data, generate_pdf

# ── Page config (MUST be the first Streamlit call) ────────────────────────────
st.set_page_config(
    page_title="FixFlow – AI Bug-to-Fix Assistant",
    page_icon="🔧",
    layout="centered",
    initial_sidebar_state="auto",
)

# ── Bootstrap auth state ──────────────────────────────────────────────────────
init_auth()

# ── Theme & global styles ─────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ── Variables ────────────────────────────────────────────────────────── */
    :root {
        --bg-page:       #0f1117;
        --bg-card:       #1a1d27;
        --bg-card-hover: #1f2333;
        --bg-input:      #13151f;
        --border:        #2a2d3e;
        --border-focus:  #7c3aed;
        --text-primary:  #e2e8f0;
        --text-muted:    #94a3b8;
        --text-dim:      #64748b;
        --purple:        #7c3aed;
        --purple-light:  #a78bfa;
        --purple-glow:   rgba(124,58,237,0.15);
        --blue:          #3b82f6;
        --blue-light:    #93c5fd;
        --blue-glow:     rgba(59,130,246,0.15);
        --green:         #10b981;
        --green-glow:    rgba(16,185,129,0.12);
        --amber:         #f59e0b;
        --amber-glow:    rgba(245,158,11,0.12);
        --red:           #ef4444;
        --red-glow:      rgba(239,68,68,0.12);
        --orange:        #f97316;
        --radius-sm:     8px;
        --radius-md:     12px;
        --radius-lg:     16px;
        --shadow:        0 4px 24px rgba(0,0,0,0.4);
    }

    /* ── Page base ─────────────────────────────────────────────────────────── */
    html, body, [data-testid="stAppViewContainer"],
    [data-testid="stApp"], section.main {
        background-color: var(--bg-page) !important;
        color: var(--text-primary) !important;
    }
    [data-testid="stAppViewContainer"] > .main {
        background-color: var(--bg-page) !important;
    }
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 780px !important;
    }

    /* ── Typography ────────────────────────────────────────────────────────── */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        letter-spacing: -0.02em;
    }
    p, li, span, label, div {
        color: var(--text-primary);
    }
    .stMarkdown p { line-height: 1.7; }

    /* ── Divider ───────────────────────────────────────────────────────────── */
    .ff-divider {
        border: none;
        border-top: 1px solid var(--border);
        margin: 2rem 0;
    }

    /* ── Hackathon badge ───────────────────────────────────────────────────── */
    .ff-badge {
        display: inline-block;
        background: linear-gradient(135deg, var(--purple), var(--blue));
        color: #fff;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        padding: 3px 12px;
        border-radius: 999px;
        text-transform: uppercase;
        margin-bottom: 0.75rem;
    }

    /* ── Hero title ────────────────────────────────────────────────────────── */
    .ff-hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--purple-light), var(--blue-light));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.1;
        margin: 0.25rem 0 0.1rem;
    }
    .ff-hero-sub {
        font-size: 1.1rem;
        color: var(--text-muted);
        margin-bottom: 1.2rem;
    }
    .ff-hero-desc {
        color: var(--text-muted);
        line-height: 1.75;
        font-size: 0.97rem;
    }
    .ff-hero-desc strong { color: var(--purple-light); }
    .ff-tagline {
        display: inline-block;
        margin-top: 0.5rem;
        padding: 0.4rem 1rem;
        background: var(--purple-glow);
        border: 1px solid var(--purple);
        border-radius: var(--radius-sm);
        font-size: 0.88rem;
        color: var(--purple-light);
        font-style: italic;
    }

    /* ── How it works cards ────────────────────────────────────────────────── */
    .ff-step {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 1.25rem 1rem 1rem;
        text-align: center;
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    .ff-step:hover {
        border-color: var(--purple);
        box-shadow: 0 0 0 1px var(--purple), var(--shadow);
    }
    .ff-step-icon { font-size: 1.8rem; margin-bottom: 0.5rem; }
    .ff-step-title {
        font-weight: 700;
        font-size: 0.95rem;
        color: var(--text-primary);
        margin-bottom: 0.3rem;
    }
    .ff-step-caption { font-size: 0.82rem; color: var(--text-muted); }

    /* ── Section headings ──────────────────────────────────────────────────── */
    .ff-section-head {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        margin: 1.75rem 0 0.6rem;
    }
    .ff-section-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 2rem;
        height: 2rem;
        border-radius: var(--radius-sm);
        flex-shrink: 0;
        font-size: 1rem;
    }
    .ff-section-icon.purple { background: var(--purple-glow); }
    .ff-section-icon.blue   { background: var(--blue-glow);   }
    .ff-section-icon.green  { background: var(--green-glow);  }
    .ff-section-icon.amber  { background: var(--amber-glow);  }
    .ff-section-icon.red    { background: var(--red-glow);    }
    .ff-section-label {
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--text-primary);
    }
    .ff-section-caption {
        font-size: 0.82rem;
        color: var(--text-muted);
        margin: 0 0 0.8rem;
    }

    /* ── Input widgets ─────────────────────────────────────────────────────── */
    [data-testid="stTextArea"] textarea,
    [data-testid="stTextInput"] input {
        background: var(--bg-input) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
        font-size: 0.88rem !important;
    }
    [data-testid="stTextArea"] textarea:focus,
    [data-testid="stTextInput"] input:focus {
        border-color: var(--border-focus) !important;
        box-shadow: 0 0 0 2px var(--purple-glow) !important;
    }
    [data-testid="stTextArea"] textarea::placeholder,
    [data-testid="stTextInput"] input::placeholder {
        color: var(--text-dim) !important;
    }
    /* textarea label */
    [data-testid="stTextArea"] label,
    [data-testid="stTextInput"] label {
        color: var(--text-muted) !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }

    /* ── File uploader ─────────────────────────────────────────────────────── */
    [data-testid="stFileUploader"] {
        background: var(--bg-input) !important;
        border: 1px dashed var(--border) !important;
        border-radius: var(--radius-md) !important;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: var(--purple) !important;
    }
    [data-testid="stFileUploader"] label {
        color: var(--text-muted) !important;
        font-weight: 600 !important;
        font-size: 0.87rem !important;
    }

    /* ── Buttons ───────────────────────────────────────────────────────────── */
    [data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(135deg, var(--purple), var(--blue)) !important;
        color: #fff !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        padding: 0.55rem 1.5rem !important;
        letter-spacing: 0.02em;
        box-shadow: 0 2px 12px var(--purple-glow) !important;
        transition: opacity 0.15s, box-shadow 0.15s !important;
    }
    [data-testid="stButton"] > button[kind="primary"]:hover {
        opacity: 0.9 !important;
        box-shadow: 0 4px 20px var(--purple-glow) !important;
    }
    [data-testid="stDownloadButton"] > button {
        background: linear-gradient(135deg, #064e3b, #065f46) !important;
        color: #6ee7b7 !important;
        border: 1px solid #10b981 !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }
    [data-testid="stDownloadButton"] > button:hover {
        background: linear-gradient(135deg, #065f46, #047857) !important;
        box-shadow: 0 4px 16px var(--green-glow) !important;
    }

    /* ── Expanders ─────────────────────────────────────────────────────────── */
    [data-testid="stExpander"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-md) !important;
        margin-bottom: 0.5rem !important;
    }
    [data-testid="stExpander"] summary {
        background: transparent !important;
        color: var(--text-muted) !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        padding: 0.65rem 1rem !important;
    }
    [data-testid="stExpander"] summary:hover {
        color: var(--purple-light) !important;
    }
    [data-testid="stExpander"] > div[data-testid="stExpanderDetails"] {
        padding: 0.25rem 1rem 0.75rem !important;
    }
    /* Expander arrow */
    [data-testid="stExpander"] svg { stroke: var(--text-muted) !important; }

    /* ── st.code / code blocks ─────────────────────────────────────────────── */
    [data-testid="stCode"] pre,
    .stCode > pre {
        background: #0d1117 !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
    }

    /* ── st.error / warning / success / info ───────────────────────────────── */
    [data-testid="stAlert"] {
        border-radius: var(--radius-sm) !important;
        border: 1px solid var(--border) !important;
    }

    /* ── Error card ────────────────────────────────────────────────────────── */
    .ff-err-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-left: 4px solid var(--orange);
        border-radius: var(--radius-md);
        padding: 1rem 1.1rem 0.75rem;
        margin-bottom: 0.35rem;
    }
    .ff-err-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--text-primary);
    }
    .ff-err-loc {
        font-size: 0.78rem;
        color: var(--text-dim);
        margin-top: 0.2rem;
    }

    /* ── Advice sub-sections ───────────────────────────────────────────────── */
    .ff-advice-label {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin: 1rem 0 0.35rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    .ff-advice-label.purple { color: var(--purple-light); }
    .ff-advice-label.amber  { color: var(--amber); }
    .ff-advice-label.blue   { color: var(--blue-light); }
    .ff-root-cause-box {
        background: rgba(245,158,11,0.08);
        border-left: 3px solid var(--amber);
        border-radius: 6px;
        padding: 0.6rem 0.85rem;
        color: var(--text-primary);
        font-size: 0.9rem;
        line-height: 1.6;
    }
    .ff-step-row {
        display: flex;
        gap: 0.65rem;
        align-items: flex-start;
        margin-bottom: 0.55rem;
    }
    .ff-step-num {
        flex-shrink: 0;
        width: 1.4rem;
        height: 1.4rem;
        border-radius: 50%;
        background: var(--purple-glow);
        border: 1px solid var(--purple);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.7rem;
        font-weight: 700;
        color: var(--purple-light);
        margin-top: 0.1rem;
    }
    .ff-step-text {
        color: var(--text-primary);
        font-size: 0.9rem;
        line-height: 1.6;
    }

    /* ── Repo context card ─────────────────────────────────────────────────── */
    .ff-ctx-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 1rem 1.1rem 0.75rem;
        margin-bottom: 0.35rem;
    }
    .ff-ctx-card.high   { border-left: 4px solid var(--green); }
    .ff-ctx-card.medium { border-left: 4px solid var(--amber); }
    .ff-ctx-card.low    { border-left: 4px solid var(--text-dim); }
    .ff-ctx-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.4rem;
    }
    .ff-ctx-filename {
        font-size: 1rem;
        font-weight: 700;
        color: var(--text-primary);
    }
    .ff-conf-badge {
        font-size: 0.68rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 2px 10px;
        border-radius: 999px;
    }
    .ff-conf-badge.high   { background:rgba(16,185,129,0.15); color:var(--green); border:1px solid var(--green); }
    .ff-conf-badge.medium { background:rgba(245,158,11,0.15); color:var(--amber); border:1px solid var(--amber); }
    .ff-conf-badge.low    { background:rgba(100,116,139,0.15); color:var(--text-dim); border:1px solid var(--text-dim); }
    .ff-ctx-meta {
        margin-top: 0.4rem;
        font-size: 0.84rem;
        color: var(--text-muted);
    }
    .ff-ctx-meta strong { color: var(--text-primary); }

    /* ── Download card ─────────────────────────────────────────────────────── */
    .ff-dl-card {
        background: var(--bg-card);
        border: 1px solid var(--green);
        border-radius: var(--radius-md);
        padding: 1.25rem 1.4rem;
        margin: 1rem 0;
        box-shadow: 0 0 24px var(--green-glow);
    }
    .ff-dl-title {
        font-size: 1rem;
        font-weight: 700;
        color: var(--green);
        margin-bottom: 0.2rem;
    }
    .ff-dl-caption { font-size: 0.83rem; color: var(--text-muted); margin-bottom: 0.75rem; }

    /* ── Footer ────────────────────────────────────────────────────────────── */
    .ff-footer {
        text-align: center;
        font-size: 0.78rem;
        color: var(--text-dim);
        margin-top: 1rem;
        padding-top: 1.5rem;
        border-top: 1px solid var(--border);
    }
    .ff-footer a { color: var(--purple-light); text-decoration: none; }

    /* ── Responsive tweaks ─────────────────────────────────────────────────── */
    @media (max-width: 600px) {
        .ff-hero-title { font-size: 1.9rem; }
        .ff-step { padding: 0.9rem 0.75rem; }
        .ff-ctx-header { flex-direction: column; align-items: flex-start; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Auth gate ─────────────────────────────────────────────────────────────────
if not is_authenticated():
    render_auth_page()
    st.stop()

# ── Logout button (top-right, subtle) ─────────────────────────────────────────
with st.container():
    _, logout_col = st.columns([6, 1])
    with logout_col:
        if st.button("Logout", key="btn_logout"):
            st.session_state["ff_authenticated"] = False
            st.session_state["ff_current_user"]  = ""
            st.session_state["ff_auth_view"]      = "login"
            # Clear any stale PDF state so it doesn't bleed into the next session
            st.session_state.pop("pdf_ready", None)
            st.session_state.pop("pdf_bytes", None)
            st.rerun()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<span class="ff-badge">IBM Bob 2.0 Hackathon</span>', unsafe_allow_html=True)
st.markdown('<h1 class="ff-hero-title">🔧 FixFlow</h1>', unsafe_allow_html=True)
st.markdown('<p class="ff-hero-sub">AI Bug-to-Fix Assistant</p>', unsafe_allow_html=True)
st.markdown(
    """
    <p class="ff-hero-desc">
        Debugging is the most time-consuming part of software development.
        <strong>FixFlow</strong> cuts that time dramatically by letting you paste or upload
        an error log and receive an AI-powered root-cause analysis with concrete fix
        suggestions — all powered by <strong>IBM Bob</strong>.
    </p>
    <span class="ff-tagline">Upload an error log &rarr; get a diagnosis &rarr; apply the fix.</span>
    """,
    unsafe_allow_html=True,
)

st.markdown('<hr class="ff-divider">', unsafe_allow_html=True)

# ── How it works ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="ff-section-head">
        <div class="ff-section-icon purple">💡</div>
        <span class="ff-section-label">How it works</span>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        """
        <div class="ff-step">
            <div class="ff-step-icon">📂</div>
            <div class="ff-step-title">1. Upload</div>
            <div class="ff-step-caption">Drop in your error log, stack trace, or crash report.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div class="ff-step">
            <div class="ff-step-icon">🤖</div>
            <div class="ff-step-title">2. Analyze</div>
            <div class="ff-step-caption">IBM Bob reads the log and identifies root causes.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        """
        <div class="ff-step">
            <div class="ff-step-icon">✅</div>
            <div class="ff-step-title">3. Fix</div>
            <div class="ff-step-caption">Get actionable code-level fix suggestions instantly.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<hr class="ff-divider">', unsafe_allow_html=True)

# ── Upload Error Log ──────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="ff-section-head">
        <div class="ff-section-icon blue">📄</div>
        <span class="ff-section-label">Upload Error Log</span>
    </div>
    <p class="ff-section-caption">Upload a <code>.txt</code> file <strong>or</strong> paste your error log below, then click <strong>Analyze</strong>.</p>
    """,
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    label="Drop your error log here (.txt)",
    type=["txt"],
    accept_multiple_files=False,
    help="Select a plain-text Python error log from your machine.",
    key="error_log_uploader",
)

# ── Paste / text area ─────────────────────────────────────────────────────────
pasted_log = st.text_area(
    label="Or paste your error log here",
    placeholder="Traceback (most recent call last):\n  File \"main.py\", line 5, in <module>\nModuleNotFoundError: No module named 'pandas'",
    height=180,
)

st.markdown('<hr class="ff-divider">', unsafe_allow_html=True)

# ── Repository Context (optional) ────────────────────────────────────────────
st.markdown(
    """
    <div class="ff-section-head">
        <div class="ff-section-icon purple">🗂️</div>
        <span class="ff-section-label">Repository Context <span style="color:var(--text-dim);font-weight:400;font-size:0.85rem;">(optional)</span></span>
    </div>
    <p class="ff-section-caption">Upload your project&#39;s <code>.py</code> files so FixFlow can pinpoint which file and function caused the error. Skip this section to analyze the log only.</p>
    """,
    unsafe_allow_html=True,
)

repo_py_files = st.file_uploader(
    label="Upload project Python files (.py)",
    type=["py"],
    accept_multiple_files=True,
    help="Select all .py files from your project. Hold Ctrl/Cmd to multi-select.",
    key="repo_py_uploader",
)

local_repo_path = st.text_input(
    label="Or enter a local project directory path",
    placeholder=r"C:\my-project  or  /home/user/my-project",
    help="FixFlow will scan all .py files in this directory (and subdirectories).",
)

analyze_clicked = st.button("🔍 Analyze", type="primary", use_container_width=True)

st.markdown('<hr class="ff-divider">', unsafe_allow_html=True)

# ── Analysis ──────────────────────────────────────────────────────────────────
if analyze_clicked:
    # Initialise all values so PDF builder always has valid references
    log_text = ""
    source_label = ""
    results = []
    context_matches: list = []

    if uploaded_file is not None:
        log_text = parse_uploaded_file(uploaded_file.read())
        source_label = f"📄 **{uploaded_file.name}**"
    elif pasted_log.strip():
        log_text = pasted_log
        source_label = "📋 **Pasted log**"

    if not log_text.strip():
        st.warning("Please upload a file or paste an error log before analyzing.", icon="⚠️")
    else:
        # ── Results heading ───────────────────────────────────────────────────
        st.markdown(
            """
            <div class="ff-section-head">
                <div class="ff-section-icon red">🔍</div>
                <span class="ff-section-label">Analysis Results</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
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

                # ── Error card header ─────────────────────────────────────────
                st.markdown(
                    f"""
                    <div class="ff-err-card">
                        <div class="ff-err-title">{err.emoji} {err.name}</div>
                        <div class="ff-err-loc">📍 Found at: {line_refs}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                with st.expander("View details", expanded=True):
                    if adv:
                        # Explanation
                        st.markdown(
                            '<div class="ff-advice-label purple">💬 &nbsp;What does this mean?</div>',
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            f'<p style="color:var(--text-primary);font-size:0.92rem;line-height:1.7;margin-bottom:0.2rem">{adv.explanation}</p>',
                            unsafe_allow_html=True,
                        )

                        # Root cause
                        st.markdown(
                            '<div class="ff-advice-label amber">⚡ &nbsp;Most likely root cause</div>',
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            f'<div class="ff-root-cause-box">{adv.root_cause}</div>',
                            unsafe_allow_html=True,
                        )

                        # Fix steps
                        st.markdown(
                            '<div class="ff-advice-label blue">🛠️ &nbsp;Step-by-step fix</div>',
                            unsafe_allow_html=True,
                        )
                        steps_html = "".join(
                            f'<div class="ff-step-row">'
                            f'<div class="ff-step-num">{i}</div>'
                            f'<div class="ff-step-text">{step}</div>'
                            f'</div>'
                            for i, step in enumerate(adv.steps, start=1)
                        )
                        st.markdown(
                            f'<div style="margin-bottom:0.5rem">{steps_html}</div>',
                            unsafe_allow_html=True,
                        )

                        # Example fix
                        st.markdown(
                            '<div class="ff-advice-label purple">✨ &nbsp;Example fix</div>',
                            unsafe_allow_html=True,
                        )
                        st.code(adv.example_fix, language="python")

                    else:
                        st.caption(err.description)

                st.markdown("&nbsp;", unsafe_allow_html=True)

        # Show the raw log in an expander so it doesn't clutter the page
        with st.expander("📋 View raw log"):
            st.code(log_text, language="python")

        # ── Repository Context Results ────────────────────────────────────────
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

            st.markdown('<hr class="ff-divider">', unsafe_allow_html=True)
            st.markdown(
                """
                <div class="ff-section-head">
                    <div class="ff-section-icon purple">🗂️</div>
                    <span class="ff-section-label">Repository Context</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
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
                    conf_cls = match.confidence.lower()   # "high" | "medium" | "low"
                    lineno_str   = f"Line {match.lineno}" if match.lineno else "Line unknown"
                    function_str = f"<code>{match.function}</code>" if match.function else "unknown"

                    st.markdown(
                        f"""
                        <div class="ff-ctx-card {conf_cls}">
                            <div class="ff-ctx-header">
                                <span class="ff-ctx-filename">📄 {match.filename}</span>
                                <span class="ff-conf-badge {conf_cls}">{match.confidence.upper()} CONFIDENCE</span>
                            </div>
                            <div class="ff-ctx-meta">
                                <strong>Location:</strong> {lineno_str} &nbsp;|&nbsp;
                                <strong>Function:</strong> {function_str}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    with st.expander("🔎 Why this file?", expanded=True):
                        st.markdown(match.reason)
                        if match.snippet:
                            st.markdown(
                                '<div class="ff-advice-label blue">📝 &nbsp;Relevant code</div>',
                                unsafe_allow_html=True,
                            )
                            st.code(match.snippet, language="python")

                    st.markdown("&nbsp;", unsafe_allow_html=True)

        # ── Generate and store PDF in session state ───────────────────────────
        # results and context_matches are always [] or populated lists at this point
        report_data = build_report_data(
            log_text=log_text,
            results=results,
            context_matches=context_matches,
        )
        st.session_state["pdf_bytes"] = generate_pdf(report_data)
        st.session_state["pdf_ready"] = True

# ── Download Bug Report ───────────────────────────────────────────────────────
if st.session_state.get("pdf_ready") and st.session_state.get("pdf_bytes"):
    st.markdown('<hr class="ff-divider">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="ff-dl-card">
            <div class="ff-dl-title">📥 &nbsp;Bug Report Ready</div>
            <div class="ff-dl-caption">A professional PDF summarising the full analysis — error type, root cause, fix steps, code example, and repository context.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.download_button(
        label="⬇️  Download Bug Report (.pdf)",
        data=st.session_state["pdf_bytes"],
        file_name="fixflow_bug_report.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="ff-footer">
        FixFlow v1.0 &nbsp;·&nbsp; Built with ❤️ for
        <a href="https://www.ibm.com" target="_blank">IBM Bob 2.0 Hackathon</a>
    </div>
    """,
    unsafe_allow_html=True,
)
