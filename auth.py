"""
auth.py

FixFlow – Milestone 7 authentication helpers.

All credentials are stored in st.session_state for the current browser session
only — no database, no file I/O.  This is intentional: the requirement is a
simple local-session gate, not a production auth system.

Public API
----------
init_auth()          → ensure session_state keys exist (call once, at startup)
render_auth_page()   → draw the full login / sign-up / forgot-password UI
is_authenticated()   → bool — True when the user has logged in this session
"""

from __future__ import annotations

import hashlib

import streamlit as st

# ── Default demo account (always available) ──────────────────────────────────
_DEFAULT_EMAIL    = "demo@fixflow.ai"
_DEFAULT_PASSWORD = "fixflow2025"


# ── Helpers ───────────────────────────────────────────────────────────────────

def _hash(password: str) -> str:
    """SHA-256 hash so plaintext passwords aren't stored in session_state."""
    return hashlib.sha256(password.encode()).hexdigest()


def init_auth() -> None:
    """
    Ensure all auth-related session_state keys are initialised.
    Must be called before any auth check or render.
    """
    if "ff_authenticated" not in st.session_state:
        st.session_state["ff_authenticated"] = False
    if "ff_current_user" not in st.session_state:
        st.session_state["ff_current_user"] = ""
    if "ff_auth_view" not in st.session_state:
        # "login" | "signup" | "forgot"
        st.session_state["ff_auth_view"] = "login"
    if "ff_users" not in st.session_state:
        # Registry: {email: hashed_password}
        st.session_state["ff_users"] = {
            _DEFAULT_EMAIL: _hash(_DEFAULT_PASSWORD),
        }


def is_authenticated() -> bool:
    """Return True if the user has authenticated this session."""
    return bool(st.session_state.get("ff_authenticated", False))


# ── CSS shared with auth page ─────────────────────────────────────────────────

_AUTH_CSS = """
<style>
/* ── Auth card ─────────────────────────────────────────────────────────────── */
.ff-auth-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem 0 3rem;
}
.ff-auth-card {
    background: #1a1d27;
    border: 1px solid #2a2d3e;
    border-radius: 16px;
    padding: 2.5rem 2rem 2rem;
    width: 100%;
    max-width: 420px;
    box-shadow: 0 8px 40px rgba(0,0,0,0.5);
}
.ff-auth-logo {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #93c5fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    margin-bottom: 0.2rem;
}
.ff-auth-subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 0.88rem;
    margin-bottom: 1.8rem;
}
.ff-auth-divider {
    border: none;
    border-top: 1px solid #2a2d3e;
    margin: 1.2rem 0;
}
.ff-auth-link-row {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin-top: 0.8rem;
}
.ff-demo-hint {
    background: rgba(124,58,237,0.08);
    border: 1px solid #7c3aed;
    border-radius: 8px;
    padding: 0.55rem 0.9rem;
    font-size: 0.8rem;
    color: #a78bfa;
    text-align: center;
    margin-top: 1rem;
}
</style>
"""


# ── View renderers ─────────────────────────────────────────────────────────────

def _render_login() -> None:
    st.markdown(
        """
        <div class="ff-auth-logo">🔧 FixFlow</div>
        <div class="ff-auth-subtitle">AI Bug-to-Fix Assistant &nbsp;·&nbsp; IBM Bob 2.0 Hackathon</div>
        """,
        unsafe_allow_html=True,
    )

    email    = st.text_input("Email",    placeholder="you@example.com", key="login_email")
    password = st.text_input("Password", placeholder="••••••••",        key="login_password", type="password")

    if st.button("🔑  Login", type="primary", use_container_width=True, key="btn_login"):
        email = email.strip().lower()
        users: dict = st.session_state["ff_users"]
        if email in users and users[email] == _hash(password):
            st.session_state["ff_authenticated"] = True
            st.session_state["ff_current_user"]  = email
            st.rerun()
        else:
            st.error("Incorrect email or password.", icon="🔒")

    st.markdown('<hr class="ff-auth-divider">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝  Sign Up", use_container_width=True, key="btn_goto_signup"):
            st.session_state["ff_auth_view"] = "signup"
            st.rerun()
    with col2:
        if st.button("🔓  Forgot Password", use_container_width=True, key="btn_goto_forgot"):
            st.session_state["ff_auth_view"] = "forgot"
            st.rerun()

    st.markdown(
        f'<div class="ff-demo-hint">Demo account: <strong>{_DEFAULT_EMAIL}</strong> / <strong>{_DEFAULT_PASSWORD}</strong></div>',
        unsafe_allow_html=True,
    )


def _render_signup() -> None:
    st.markdown(
        """
        <div class="ff-auth-logo">🔧 FixFlow</div>
        <div class="ff-auth-subtitle">Create a new account</div>
        """,
        unsafe_allow_html=True,
    )

    email    = st.text_input("Email",            placeholder="you@example.com", key="su_email")
    password = st.text_input("Password",         placeholder="Choose a password", key="su_password",  type="password")
    confirm  = st.text_input("Confirm Password", placeholder="Repeat password",  key="su_confirm",   type="password")

    if st.button("✅  Create Account", type="primary", use_container_width=True, key="btn_signup"):
        email = email.strip().lower()
        if not email or not password:
            st.error("Email and password are required.", icon="⚠️")
        elif password != confirm:
            st.error("Passwords do not match.", icon="⚠️")
        elif len(password) < 6:
            st.error("Password must be at least 6 characters.", icon="⚠️")
        elif email in st.session_state["ff_users"]:
            st.error("An account with that email already exists.", icon="⚠️")
        else:
            st.session_state["ff_users"][email] = _hash(password)
            st.success("Account created! You can now log in.", icon="✅")
            st.session_state["ff_auth_view"] = "login"
            st.rerun()

    st.markdown('<hr class="ff-auth-divider">', unsafe_allow_html=True)
    if st.button("← Back to Login", use_container_width=True, key="btn_back_from_signup"):
        st.session_state["ff_auth_view"] = "login"
        st.rerun()


def _render_forgot() -> None:
    st.markdown(
        """
        <div class="ff-auth-logo">🔧 FixFlow</div>
        <div class="ff-auth-subtitle">Reset your password</div>
        """,
        unsafe_allow_html=True,
    )

    email       = st.text_input("Email",        placeholder="Registered email address", key="fp_email")
    new_pass    = st.text_input("New Password", placeholder="New password",             key="fp_new",    type="password")
    confirm     = st.text_input("Confirm",      placeholder="Repeat new password",      key="fp_confirm", type="password")

    if st.button("🔄  Reset Password", type="primary", use_container_width=True, key="btn_reset"):
        email = email.strip().lower()
        users: dict = st.session_state["ff_users"]
        if not email or not new_pass:
            st.error("All fields are required.", icon="⚠️")
        elif email not in users:
            st.error("No account found with that email.", icon="⚠️")
        elif new_pass != confirm:
            st.error("Passwords do not match.", icon="⚠️")
        elif len(new_pass) < 6:
            st.error("Password must be at least 6 characters.", icon="⚠️")
        else:
            users[email] = _hash(new_pass)
            st.success("Password reset successfully! You can now log in.", icon="✅")
            st.session_state["ff_auth_view"] = "login"
            st.rerun()

    st.markdown('<hr class="ff-auth-divider">', unsafe_allow_html=True)
    if st.button("← Back to Login", use_container_width=True, key="btn_back_from_forgot"):
        st.session_state["ff_auth_view"] = "login"
        st.rerun()


# ── Public entry point ────────────────────────────────────────────────────────

def render_auth_page() -> None:
    """
    Render the full authentication UI (login / sign-up / forgot-password).
    Injects its own CSS; does not depend on the main app's CSS block.
    """
    st.markdown(_AUTH_CSS, unsafe_allow_html=True)

    # Centre the card using columns
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        view = st.session_state.get("ff_auth_view", "login")
        if view == "signup":
            _render_signup()
        elif view == "forgot":
            _render_forgot()
        else:
            _render_login()
