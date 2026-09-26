"""
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
