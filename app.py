import os
import requests
import streamlit as st
from dotenv import load_dotenv
from streamlit import components

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Feedback System",
    page_icon="⭐",
    layout="centered"
)

st.markdown(
    """
    <style>
    .main {
        max-width: 760px;
        margin: 0 auto;
    }
    body {
        background: radial-gradient(circle at top left, #0b1020 0, #020617 45%, #000000 100%);
    }
    .app-title-row {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        margin-bottom: 0.2rem;
        margin-top: 1.6rem;
    }
    .app-title-icon {
        width: 34px;
        height: 34px;
        border-radius: 999px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: radial-gradient(circle at 30% 10%, #facc15, #f97316);
        box-shadow: 0 0 16px rgba(250,204,21,0.7);
        font-size: 1.4rem;
    }
    .app-title {
        font-size: 1.85rem;
        font-weight: 700;
        letter-spacing: 0.01em;
        color: #e5e7eb;
    }
    .app-subtitle {
        font-size: 0.96rem;
        color: #9ca3af;
        margin-bottom: 1.1rem;
    }
    .chip-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin-bottom: 1.5rem;
    }
    .chip {
        padding: 0.18rem 0.7rem;
        border-radius: 999px;
        background: rgba(15,23,42,0.9);
        border: 1px solid rgba(148,163,184,0.55);
        font-size: 0.74rem;
        color: #9ca3af;
    }
    .section-title {
        font-size: 1.03rem;
        font-weight: 600;
        margin-top: 0.2rem;
        margin-bottom: 0.35rem;
        color: #e5e7eb;
    }
    .hint-text {
        font-size: 0.86rem;
        color: #9ca3af;
        margin-bottom: 0.35rem;
    }
    .success-box, .error-box {
        padding: 0.85rem 0.9rem;
        border-radius: 10px;
        font-size: 0.9rem;
        margin-top: 1.1rem;
    }
    .success-box {
        background: rgba(22,163,74,0.08);
        border: 1px solid #22c55e;
        color: #bbf7d0;
    }
    .error-box {
        background: rgba(153,27,27,0.16);
        border: 1px solid #fb7185;
        color: #fecaca;
    }
    .char-counter {
        font-size: 0.8rem;
        color: #9ca3af;
        text-align: right;
        margin-top: -0.35rem;
        margin-bottom: 0.15rem;
    }
    .footer-text {
        font-size: 0.78rem;
        color: #6b7280;
        text-align: center;
        margin-top: 1.3rem;
        margin-bottom: 1.0rem;
    }
    /* Stars as futuristic pills */
    .star-row {
        display: flex;
        align-items: center;
        gap: 0.45rem;
        padding-top: 0.15rem;
    }
    .star-button button {
        width: 40px !important;
        height: 40px !important;
        border-radius: 999px !important;
        border: 1px solid rgba(148,163,184,0.45) !important;
        background: radial-gradient(circle at 30% 0, #111827, #020617) !important;
        color: #e5e7eb !important;
        font-size: 1.3rem !important;
        line-height: 1 !important;
        padding: 0 !important;
        box-shadow: 0 0 0 rgba(0,0,0,0) !important;
    }
    .star-button button:hover {
        border-color: rgba(248,250,252,0.8) !important;
        box-shadow: 0 0 14px rgba(250,204,21,0.85) !important;
        transform: translateY(-1px) scale(1.03);
    }
    .star-button-selected button {
        border-color: #facc15 !important;
        box-shadow: 0 0 16px rgba(250,204,21,0.9) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# State
if "rating" not in st.session_state:
    st.session_state.rating = 5
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "ai_response" not in st.session_state:
    st.session_state.ai_response = ""

# HEADER (no surrounding card)
st.markdown(
    """
    <div class="app-title-row">
        <div class="app-title-icon">⭐</div>
        <div class="app-title">Feedback Portal</div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="app-subtitle">Share how your session felt. A tiny bit of text here shapes the future of this system.</div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="chip-row">
        <span class="chip">Realtime</span>
        <span class="chip">Anonymous</span>
        <span class="chip">AI‑summarised</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# Rating
st.markdown('<div class="section-title">Rate your experience</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hint-text">Use the slider or tap a star. Both control the same rating.</div>',
    unsafe_allow_html=True,
)

col_slider, col_stars = st.columns([3, 2])

with col_slider:
    st.session_state.rating = st.slider(
        "Rating",
        min_value=1,
        max_value=5,
        value=st.session_state.rating,
        label_visibility="collapsed",
        help="1 = Poor · 5 = Excellent",
    )

with col_stars:
    star_cols = st.columns(5)
    for i in range(5):
        star_val = i + 1
        label = "⭐" if star_val <= st.session_state.rating else "☆"
        css_class = "star-button-selected" if star_val <= st.session_state.rating else "star-button"
        with star_cols[i]:
            st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
            if st.button(label, key=f"star_{star_val}", help=f"{star_val} stars"):
                st.session_state.rating = star_val
            st.markdown("</div>", unsafe_allow_html=True)

    st.caption(f"You selected {st.session_state.rating}/5")

# Review
st.markdown('<div class="section-title">Tell us more</div>', unsafe_allow_html=True)
st.markdown(
    "<div class='hint-text'>Mention what worked, what felt off, or anything you'd like this system to learn from.</div>",
    unsafe_allow_html=True,
)

review = st.text_area(
    label="Write your review",
    placeholder=(
        "Example: The responses were accurate but felt a bit slow when rating multiple times in a row. "
        "A compact mobile view would be great."
    ),
    height=160,
    label_visibility="collapsed",
    max_chars=1000,
)

char_count = len(review.strip())
st.markdown(
    f'<div class="char-counter">{char_count}/1000 characters · minimum 10</div>',
    unsafe_allow_html=True,
)

submit_button = st.button("Submit feedback", type="primary", use_container_width=True)

if submit_button:
    if char_count < 10:
        st.markdown(
            '<div class="error-box">❌ Please write at least 10 characters so the AI can learn something meaningful.</div>',
            unsafe_allow_html=True,
        )
    else:
        with st.spinner("Sending your feedback to the AI engine..."):
            try:
                response = requests.post(
                    f"{API_URL}/feedback/",
                    json={"rating": st.session_state.rating, "review": review},
                    timeout=30,
                )

                if response.status_code == 201:
                    data = response.json()
                    st.session_state.submitted = True
                    st.session_state.ai_response = data.get("ai_response", "")

                    st.markdown(
                        '<div class="success-box">✅ Feedback received. Below is an AI summary tailored to your message.</div>',
                        unsafe_allow_html=True,
                    )

                elif response.status_code == 429:
                    st.markdown(
                        '<div class="error-box">⏱️ Too many submissions from this browser. Please pause a moment and retry.</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    try:
                        error_detail = response.json().get("error", "Unknown error")
                    except Exception:
                        error_detail = "Unknown error"
                    st.markdown(
                        f'<div class="error-box">❌ Something went wrong: {error_detail}</div>',
                        unsafe_allow_html=True,
                    )

            except requests.exceptions.Timeout:
                st.markdown(
                    '<div class="error-box">⏱️ The request timed out. Please check your connection and try once more.</div>',
                    unsafe_allow_html=True,
                )
            except requests.exceptions.ConnectionError:
                st.markdown(
                    '<div class="error-box">🔌 Could not reach the feedback API. Ensure the backend is live.</div>',
                    unsafe_allow_html=True,
                )
            except Exception as e:
                st.markdown(
                    f'<div class="error-box">❌ Unexpected error: {str(e)}</div>',
                    unsafe_allow_html=True,
                )

if st.session_state.submitted and st.session_state.ai_response:
    st.markdown('<div class="section-title">AI summary of your feedback</div>', unsafe_allow_html=True)
    st.info(st.session_state.ai_response)

st.markdown(
    '<div class="footer-text">Feedback powers the next iteration · Nothing here is stored with your identity.</div>',
    unsafe_allow_html=True,
)
