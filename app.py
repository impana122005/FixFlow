"""
FixFlow – AI Bug-to-Fix Assistant
Streamlit home page (Milestone 6 – confidence score, severity badge, fix time, sample errors, smart upload guidance).
"""

import os
from pathlib import Path

import streamlit as st

from analyzer.confidence import estimate_fix_time, score_confidence
from analyzer.parser import analyze_log, parse_uploaded_file
from analyzer.repo_context import analyze_repo_context
from reports.report_generator import build_report_data, generate_pdf, get_severity

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FixFlow – AI Bug-to-Fix Assistant",
    page_icon="🔧",
    layout="centered",
    initial_sidebar_state="auto",
)

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

    /* ── Top toolbar (Deploy button + three-dot menu) ──────────────────────── */
    [data-testid="stToolbar"] {
        color: var(--text-muted) !important;
    }
    /* "Deploy" button text */
    [data-testid="stToolbar"] button[kind="header"],
    [data-testid="stToolbar"] button {
        color: var(--purple-light) !important;
        border-color: transparent !important;
        background: transparent !important;
    }
    [data-testid="stToolbar"] button:hover {
        color: #c4b5fd !important;
        background: var(--purple-glow) !important;
    }
    /* Three-dot menu icon and any toolbar SVG/spans */
    [data-testid="stToolbar"] svg {
        fill: var(--purple-light) !important;
        stroke: var(--purple-light) !important;
    }
    [data-testid="stDecoration"] { display: none !important; }

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
    p, li, span, label, div { color: var(--text-primary); }
    .stMarkdown p { line-height: 1.7; }

    /* ── Divider ───────────────────────────────────────────────────────────── */
    .ff-divider {
        border: none;
        height: 1px;
        background: linear-gradient(
            90deg,
            transparent 0%,
            var(--border) 15%,
            var(--border) 85%,
            transparent 100%
        );
        margin: 2rem 0;
    }

    /* ── Hackathon badge ───────────────────────────────────────────────────── */
    .ff-badge {
        display: inline-block;
        background: linear-gradient(135deg, var(--purple), var(--blue));
        color: #fff;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        padding: 4px 14px;
        border-radius: 999px;
        text-transform: uppercase;
        margin-bottom: 0.75rem;
        box-shadow: 0 2px 12px var(--purple-glow);
    }

    /* ── Hero glow backdrop ────────────────────────────────────────────────── */
    .ff-hero-glow {
        position: relative;
    }
    .ff-hero-glow::before {
        content: '';
        position: absolute;
        top: -60px; left: 50%;
        transform: translateX(-50%);
        width: 420px; height: 260px;
        background: radial-gradient(ellipse at center,
            rgba(124,58,237,0.13) 0%,
            rgba(59,130,246,0.06) 45%,
            transparent 70%);
        pointer-events: none;
        z-index: 0;
    }

    /* ── Hero ──────────────────────────────────────────────────────────────── */
    .ff-hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(120deg, #c4b5fd 0%, var(--purple-light) 40%, var(--blue-light) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.08;
        margin: 0.2rem 0 0.05rem;
        letter-spacing: -0.03em;
    }
    .ff-hero-sub {
        font-size: 1.1rem;
        color: var(--text-muted);
        margin-bottom: 1.1rem;
        letter-spacing: 0.01em;
    }
    .ff-hero-desc { color: var(--text-muted); line-height: 1.8; font-size: 0.97rem; }
    .ff-hero-desc strong { color: var(--purple-light); }
    .ff-tagline {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        margin-top: 0.6rem;
        padding: 0.45rem 1.1rem;
        background: var(--purple-glow);
        border: 1px solid rgba(124,58,237,0.45);
        border-left: 3px solid var(--purple);
        border-radius: var(--radius-sm);
        font-size: 0.88rem;
        color: var(--purple-light);
        font-style: italic;
    }

    /* ── How-it-works cards ────────────────────────────────────────────────── */
    .ff-step {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 1.4rem 1rem 1.1rem;
        text-align: center;
        transition: border-color 0.2s, box-shadow 0.2s, transform 0.15s;
        position: relative;
        overflow: hidden;
    }
    .ff-step::before {
        content: '';
        position: absolute;
        inset: 0 0 auto 0;
        height: 2px;
        background: linear-gradient(90deg, var(--purple), var(--blue));
        opacity: 0;
        transition: opacity 0.2s;
    }
    .ff-step:hover {
        border-color: rgba(124,58,237,0.6);
        box-shadow: 0 4px 24px rgba(0,0,0,0.35), 0 0 0 1px rgba(124,58,237,0.25);
        transform: translateY(-2px);
    }
    .ff-step:hover::before { opacity: 1; }
    .ff-step-icon  { font-size: 2rem; margin-bottom: 0.55rem; line-height: 1; }
    .ff-step-title { font-weight: 700; font-size: 0.95rem; color: var(--text-primary); margin-bottom: 0.3rem; }
    .ff-step-caption { font-size: 0.82rem; color: var(--text-muted); line-height: 1.5; }

    /* ── Section headings ──────────────────────────────────────────────────── */
    .ff-section-head {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        margin: 1.75rem 0 0.6rem;
    }
    .ff-section-icon {
        display: flex; align-items: center; justify-content: center;
        width: 2rem; height: 2rem;
        border-radius: var(--radius-sm);
        flex-shrink: 0; font-size: 1rem;
    }
    .ff-section-icon.purple { background: var(--purple-glow); border: 1px solid rgba(124,58,237,0.3); }
    .ff-section-icon.blue   { background: var(--blue-glow);   border: 1px solid rgba(59,130,246,0.3);  }
    .ff-section-icon.green  { background: var(--green-glow);  border: 1px solid rgba(16,185,129,0.3);  }
    .ff-section-icon.amber  { background: var(--amber-glow);  border: 1px solid rgba(245,158,11,0.3);  }
    .ff-section-icon.red    { background: var(--red-glow);    border: 1px solid rgba(239,68,68,0.3);   }
    .ff-section-label   { font-size: 1.05rem; font-weight: 700; color: var(--text-primary); }
    .ff-section-caption { font-size: 0.82rem; color: var(--text-muted); margin: 0 0 0.8rem; }

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
    [data-testid="stTextInput"] input::placeholder { color: var(--text-dim) !important; }
    [data-testid="stTextArea"] label,
    [data-testid="stTextInput"] label {
        color: var(--text-muted) !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }

    /* ── File uploader ─────────────────────────────────────────────────────── */
    [data-testid="stFileUploader"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    /* Drop-zone box */
    [data-testid="stFileUploaderDropzone"] {
        background: var(--bg-input) !important;
        border: 2px dashed rgba(139,92,246,0.55) !important;
        border-radius: var(--radius-md) !important;
        padding: 1.4rem 1.25rem !important;
        transition: border-color 0.2s ease, background 0.2s ease,
                    box-shadow 0.2s ease !important;
    }
    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: var(--purple-light) !important;
        background: rgba(139,92,246,0.05) !important;
        box-shadow: 0 0 0 3px rgba(139,92,246,0.12) !important;
    }
    /* Drag-over highlight */
    [data-testid="stFileUploaderDropzone"]:focus-within {
        border-color: var(--purple-light) !important;
        box-shadow: 0 0 0 3px rgba(139,92,246,0.18) !important;
    }
    /* Upload icon */
    [data-testid="stFileUploaderDropzone"] svg {
        fill: #8B5CF6 !important;
        stroke: #8B5CF6 !important;
        opacity: 0.9 !important;
    }
    /* "Drag and drop…" instruction text */
    [data-testid="stFileUploaderDropzoneInstructions"] {
        color: var(--text-muted) !important;
        font-size: 0.88rem !important;
    }
    [data-testid="stFileUploaderDropzoneInstructions"] span {
        color: var(--text-muted) !important;
    }
    /* "Limit X·MB" / file-type hint */
    [data-testid="stFileUploaderDropzoneInstructions"] small {
        color: var(--text-dim) !important;
        font-size: 0.76rem !important;
    }
    /* "Browse files" button inside uploader */
    [data-testid="stFileUploaderDropzone"] button {
        background: var(--bg-card) !important;
        color: var(--purple-light) !important;
        border: 1px solid rgba(139,92,246,0.5) !important;
        border-radius: var(--radius-sm) !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        padding: 0.3rem 0.9rem !important;
        transition: background 0.15s, border-color 0.15s !important;
    }
    [data-testid="stFileUploaderDropzone"] button:hover {
        background: rgba(139,92,246,0.12) !important;
        border-color: var(--purple-light) !important;
    }
    /* Uploaded file chip */
    [data-testid="stFileUploaderFile"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-muted) !important;
        font-size: 0.82rem !important;
        padding: 0.3rem 0.6rem !important;
        margin-top: 0.4rem !important;
    }
    /* Section label above the uploader */
    [data-testid="stFileUploader"] label {
        color: var(--text-muted) !important;
        font-weight: 600 !important;
        font-size: 0.87rem !important;
        margin-bottom: 0.35rem !important;
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
        transition: transform 0.1s, box-shadow 0.15s, opacity 0.15s !important;
    }
    [data-testid="stButton"] > button[kind="primary"]:hover {
        opacity: 0.92 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 22px rgba(124,58,237,0.35) !important;
    }
    [data-testid="stButton"] > button[kind="primary"]:active {
        transform: translateY(0px) !important;
        box-shadow: 0 2px 8px var(--purple-glow) !important;
    }
    [data-testid="stButton"] > button[kind="secondary"] {
        background: var(--bg-card) !important;
        color: var(--purple-light) !important;
        border: 1px solid rgba(124,58,237,0.45) !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
        transition: background 0.15s, border-color 0.15s !important;
    }
    [data-testid="stButton"] > button[kind="secondary"]:hover {
        background: rgba(124,58,237,0.1) !important;
        border-color: var(--purple-light) !important;
    }
    [data-testid="stDownloadButton"] > button {
        background: linear-gradient(135deg, #064e3b, #065f46) !important;
        color: #6ee7b7 !important;
        border: 1px solid rgba(16,185,129,0.6) !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        transition: transform 0.1s, box-shadow 0.15s !important;
    }
    [data-testid="stDownloadButton"] > button:hover {
        background: linear-gradient(135deg, #065f46, #047857) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(16,185,129,0.2) !important;
    }
    [data-testid="stDownloadButton"] > button:active {
        transform: translateY(0) !important;
    }

    /* ── Expanders ─────────────────────────────────────────────────────────── */
    [data-testid="stExpander"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-md) !important;
        margin-bottom: 0.5rem !important;
        transition: border-color 0.2s !important;
    }
    [data-testid="stExpander"]:has(> details[open]) {
        border-color: rgba(124,58,237,0.4) !important;
        border-left: 3px solid var(--purple) !important;
    }
    [data-testid="stExpander"] summary {
        background: transparent !important;
        color: var(--text-muted) !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        padding: 0.65rem 1rem !important;
        transition: color 0.15s !important;
    }
    [data-testid="stExpander"] summary:hover {
        color: var(--purple-light) !important;
        background: rgba(124,58,237,0.04) !important;
    }
    [data-testid="stExpander"] > div[data-testid="stExpanderDetails"] {
        padding: 0.25rem 1rem 0.75rem !important;
    }
    [data-testid="stExpander"] svg { stroke: var(--text-muted) !important; }

    /* ── Code blocks ───────────────────────────────────────────────────────── */
    [data-testid="stCode"] pre, .stCode > pre {
        background: #0d1117 !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        font-size: 0.84rem !important;
        line-height: 1.65 !important;
    }
    /* Copy button inside code block */
    [data-testid="stCode"] button,
    [data-testid="stCode"] [data-testid="stCodeCopyButton"] {
        color: var(--text-dim) !important;
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 5px !important;
        transition: color 0.15s, background 0.15s !important;
    }
    [data-testid="stCode"] button:hover,
    [data-testid="stCode"] [data-testid="stCodeCopyButton"]:hover {
        color: var(--purple-light) !important;
        background: rgba(124,58,237,0.1) !important;
        border-color: rgba(124,58,237,0.4) !important;
    }

    /* ── Alerts ────────────────────────────────────────────────────────────── */
    [data-testid="stAlert"] {
        border-radius: var(--radius-sm) !important;
    }
    /* Error alert */
    [data-testid="stAlert"][data-baseweb="notification"][kind="error"],
    div[data-testid="stAlert"].st-emotion-cache-error {
        background: rgba(239,68,68,0.08) !important;
        border: 1px solid rgba(239,68,68,0.4) !important;
        color: #fca5a5 !important;
    }
    /* Warning alert */
    [data-testid="stAlert"][kind="warning"] {
        background: rgba(245,158,11,0.08) !important;
        border: 1px solid rgba(245,158,11,0.35) !important;
        color: #fcd34d !important;
    }
    /* Success alert */
    [data-testid="stAlert"][kind="success"] {
        background: rgba(16,185,129,0.08) !important;
        border: 1px solid rgba(16,185,129,0.35) !important;
        color: #6ee7b7 !important;
    }
    /* Info alert */
    [data-testid="stAlert"][kind="info"] {
        background: rgba(59,130,246,0.08) !important;
        border: 1px solid rgba(59,130,246,0.35) !important;
        color: var(--blue-light) !important;
    }

    /* ── Caption / help text ───────────────────────────────────────────────── */
    .stCaption, [data-testid="stCaptionContainer"] p,
    [data-testid="stCaption"] {
        color: var(--text-dim) !important;
        font-size: 0.8rem !important;
    }
    /* Help (?) tooltip icon next to inputs */
    [data-testid="stTooltipIcon"] svg,
    button[data-testid="stTooltipHoverTarget"] svg {
        stroke: var(--purple-light) !important;
        opacity: 0.7 !important;
        transition: opacity 0.15s !important;
    }
    [data-testid="stTooltipIcon"]:hover svg,
    button[data-testid="stTooltipHoverTarget"]:hover svg {
        opacity: 1 !important;
    }

    /* ── Progress bar ──────────────────────────────────────────────────────── */
    [data-testid="stProgressBar"] > div > div {
        background: linear-gradient(90deg, var(--purple), var(--blue)) !important;
        border-radius: 999px !important;
        min-height: 4px !important;
    }
    [data-testid="stProgressBar"] > div {
        background: var(--bg-input) !important;
        border-radius: 999px !important;
        height: 4px !important;
    }

    /* ── Error card ────────────────────────────────────────────────────────── */
    .ff-err-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-left: 4px solid var(--orange);
        border-radius: var(--radius-md);
        padding: 1.05rem 1.15rem 0.85rem;
        margin-bottom: 0.35rem;
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    .ff-err-card:hover {
        border-color: rgba(249,115,22,0.5);
        box-shadow: 0 2px 16px rgba(0,0,0,0.25);
    }
    /* Severity-tinted left borders */
    .ff-err-card.sev-high   { border-left-color: var(--red);   }
    .ff-err-card.sev-medium { border-left-color: var(--amber); }
    .ff-err-card.sev-low    { border-left-color: var(--green); }
    .ff-err-card-top {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        flex-wrap: wrap;
        gap: 0.4rem;
    }
    .ff-err-title { font-size: 1.05rem; font-weight: 700; color: var(--text-primary); }
    .ff-err-loc   { font-size: 0.78rem; color: var(--text-dim); margin-top: 0.25rem; }

    /* ── Severity badge ────────────────────────────────────────────────────── */
    .ff-sev-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        padding: 3px 10px;
        border-radius: 999px;
        white-space: nowrap;
    }
    .ff-sev-badge.high   { background: rgba(239,68,68,0.15);  color: #f87171; border: 1px solid #ef4444; }
    .ff-sev-badge.medium { background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid #f59e0b; }
    .ff-sev-badge.low    { background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid #10b981; }

    /* ── Time-to-fix info card ─────────────────────────────────────────────── */
    .ff-time-card {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        background: var(--blue-glow);
        border: 1px solid rgba(59,130,246,0.35);
        border-radius: var(--radius-sm);
        padding: 0.3rem 0.75rem;
        font-size: 0.8rem;
        color: var(--blue-light);
        font-weight: 600;
        white-space: nowrap;
    }
    .ff-time-card .ff-time-icon { font-size: 0.9rem; }

    /* ── Confidence row ────────────────────────────────────────────────────── */
    .ff-confidence-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.5rem;
        margin: 0.55rem 0 0.3rem;
        padding: 0.35rem 0.65rem;
        background: rgba(124,58,237,0.06);
        border-radius: var(--radius-sm);
        font-size: 0.8rem;
        color: var(--text-muted);
    }
    .ff-confidence-pct {
        font-weight: 700;
        font-size: 0.85rem;
        color: var(--purple-light);
        min-width: 3rem;
        text-align: right;
    }

    /* ── Supported error types info card ───────────────────────────────────── */
    .ff-error-types-card {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-left: 3px solid rgba(124,58,237,0.4) !important;
        border-radius: var(--radius-md) !important;
        padding: 1rem 1.25rem 0.9rem !important;
        margin: 0.75rem 0 0.5rem !important;
    }
    .ff-error-types-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.5rem 0.75rem;
        margin-top: 0.65rem;
    }
    .ff-error-chip {
        display: flex;
        align-items: center;
        gap: 0.35rem;
        background: var(--bg-input);
        border: 1px solid var(--border);
        border-radius: 6px;
        padding: 0.3rem 0.55rem;
        font-size: 0.78rem;
        font-weight: 600;
        color: var(--text-muted);
        white-space: nowrap;
        transition: border-color 0.15s, color 0.15s, background 0.15s;
        cursor: default;
    }
    .ff-error-chip:hover {
        border-color: rgba(139,92,246,0.5);
        color: var(--purple-light);
        background: rgba(124,58,237,0.06);
    }
    .ff-error-chip .chip-icon { font-size: 0.85rem; }

    /* ── Advice sub-sections ───────────────────────────────────────────────── */
    .ff-advice-label {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        margin: 1.1rem 0 0.4rem;
        padding-bottom: 0.3rem;
        border-bottom: 1px solid var(--border);
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    .ff-advice-label.purple { color: var(--purple-light); }
    .ff-advice-label.amber  { color: var(--amber); }
    .ff-advice-label.blue   { color: var(--blue-light); }
    .ff-root-cause-box {
        background: rgba(245,158,11,0.07);
        border-left: 3px solid var(--amber);
        border-radius: 0 6px 6px 0;
        padding: 0.65rem 0.95rem;
        color: var(--text-primary);
        font-size: 0.9rem;
        line-height: 1.65;
    }
    .ff-step-row { display: flex; gap: 0.7rem; align-items: flex-start; margin-bottom: 0.6rem; }
    .ff-step-num {
        flex-shrink: 0;
        width: 1.5rem; height: 1.5rem;
        border-radius: 50%;
        background: var(--purple-glow);
        border: 1px solid rgba(124,58,237,0.5);
        display: flex; align-items: center; justify-content: center;
        font-size: 0.7rem; font-weight: 700;
        color: var(--purple-light);
        margin-top: 0.1rem;
    }
    .ff-step-text { color: var(--text-primary); font-size: 0.9rem; line-height: 1.65; }

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
    .ff-ctx-header { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.4rem; }
    .ff-ctx-filename { font-size: 1rem; font-weight: 700; color: var(--text-primary); }
    .ff-conf-badge {
        font-size: 0.68rem; font-weight: 800; letter-spacing: 0.08em;
        text-transform: uppercase; padding: 2px 10px; border-radius: 999px;
    }
    .ff-conf-badge.high   { background:rgba(16,185,129,0.15); color:var(--green); border:1px solid var(--green); }
    .ff-conf-badge.medium { background:rgba(245,158,11,0.15); color:var(--amber); border:1px solid var(--amber); }
    .ff-conf-badge.low    { background:rgba(100,116,139,0.15); color:var(--text-dim); border:1px solid var(--text-dim); }
    .ff-ctx-meta { margin-top: 0.4rem; font-size: 0.84rem; color: var(--text-muted); }
    .ff-ctx-meta strong { color: var(--text-primary); }

    /* ── Download card ─────────────────────────────────────────────────────── */
    .ff-dl-card {
        background: var(--bg-card);
        border: 1px solid rgba(16,185,129,0.5);
        border-top: 3px solid var(--green);
        border-radius: var(--radius-md);
        padding: 1.25rem 1.4rem;
        margin: 1rem 0;
        box-shadow: 0 4px 28px rgba(16,185,129,0.1), 0 1px 0 rgba(16,185,129,0.08) inset;
    }
    .ff-dl-title   { font-size: 1rem; font-weight: 700; color: var(--green); margin-bottom: 0.25rem; }
    .ff-dl-caption { font-size: 0.83rem; color: var(--text-muted); margin-bottom: 0.75rem; line-height: 1.6; }

    /* ── Footer ────────────────────────────────────────────────────────────── */
    .ff-footer {
        text-align: center; font-size: 0.8rem; color: var(--text-dim);
        margin-top: 1.5rem; padding-top: 1.5rem;
        border-top: 1px solid var(--border);
        line-height: 2;
    }
    .ff-footer a { color: var(--purple-light); text-decoration: none; font-weight: 500; }
    .ff-footer a:hover { color: #c4b5fd; }
    .ff-footer-brand { color: var(--purple-light); font-weight: 700; }

    /* ── Upload guidance ───────────────────────────────────────────────────── */
    .ff-upload-warn {
        background: rgba(245,158,11,0.08);
        border: 1px solid var(--amber);
        border-radius: var(--radius-sm);
        padding: 0.65rem 0.9rem;
        font-size: 0.85rem;
        color: var(--amber);
        margin-top: 0.4rem;
    }

    /* ── Scrollbar ─────────────────────────────────────────────────────────── */
    ::-webkit-scrollbar       { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-page); }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 999px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--purple); }

    /* ── Code block polish ─────────────────────────────────────────────────── */
    [data-testid="stCode"] pre, .stCode > pre {
        border-top: 2px solid rgba(124,58,237,0.35) !important;
    }

    /* ── Responsive ────────────────────────────────────────────────────────── */
    @media (max-width: 600px) {
        .ff-hero-title { font-size: 2rem; }
        .ff-step { padding: 0.9rem 0.75rem; }
        .ff-ctx-header { flex-direction: column; align-items: flex-start; }
        .ff-err-card-top { flex-direction: column; }
        .ff-error-types-grid { grid-template-columns: repeat(2, 1fr); }
        .ff-tagline { font-size: 0.82rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="ff-hero-glow">
        <span class="ff-badge">IBM Bob 2.0 Hackathon</span>
        <h1 class="ff-hero-title">🔧 FixFlow</h1>
        <p class="ff-hero-sub">AI Bug-to-Fix Assistant</p>
        <p class="ff-hero-desc">
            Debugging is the most time-consuming part of software development.
            <strong>FixFlow</strong> cuts that time dramatically by letting you paste or upload
            an error log and receive an AI-powered root-cause analysis with concrete fix
            suggestions — all powered by <strong>IBM Bob</strong>.
        </p>
        <span class="ff-tagline">Upload an error log &rarr; get a diagnosis &rarr; apply the fix.</span>
    </div>
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
        """<div class="ff-step"><div class="ff-step-icon">📂</div>
        <div class="ff-step-title">1. Upload</div>
        <div class="ff-step-caption">Drop in your error log, stack trace, or crash report.</div></div>""",
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """<div class="ff-step"><div class="ff-step-icon">🤖</div>
        <div class="ff-step-title">2. Analyze</div>
        <div class="ff-step-caption">IBM Bob reads the log and identifies root causes.</div></div>""",
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        """<div class="ff-step"><div class="ff-step-icon">✅</div>
        <div class="ff-step-title">3. Fix</div>
        <div class="ff-step-caption">Get actionable code-level fix suggestions instantly.</div></div>""",
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

# ── Smart upload guidance — wrong file type warning ───────────────────────────
if uploaded_file is not None:
    ext = Path(uploaded_file.name).suffix.lower()
    if ext != ".txt":
        st.markdown(
            f"""
            <div class="ff-upload-warn">
                ⚠️ <strong>{uploaded_file.name}</strong> is a <code>{ext}</code> file.
                The <em>Error Log</em> uploader only accepts <code>.txt</code> files.
                If you want to upload Python source files for repository context,
                use the <strong>Repository Context</strong> section below.
            </div>
            """,
            unsafe_allow_html=True,
        )
        uploaded_file = None   # prevent analysing a non-log file

# ── Supported Error Types info card ──────────────────────────────────────────
st.markdown(
    """
    <div class="ff-error-types-card">
        <div style="font-size:0.82rem;font-weight:700;text-transform:uppercase;
                    letter-spacing:0.07em;color:var(--text-dim);margin-bottom:0.1rem;">
            Supported Error Types
        </div>
        <div style="font-size:0.78rem;color:var(--text-dim);margin-bottom:0.5rem;">
            FixFlow detects and provides fixes for these Python error types:
        </div>
        <div class="ff-error-types-grid">
            <div class="ff-error-chip"><span class="chip-icon">🔴</span>NameError</div>
            <div class="ff-error-chip"><span class="chip-icon">📦</span>ModuleNotFoundError</div>
            <div class="ff-error-chip"><span class="chip-icon">🔢</span>TypeError</div>
            <div class="ff-error-chip"><span class="chip-icon">⚠️</span>ValueError</div>
            <div class="ff-error-chip"><span class="chip-icon">📋</span>IndexError</div>
            <div class="ff-error-chip"><span class="chip-icon">🗝️</span>KeyError</div>
            <div class="ff-error-chip"><span class="chip-icon">🔧</span>AttributeError</div>
            <div class="ff-error-chip"><span class="chip-icon">✏️</span>SyntaxError</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Paste / text area ─────────────────────────────────────────────────────────
pasted_log = st.text_area(
    label="Or paste your error log here",
    value="",
    placeholder=(
        "Traceback (most recent call last):\n"
        "  File \"main.py\", line 5, in <module>\n"
        "ModuleNotFoundError: No module named 'pandas'"
    ),
    height=180,
    key="pasted_log_area",
)

st.markdown('<hr class="ff-divider">', unsafe_allow_html=True)

# ── Repository Context (optional) ────────────────────────────────────────────
st.markdown(
    """
    <div class="ff-section-head">
        <div class="ff-section-icon purple">🗂️</div>
        <span class="ff-section-label">Repository Context
            <span style="color:var(--text-dim);font-weight:400;font-size:0.85rem;">(optional)</span>
        </span>
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

# ── Smart upload guidance — wrong file type in repo uploader ──────────────────
if repo_py_files:
    wrong = [f.name for f in repo_py_files if Path(f.name).suffix.lower() != ".py"]
    if wrong:
        st.markdown(
            f"""
            <div class="ff-upload-warn">
                ⚠️ The following file(s) are not <code>.py</code> files and will be skipped:
                <strong>{', '.join(wrong)}</strong>.<br>
                The <em>Repository Context</em> uploader only accepts Python source files.
                To analyze an error log, use the <strong>Upload Error Log</strong> section above.
            </div>
            """,
            unsafe_allow_html=True,
        )
        # Filter to only .py files
        repo_py_files = [f for f in repo_py_files if Path(f.name).suffix.lower() == ".py"]

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

                # ── Per-error enrichment ──────────────────────────────────────
                severity  = get_severity(err.name)          # High / Medium / Low
                fix_time  = estimate_fix_time(err.name)     # e.g. "3–10 min"
                sev_cls   = severity.lower()                # css class
                sev_icon  = {"high": "🔴", "medium": "🟡", "low": "🟢"}[sev_cls]

                # ── Error card header ─────────────────────────────────────────
                st.markdown(
                    f"""
                    <div class="ff-err-card sev-{sev_cls}">
                        <div class="ff-err-card-top">
                            <div>
                                <div class="ff-err-title">{err.emoji} {err.name}</div>
                                <div class="ff-err-loc">📍 Found at: {line_refs}</div>
                            </div>
                            <div style="display:flex;gap:0.5rem;align-items:center;flex-wrap:wrap;">
                                <span class="ff-sev-badge {sev_cls}">{sev_icon} {severity}</span>
                                <span class="ff-time-card">
                                    <span class="ff-time-icon">⏱️</span>
                                    Est. fix: {fix_time}
                                </span>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                with st.expander("View details", expanded=True):
                    # ── Confidence score ──────────────────────────────────────
                    # context_matches not yet computed here; pass [] for first card pass
                    conf = score_confidence(log_text, results, [])
                    st.markdown(
                        f"""
                        <div class="ff-confidence-row">
                            <span>Analysis confidence:</span>
                            <span class="ff-confidence-pct">{conf}%</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.progress(conf / 100)

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
                # Re-score confidence now that we have context
                final_conf = score_confidence(log_text, results, context_matches)

                for match in context_matches:
                    conf_cls     = match.confidence.lower()
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

                # Updated confidence banner after context
                st.markdown(
                    f"""
                    <div style="display:flex;align-items:center;gap:0.6rem;
                                margin:0.5rem 0 0.2rem;font-size:0.82rem;color:var(--text-muted);">
                        <span>Final analysis confidence (with repository context):</span>
                        <span style="font-weight:700;color:var(--purple-light);">{final_conf}%</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.progress(final_conf / 100)

        # ── Generate and store PDF in session state ───────────────────────────
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
        <span class="ff-footer-brand">FixFlow</span> v1.0
        &nbsp;·&nbsp; Built with ❤️ for
        <a href="https://www.ibm.com" target="_blank">IBM Bob 2.0 Hackathon</a>
    </div>
    """,
    unsafe_allow_html=True,
)
