import streamlit as st
import requests
from PIL import Image
import io
import datetime

# -----------------------------
# Config
# -----------------------------
APP_NAME = "AI Image Studio"
APP_TAGLINE = "Create stunning AI images instantly for social media, ads, and creative projects."
FREE_DAILY_LIMIT = 1
PREMIUM_LINK = "https://aiimagestudio.gumroad.com/l/yrpblj"
PREMIUM_CODE = "AISTUDIO2026"

HF_TOKEN = st.secrets.get("HF_TOKEN", "")

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(page_title=APP_NAME, page_icon="🎨", layout="wide")

# -----------------------------
# Daily usage tracking
# -----------------------------
today = str(datetime.date.today())

if "usage_date" not in st.session_state:
    st.session_state.usage_date = today

if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0

if "premium_unlocked" not in st.session_state:
    st.session_state.premium_unlocked = False

if "history" not in st.session_state:
    st.session_state.history = []

if st.session_state.usage_date != today:
    st.session_state.usage_date = today
    st.session_state.usage_count = 0

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #0b1020 0%, #111827 100%);
    color: white;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

.hero {
    background: linear-gradient(135deg, rgba(79,70,229,0.35), rgba(168,85,247,0.25));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 2.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 12px 40px rgba(0,0,0,0.28);
}

.hero-title {
    font-size: 3rem;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 0.5rem;
    color: white;
}

.hero-sub {
    font-size: 1.05rem;
    color: #d1d5db;
    max-width: 700px;
    margin-bottom: 1rem;
}

.badge {
    display: inline-block;
    padding: 0.45rem 0.8rem;
    margin-right: 0.5rem;
    margin-top: 0.4rem;
    border-radius: 999px;
    background: rgba(255,255,255,0.08);
    color: #e5e7eb;
    font-size: 0.85rem;
    border: 1px solid rgba(255,255,255,0.08);
}

.card {
    background: rgba(17,24,39,0.85);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 8px 24px rgba(0,0,0,0.18);
}

.card-title {
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 0.35rem;
    color: white;
}

.card-sub {
    color: #9ca3af;
    margin-bottom: 0.8rem;
}

.feature-box {
    background: rgba(31,41,55,0.8);
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.06);
    padding: 1rem;
    height: 100%;
}

.feature-head {
    font-size: 1.05rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
    color: #f3f4f6;
}

.feature-text {
    color: #cbd5e1;
    font-size: 0.93rem;
}

.price-box {
    background: rgba(31,41,55,0.85);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 1rem;
    height: 100%;
}

.price-box.premium {
    border: 1px solid rgba(168,85,247,0.5);
    box-shadow: 0 10px 25px rgba(168,85,247,0.12);
}

.price-name {
    font-size: 1.1rem;
    font-weight: 700;
    color: white;
}

.price-value {
    font-size: 2rem;
    font-weight: 800;
    margin: 0.4rem 0;
    color: white;
}

.small-muted {
    color: #94a3b8;
    font-size: 0.9rem;
}

.status-free {
    padding: 0.9rem 1rem;
    border-radius: 14px;
    background: rgba(127,29,29,0.4);
    border: 1px solid rgba(248,113,113,0.25);
    color: #fecaca;
    margin-bottom: 1rem;
}

.status-premium {
    padding: 0.9rem 1rem;
    border-radius: 14px;
    background: rgba(20,83,45,0.35);
    border: 1px solid rgba(74,222,128,0.25);
    color: #bbf7d0;
    margin-bottom: 1rem;
}

.footer {
    text-align: center;
    color: #9ca3af;
    margin-top: 1rem;
    font-size: 0.9rem;
}

.stTextArea textarea, .stTextInput input {
    background-color: #0f172a !important;
    color: white !important;
    border-radius: 14px !important;
    border: 1px solid #374151 !important;
}

.stSelectbox > div > div {
    background-color: #0f172a !important;
    color: white !important;
    border-radius: 14px !important;
    border: 1px solid #374151 !important;
}

div.stButton > button, a[data-testid="stLinkButton"] {
    width: 100%;
    border-radius: 14px !important;
    font-weight: 700 !important;
}

div.stButton > button {
    border: none;
    background: linear-gradient(135deg, #4f46e5, #9333ea);
    color: white;
    padding: 0.8rem 1rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown("## 💎 Premium")
    st.link_button("Buy Premium", PREMIUM_LINK)

    premium_code_input = st.text_input("Enter Premium Code", type="password")

    if st.button("Unlock Premium"):
        if premium_code_input.strip() == PREMIUM_CODE:
            st.session_state.premium_unlocked = True
            st.success("Premium unlocked successfully.")
        else:
            st.error("Invalid premium code.")

    st.markdown("---")
    if st.session_state.premium_unlocked:
        st.success("Unlimited access active")
    else:
        remaining = max(FREE_DAILY_LIMIT - st.session_state.usage_count, 0)
        st.info(f"Free images left today: {remaining}")

    st.markdown("---")
    st.markdown("### Recent Prompts")
    if st.session_state.history:
        for item in st.session_state.history[:5]:
            st.caption(item)
    else:
        st.caption("No prompts yet")

# -----------------------------
# Hero section
# -----------------------------
st.markdown(f"""
<div class="hero">
    <div class="hero-title">{APP_NAME}</div>
    <div class="hero-sub">{APP_TAGLINE}</div>
    <span class="badge">🎨 AI Art Generator</span>
    <span class="badge">⚡ Fast Results</span>
    <span class="badge">📱 Social Media Ready</span>
    <span class="badge">⬇️ Instant Download</span>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Features
# -----------------------------
st.markdown("""
<div class="card">
    <div class="card-title">Powerful features</div>
    <div class="card-sub">Everything users need in a modern AI image generation website.</div>
</div>
""", unsafe_allow_html=True)

f1, f2, f3 = st.columns(3)
with f1:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-head">Smart text-to-image</div>
        <div class="feature-text">Turn simple words into posters, product ads, portraits, thumbnails, and creative visuals.</div>
    </div>
    """, unsafe_allow_html=True)
with f2:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-head">Fast workflow</div>
        <div class="feature-text">
