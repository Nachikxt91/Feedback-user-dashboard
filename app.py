import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
try:
    API_URL = st.secrets["API_URL"]
except (KeyError, FileNotFoundError):
    API_URL = os.getenv("API_URL", "http://localhost:8000/api/feedback")

st.set_page_config(
    page_title="Feedback System",
    page_icon="⭐",
    layout="centered"
)

# Responsive Styles
st.markdown(
    """
    <style>
    /* Base responsive container */
    .main .block-container {
        max-width: 800px;
        padding: 1rem 1.5rem;
        margin: 0 auto;
    }
    
    /* Dark theme */
    body {
        background: radial-gradient(circle at top left, #0b1020 0, #020617 45%, #000000 100%);
    }
    
    /* Header styles */
    .app-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 1rem 0;
        flex-wrap: wrap;
    }
    .app-icon {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #facc15, #f97316);
        box-shadow: 0 0 20px rgba(250,204,21,0.5);
        font-size: 1.5rem;
        flex-shrink: 0;
    }
    .app-title {
        font-size: clamp(1.5rem, 5vw, 2rem);
        font-weight: 700;
        color: #e5e7eb;
    }
    .app-subtitle {
        font-size: clamp(0.85rem, 2.5vw, 1rem);
        color: #9ca3af;
        margin-bottom: 1rem;
        line-height: 1.5;
    }
    
    /* Chip tags */
    .chip-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
        margin-bottom: 1.5rem;
    }
    .chip {
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        background: rgba(15,23,42,0.9);
        border: 1px solid rgba(148,163,184,0.4);
        font-size: 0.75rem;
        color: #9ca3af;
        white-space: nowrap;
    }
    
    /* Section titles */
    .section-title {
        font-size: clamp(0.9rem, 2.5vw, 1.1rem);
        font-weight: 600;
        margin: 1.5rem 0 0.5rem;
        color: #e5e7eb;
    }
    .hint-text {
        font-size: clamp(0.8rem, 2vw, 0.9rem);
        color: #9ca3af;
        margin-bottom: 0.75rem;
        line-height: 1.5;
    }
    
    /* Star rating container */
    .star-container {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        padding: 1rem 0;
    }
    .star-btn {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        border: 2px solid rgba(148,163,184,0.4);
        background: linear-gradient(135deg, #1f2937, #111827);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .star-btn:hover {
        border-color: #facc15;
        box-shadow: 0 0 15px rgba(250,204,21,0.6);
        transform: scale(1.1);
    }
    .star-btn.selected {
        border-color: #facc15;
        box-shadow: 0 0 20px rgba(250,204,21,0.8);
    }
    
    /* Feedback boxes */
    .success-box {
        padding: 1rem;
        border-radius: 12px;
        background: rgba(22,163,74,0.1);
        border: 1px solid #22c55e;
        color: #bbf7d0;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 12px;
        background: rgba(153,27,27,0.15);
        border: 1px solid #fb7185;
        color: #fecaca;
        margin: 1rem 0;
    }
    
    /* Character counter */
    .char-counter {
        font-size: 0.8rem;
        color: #6b7280;
        text-align: right;
        margin: 0.25rem 0 0.75rem;
    }
    
    /* Footer */
    .footer {
        font-size: 0.75rem;
        color: #6b7280;
        text-align: center;
        margin: 2rem 0 1rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(148,163,184,0.2);
    }
    
    /* Mobile optimizations */
    @media (max-width: 640px) {
        .main .block-container {
            padding: 0.75rem 1rem;
        }
        .star-btn {
            width: 44px;
            height: 44px;
            font-size: 1.3rem;
        }
    }
    
    /* Hide default streamlit elements */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
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

# Categories
CATEGORIES = [
    ("General", "💬"),
    ("Bug Report", "🐛"),
    ("Feature Request", "✨"),
    ("Praise", "🎉"),
    ("Complaint", "😤"),
    ("Suggestion", "💡"),
]

# HEADER
st.markdown(
    """
    <div class="app-header">
        <div class="app-icon">⭐</div>
        <div class="app-title">Feedback Portal</div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="app-subtitle">Share your experience with us. Your feedback helps us improve!</div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="chip-row">
        <span class="chip">✨ Realtime</span>
        <span class="chip">🔒 Anonymous</span>
        <span class="chip">🤖 AI-summarised</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# Category Selection
st.markdown('<div class="section-title">📁 What type of feedback?</div>', unsafe_allow_html=True)
category_options = [f"{emoji} {name}" for name, emoji in CATEGORIES]
selected_category_display = st.selectbox(
    "Category",
    options=category_options,
    index=0,
    label_visibility="collapsed"
)
selected_category = selected_category_display.split(" ", 1)[1]

# Rating Section
st.markdown('<div class="section-title">⭐ Rate your experience</div>', unsafe_allow_html=True)

# Use a single row of columns for stars
st.markdown('<div class="hint-text">Tap a star to rate (1-5)</div>', unsafe_allow_html=True)

cols = st.columns(5)
for i, col in enumerate(cols):
    star_val = i + 1
    with col:
        if star_val <= st.session_state.rating:
            if st.button("⭐", key=f"star_{star_val}", use_container_width=True):
                st.session_state.rating = star_val
                st.rerun()
        else:
            if st.button("☆", key=f"star_{star_val}", use_container_width=True):
                st.session_state.rating = star_val
                st.rerun()

st.markdown(f"**Selected: {st.session_state.rating}/5 stars**")

# Slider as alternative
st.session_state.rating = st.slider(
    "Or use slider",
    min_value=1,
    max_value=5,
    value=st.session_state.rating,
    help="Alternative way to select rating"
)

# Review Text
st.markdown('<div class="section-title">💬 Tell us more</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hint-text">Share details about your experience (minimum 10 characters)</div>',
    unsafe_allow_html=True,
)

review = st.text_area(
    label="Your feedback",
    placeholder="Example: The responses were accurate and helpful. Would love to see a dark mode option!",
    height=120,
    label_visibility="collapsed",
    max_chars=1000,
)

char_count = len(review.strip())
st.markdown(
    f'<div class="char-counter">{char_count}/1000 characters</div>',
    unsafe_allow_html=True,
)

# Submit Button
submit_button = st.button("🚀 Submit Feedback", type="primary", use_container_width=True)

if submit_button:
    if char_count < 10:
        st.markdown(
            '<div class="error-box">❌ Please write at least 10 characters to submit your feedback.</div>',
            unsafe_allow_html=True,
        )
    else:
        with st.spinner("Sending your feedback..."):
            try:
                response = requests.post(
                    f"{API_URL}",
                    json={
                        "rating": st.session_state.rating,
                        "review": review,
                        "category": selected_category
                    },
                    timeout=30,
                )

                if response.status_code == 201:
                    data = response.json()
                    st.session_state.submitted = True
                    st.session_state.ai_response = data.get("ai_response", "")
                    st.markdown(
                        '<div class="success-box">✅ Thank you! Your feedback has been submitted successfully.</div>',
                        unsafe_allow_html=True,
                    )

                elif response.status_code == 429:
                    st.markdown(
                        '<div class="error-box">⏳ Too many submissions. Please wait a moment and try again.</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    error_detail = "Unknown error"
                    try:
                        error_detail = response.json().get("detail", response.json().get("error", "Unknown error"))
                    except:
                        pass
                    st.markdown(
                        f'<div class="error-box">❌ Error: {error_detail}</div>',
                        unsafe_allow_html=True,
                    )

            except requests.exceptions.Timeout:
                st.markdown(
                    '<div class="error-box">⏱️ Request timed out. Please try again.</div>',
                    unsafe_allow_html=True,
                )
            except requests.exceptions.ConnectionError:
                st.markdown(
                    '<div class="error-box">🔌 Cannot connect to server. Is the backend running?</div>',
                    unsafe_allow_html=True,
                )
            except Exception as e:
                st.markdown(
                    f'<div class="error-box">❌ Error: {str(e)}</div>',
                    unsafe_allow_html=True,
                )

# Show AI Response
if st.session_state.submitted and st.session_state.ai_response:
    st.markdown('<div class="section-title">🤖 AI Response</div>', unsafe_allow_html=True)
    st.info(st.session_state.ai_response)

# Footer
st.markdown(
    '<div class="footer">Your feedback is anonymous and helps us improve 💙</div>',
    unsafe_allow_html=True,
)