import base64
import hashlib
import io
import random
import sqlite3
import time
from datetime import datetime, date
from pathlib import Path
from typing import Optional, Tuple

import requests
import streamlit as st
from PIL import Image

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Anu AI Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# APP SETTINGS
# ============================================================
APP_NAME = "Anu AI Studio"
TAGLINE = "AI Image & Video Generator"
CONTACT_EMAIL = "anuradha90nn@gmail.com"

FREE_IMAGE_LIMIT_PER_DAY = 5
FREE_VIDEO_LIMIT_PER_DAY = 2
FREE_VIDEO_MAX_SECONDS = 10

PREMIUM_IMAGE_LIMIT_PER_DAY = None
PREMIUM_VIDEO_LIMIT_PER_DAY = None
PREMIUM_VIDEO_MAX_SECONDS = 60

ABOUT_TEXT = """
Anu AI Studio is a modern AI platform that allows users to generate images from prompts, upload images for transformation, and preview videos easily.

This website is designed to provide a clean, simple, and professional experience so anyone can use AI tools without confusion.

Our goal is to make AI creativity accessible, fast, and visually appealing for all users.
"""

INTRO_TEXT = """
Welcome to Anu AI Studio — a simple and modern AI platform for generating images, transforming uploaded images, and working with media in one clean website.

This platform is built to be easy to understand, professional in design, and smooth for users who want creative AI tools in one place.
"""

# ============================================================
# SECRETS
# ============================================================
# Add these in Streamlit Secrets:
# POLLINATIONS_API_KEY = "your_api_key"
# PREMIUM_ACCESS_CODE = "your_premium_code"
# ADMIN_PASSWORD = "your_admin_password"

POLLINATIONS_API_KEY = st.secrets.get("POLLINATIONS_API_KEY", "")
PREMIUM_ACCESS_CODE = st.secrets.get("PREMIUM_ACCESS_CODE", "ANU-PREMIUM")
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "admin123")

POLLINATIONS_BASE = "https://gen.pollinations.ai"
DB_PATH = Path("anu_ai_studio_usage.db")

# Set this to True only if you later buy credits and want to re-enable real video generation
ENABLE_REAL_VIDEO_GENERATION = False

# ============================================================
# CUSTOM CSS
# ============================================================
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(130, 94, 255, 0.16), transparent 24%),
        radial-gradient(circle at top right, rgba(0, 194, 255, 0.14), transparent 24%),
        radial-gradient(circle at bottom left, rgba(255, 0, 140, 0.10), transparent 18%),
        linear-gradient(135deg, #0b1020 0%, #12182d 50%, #0c1325 100%);
    color: #f4f7ff;
}

.block-container {
    max-width: 1320px;
    padding-top: 1rem;
    padding-bottom: 2rem;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(15,22,45,0.98), rgba(8,13,28,0.98));
    border-right: 1px solid rgba(255,255,255,0.08);
}

.hero-card, .glass-card, .feature-card, .footer-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    box-shadow: 0 10px 34px rgba(0,0,0,0.28);
}

.hero-card {
    padding: 30px;
    margin-bottom: 18px;
}

.glass-card {
    padding: 20px;
    margin-bottom: 16px;
}

.feature-card {
    padding: 20px;
    min-height: 180px;
}

.footer-card {
    padding: 18px 22px;
    margin-top: 18px;
}

.brand-chip {
    display: inline-block;
    padding: 7px 14px;
    border-radius: 999px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    font-size: 13px;
    font-weight: 700;
    color: #dfe5ff;
    margin-bottom: 14px;
}

.hero-title {
    font-size: 3rem;
    line-height: 1.08;
    font-weight: 900;
    letter-spacing: -0.03em;
    margin-bottom: 10px;
    color: #ffffff;
}

.hero-subtitle {
    font-size: 1.05rem;
    line-height: 1.8;
    color: #d8defb;
    max-width: 860px;
}

.section-title {
    font-size: 1.45rem;
    font-weight: 900;
    color: #ffffff;
    margin-bottom: 0.2rem;
}

.section-subtitle {
    font-size: 0.98rem;
    color: #cfd8ff;
    margin-bottom: 1rem;
}

.small-note {
    color: #c8d1fb;
    font-size: 0.92rem;
    line-height: 1.75;
}

.kpi {
    background: rgba(255,255,255,0.05);
    border-radius: 18px;
    padding: 16px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.08);
}

.kpi h3 {
    margin: 0;
    font-size: 1.7rem;
    color: #ffffff;
    font-weight: 900;
}

.kpi p {
    margin: 0.3rem 0 0;
    color: #c7d1ff;
    font-size: 0.92rem;
}

.plan-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 14px;
    margin-bottom: 10px;
}

.status-chip {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 800;
    margin-top: 6px;
    margin-bottom: 8px;
}

.status-ok {
    background: rgba(45, 206, 137, 0.14);
    border: 1px solid rgba(45, 206, 137, 0.26);
    color: #b9ffd8;
}

.status-warn {
    background: rgba(255, 196, 0, 0.12);
    border: 1px solid rgba(255, 196, 0, 0.22);
    color: #ffe7a2;
}

.status-premium {
    background: rgba(123, 97, 255, 0.14);
    border: 1px solid rgba(123, 97, 255, 0.30);
    color: #e4dcff;
}

.stButton > button {
    width: 100%;
    border-radius: 14px;
    border: none;
    padding: 0.85rem 1rem;
    font-weight: 800;
    background: linear-gradient(135deg, #7b61ff 0%, #12b5ff 100%);
    color: white;
    box-shadow: 0 8px 25px rgba(95, 94, 255, 0.30);
}

.stDownloadButton > button {
    width: 100%;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.12);
    padding: 0.85rem 1rem;
    font-weight: 800;
    background: rgba(255,255,255,0.08);
    color: white;
}

div[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.04);
    border-radius: 16px;
    padding: 8px;
    border: 1px dashed rgba(255,255,255,0.18);
}

input, textarea, [data-baseweb="select"] {
    border-radius: 12px !important;
}

hr {
    border-color: rgba(255,255,255,0.10);
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ============================================================
# DATABASE
# ============================================================
def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            email TEXT,
            plan TEXT DEFAULT 'free',
            created_at TEXT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS usage (
            user_id TEXT,
            usage_date TEXT,
            image_count INTEGER DEFAULT 0,
            video_count INTEGER DEFAULT 0,
            PRIMARY KEY (user_id, usage_date)
        )
        """
    )
    conn.commit()
    conn.close()


def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def ensure_user_record(user_id: str, email: str = "") -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO users (user_id, email, plan, created_at) VALUES (?, ?, 'free', ?)",
        (user_id, email, datetime.utcnow().isoformat()),
    )
    if email:
        cur.execute("UPDATE users SET email = ? WHERE user_id = ?", (email, user_id))
    conn.commit()
    conn.close()


def set_user_plan(user_id: str, plan: str) -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE users SET plan = ? WHERE user_id = ?", (plan, user_id))
    conn.commit()
    conn.close()


def get_user_plan(user_id: str) -> str:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT plan FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row and row[0] else "free"


def get_today_usage(user_id: str) -> Tuple[int, int]:
    today = str(date.today())
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO usage (user_id, usage_date, image_count, video_count) VALUES (?, ?, 0, 0)",
        (user_id, today),
    )
    cur.execute(
        "SELECT image_count, video_count FROM usage WHERE user_id = ? AND usage_date = ?",
        (user_id, today),
    )
    row = cur.fetchone()
    conn.commit()
    conn.close()
    if not row:
        return 0, 0
    return int(row[0]), int(row[1])


def increment_image_usage(user_id: str) -> None:
    today = str(date.today())
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO usage (user_id, usage_date, image_count, video_count) VALUES (?, ?, 0, 0)",
        (user_id, today),
    )
    cur.execute(
        "UPDATE usage SET image_count = image_count + 1 WHERE user_id = ? AND usage_date = ?",
        (user_id, today),
    )
    conn.commit()
    conn.close()


def increment_video_usage(user_id: str) -> None:
    today = str(date.today())
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO usage (user_id, usage_date, image_count, video_count) VALUES (?, ?, 0, 0)",
        (user_id, today),
    )
    cur.execute(
        "UPDATE usage SET video_count = video_count + 1 WHERE user_id = ? AND usage_date = ?",
        (user_id, today),
    )
    conn.commit()
    conn.close()

# ============================================================
# SESSION STATE
# ============================================================
init_db()

if "user_id" not in st.session_state:
    seed = f"{time.time()}-{random.randint(100000,999999)}"
    st.session_state.user_id = hashlib.sha256(seed.encode()).hexdigest()[:24]

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "gallery" not in st.session_state:
    st.session_state.gallery = []

if "admin_unlocked" not in st.session_state:
    st.session_state.admin_unlocked = False

ensure_user_record(st.session_state.user_id, st.session_state.user_email)

# ============================================================
# HELPERS
# ============================================================
def render_card_open(class_name="glass-card"):
    st.markdown(f'<div class="{class_name}">', unsafe_allow_html=True)


def render_card_close():
    st.markdown("</div>", unsafe_allow_html=True)


def prompt_is_valid(prompt: str) -> bool:
    return bool(prompt and len(prompt.strip()) >= 6)


def build_enhanced_prompt(prompt: str, style: str, quality: str) -> str:
    style_map = {
        "Realistic": "highly detailed realistic photography, natural lighting, cinematic depth",
        "Anime": "beautiful anime illustration, expressive details, vibrant color storytelling",
        "Fantasy": "epic fantasy concept art, magical atmosphere, dramatic lighting",
        "Minimal": "clean minimalist composition, elegant shapes, premium aesthetic",
        "3D": "high quality 3D render, polished materials, realistic depth",
        "Portrait": "professional portrait composition, balanced face details, refined lighting",
        "Product": "premium product photography, studio lighting, advertising style",
        "Cinematic": "cinematic composition, dramatic atmosphere, ultra-detailed visuals",
    }
    quality_map = {
        "Standard": "sharp details, clear output",
        "High": "high detail, refined textures, polished output",
        "Ultra": "ultra detailed, premium quality, crisp focus, visually striking",
    }
    return f"{prompt.strip()}, {style_map.get(style, 'high quality composition')}, {quality_map.get(quality, 'sharp details')}"


def img_to_bytes(img: Image.Image, fmt: str = "PNG") -> bytes:
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    buf.seek(0)
    return buf.getvalue()


def download_link_bytes(data: bytes, filename: str, mime: str):
    st.download_button(
        label=f"Download {filename}",
        data=data,
        file_name=filename,
        mime=mime,
        use_container_width=True,
    )


def save_to_gallery(kind: str, title: str, data: bytes, mime: str):
    st.session_state.gallery.insert(
        0,
        {
            "kind": kind,
            "title": title,
            "data": data,
            "mime": mime,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
    )


def get_current_plan() -> str:
    plan = get_user_plan(st.session_state.user_id)
    st.session_state.is_premium = plan == "premium"
    return plan


def get_current_image_limit() -> Optional[int]:
    return PREMIUM_IMAGE_LIMIT_PER_DAY if get_current_plan() == "premium" else FREE_IMAGE_LIMIT_PER_DAY


def get_current_video_limit() -> Optional[int]:
    return PREMIUM_VIDEO_LIMIT_PER_DAY if get_current_plan() == "premium" else FREE_VIDEO_LIMIT_PER_DAY


def get_current_video_max_seconds() -> int:
    return PREMIUM_VIDEO_MAX_SECONDS if get_current_plan() == "premium" else FREE_VIDEO_MAX_SECONDS


def can_generate_image() -> Tuple[bool, str]:
    current_limit = get_current_image_limit()
    image_count, _ = get_today_usage(st.session_state.user_id)
    if current_limit is None:
        return True, ""
    if image_count >= current_limit:
        return False, f"Daily free image limit reached ({current_limit}/{current_limit}). Upgrade to Premium for unlimited generation."
    return True, ""


def can_generate_video() -> Tuple[bool, str]:
    current_limit = get_current_video_limit()
    _, video_count = get_today_usage(st.session_state.user_id)
    if current_limit is None:
        return True, ""
    if video_count >= current_limit:
        return False, f"Daily free video limit reached ({current_limit}/{current_limit}). Upgrade to Premium for unlimited generation."
    return True, ""


def api_headers() -> dict:
    headers = {"Content-Type": "application/json"}
    if POLLINATIONS_API_KEY:
        headers["Authorization"] = f"Bearer {POLLINATIONS_API_KEY}"
    return headers

# ============================================================
# API FUNCTIONS
# ============================================================
def generate_image_pollinations(
    prompt: str,
    model: str = "flux",
    width: int = 1024,
    height: int = 1024,
    negative_prompt: Optional[str] = None,
    seed: int = -1,
    enhance: bool = True,
    safe: bool = True,
) -> Tuple[Optional[bytes], Optional[str]]:
    if not POLLINATIONS_API_KEY:
        return None, "Missing POLLINATIONS_API_KEY in Streamlit Secrets."

    url = f"{POLLINATIONS_BASE}/v1/images/generations"
    payload = {
        "model": model,
        "prompt": prompt,
        "size": f"{width}x{height}",
        "response_format": "b64_json",
        "seed": seed,
        "enhance": enhance,
        "safe": safe,
    }
    if negative_prompt:
        payload["negative_prompt"] = negative_prompt

    try:
        response = requests.post(url, headers=api_headers(), json=payload, timeout=120)
        if response.status_code != 200:
            return None, f"API error {response.status_code}: {response.text}"

        data = response.json()
        items = data.get("data", [])
        if not items:
            return None, "No image returned by the API."

        b64_data = items[0].get("b64_json")
        if not b64_data:
            return None, "Image data missing in API response."

        return base64.b64decode(b64_data), None
    except requests.Timeout:
        return None, "Image generation timed out. Please try again."
    except Exception as e:
        return None, f"Image generation failed: {str(e)}"


def edit_image_pollinations(
    image_bytes: bytes,
    prompt: str,
    model: str = "flux",
) -> Tuple[Optional[bytes], Optional[str]]:
    if not POLLINATIONS_API_KEY:
        return None, "Missing POLLINATIONS_API_KEY in Streamlit Secrets."

    url = f"{POLLINATIONS_BASE}/v1/images/edits"
    headers = {}
    if POLLINATIONS_API_KEY:
        headers["Authorization"] = f"Bearer {POLLINATIONS_API_KEY}"

    files = {"image": ("upload.png", image_bytes, "image/png")}
    data = {"prompt": prompt, "model": model}

    try:
        response = requests.post(url, headers=headers, data=data, files=files, timeout=180)
        if response.status_code != 200:
            return None, f"API error {response.status_code}: {response.text}"

        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type:
            res_json = response.json()
            items = res_json.get("data", [])
            if items and items[0].get("b64_json"):
                return base64.b64decode(items[0]["b64_json"]), None
            if items and items[0].get("url"):
                img_res = requests.get(items[0]["url"], timeout=120)
                if img_res.status_code == 200:
                    return img_res.content, None
                return None, "Failed to download edited image."
            return None, "Unexpected edit API response."

        return response.content, None
    except requests.Timeout:
        return None, "Image edit timed out. Please try again."
    except Exception as e:
        return None, f"Image edit failed: {str(e)}"


def generate_video_pollinations(
    prompt: str,
    model: str = "wan",
    duration: int = 4,
    aspect_ratio: str = "16:9",
) -> Tuple[Optional[bytes], Optional[str]]:
    if not POLLINATIONS_API_KEY:
        return None, "Missing POLLINATIONS_API_KEY in Streamlit Secrets."

    try:
        from urllib.parse import quote

        encoded = quote(prompt.strip())
        url = (
            f"{POLLINATIONS_BASE}/image/{encoded}"
            f"?model={model}&duration={duration}&aspectRatio={aspect_ratio}&safe=true&enhance=true"
        )
        headers = {"Authorization": f"Bearer {POLLINATIONS_API_KEY}"}
        response = requests.get(url, headers=headers, timeout=300)

        if response.status_code != 200:
            return None, f"API error {response.status_code}: {response.text}"

        content_type = response.headers.get("Content-Type", "")
        if "video" not in content_type and not response.content:
            return None, "The API did not return a valid video file."

        return response.content, None
    except requests.Timeout:
        return None, "Video generation timed out. Please try again."
    except Exception as e:
        return None, f"Video generation failed: {str(e)}"

# ============================================================
# SIDEBAR
# ============================================================
def sidebar():
    ensure_user_record(st.session_state.user_id, st.session_state.user_email)

    st.sidebar.markdown(f"## {APP_NAME}")
    st.sidebar.caption(TAGLINE)
    st.sidebar.markdown("---")

    page = st.sidebar.radio(
        "Navigate",
        [
            "Home",
            "Image Generator",
            "Image Restyle",
            "Video Studio",
            "Gallery",
            "About Us",
            "Contact",
            "Premium",
        ],
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### User Details")
    email_input = st.sidebar.text_input(
        "Email / User ID",
        value=st.session_state.user_email,
        placeholder="Enter your email",
    )
    if email_input != st.session_state.user_email:
        st.session_state.user_email = email_input.strip()
        ensure_user_record(st.session_state.user_id, st.session_state.user_email)

    plan = get_current_plan()
    image_count, video_count = get_today_u
