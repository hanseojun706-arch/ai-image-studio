import os
import io
import re
import sqlite3
import hashlib
import secrets
from datetime import datetime

import requests
import streamlit as st
from PIL import Image
from huggingface_hub import InferenceClient

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="AI Image Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# SETTINGS
# =========================================================
APP_TITLE = "AI Image Studio"
GUMROAD_URL = "https://aiimagestudio.gumroad.com/l/yrpblj"

# Put these in Streamlit secrets or environment variables
HF_TOKEN = st.secrets.get("HF_TOKEN", os.getenv("HF_TOKEN", ""))
HF_MODEL = st.secrets.get(
    "HF_MODEL",
    os.getenv("HF_MODEL", "black-forest-labs/FLUX.1-schnell")
)

GUMROAD_PRODUCT_ID = st.secrets.get(
    "GUMROAD_PRODUCT_ID",
    os.getenv("GUMROAD_PRODUCT_ID", "")
)

ADMIN_PASSWORD = st.secrets.get(
    "ADMIN_PASSWORD",
    os.getenv("ADMIN_PASSWORD", "")
)

FREE_LIMIT = 1
DB_PATH = "ai_image_studio.db"

# =========================================================
# STYLES
# =========================================================
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0b1020 0%, #111827 40%, #1f2937 100%);
        color: #ffffff;
    }

    .hero-box {
        padding: 28px;
        border-radius: 24px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.12);
        backdrop-filter: blur(12px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        margin-bottom: 20px;
    }

    .card {
        padding: 20px;
        border-radius: 22px;
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.10);
        margin-bottom: 14px;
    }

    .big-title {
        font-size: 3rem;
        font-weight: 800;
        line-height: 1.05;
        margin-bottom: 8px;
        color: #ffffff;
    }

    .subtext {
        font-size: 1rem;
        color: #d1d5db;
        margin-bottom: 10px;
    }

    .pill {
        display: inline-block;
        padding: 8px 14px;
        border-radius: 999px;
        background: linear-gradient(90deg, #7c3aed, #ec4899);
        color: white;
        font-size: 0.9rem;
        font-weight: 700;
        margin-right: 8px;
        margin-top: 8px;
    }

    .small-note {
        color: #cbd5e1;
        font-size: 0.92rem;
    }

    .success-box {
        padding: 14px;
        border-radius: 14px;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.35);
        margin-top: 10px;
    }

    .warning-box {
        padding: 14px;
        border-radius: 14px;
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid rgba(245, 158, 11, 0.35);
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# DATABASE
# =========================================================
def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_hash TEXT UNIQUE,
            email_plain TEXT,
            generations_used INTEGER DEFAULT 0,
            is_premium INTEGER DEFAULT 0,
            premium_source TEXT,
            premium_since TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS premium_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            created_at TEXT,
            created_by TEXT,
            redeemed INTEGER DEFAULT 0,
            redeemed_at TEXT,
            redeemed_by_email_hash TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# =========================================================
# HELPERS
# =========================================================
def normalize_email(email: str) -> str:
    return (email or "").strip().lower()

def is_valid_email(email: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email or ""))

def hash_email(email: str) -> str:
    return hashlib.sha256(normalize_email(email).encode()).hexdigest()

def get_user(email: str):
    email = normalize_email(email)
    email_hash = hash_email(email)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email_hash = ?", (email_hash,))
    row = cur.fetchone()
    conn.close()
    return row

def ensure_user(email: str):
    email = normalize_email(email)
    email_hash = hash_email(email)

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE email_hash = ?", (email_hash,))
    exists = cur.fetchone()

    if not exists:
        cur.execute("""
            INSERT INTO users (email_hash, email_plain, generations_used, is_premium, premium_source, premium_since)
            VALUES (?, ?, 0, 0, '', '')
        """, (email_hash, email))

    conn.commit()
    conn.close()

def increment_generation(email: str):
    email_hash = hash_email(email)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users
        SET generations_used = generations_used + 1
        WHERE email_hash = ?
    """, (email_hash,))
    conn.commit()
    conn.close()

def set_premium(email: str, source: str):
    email = normalize_email(email)
    email_hash = hash_email(email)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users
        SET is_premium = 1,
            premium_source = ?,
            premium_since = ?
        WHERE email_hash = ?
    """, (source, datetime.utcnow().isoformat(), email_hash))
    conn.commit()
    conn.close()

def create_local_premium_code(created_by: str = "admin") -> str:
    raw = secrets.token_hex(8).upper()
    code = f"AIS-{raw[:4]}-{raw[4:8]}-{raw[8:12]}-{raw[12:16]}"
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO premium_codes (code, created_at, created_by, redeemed)
        VALUES (?, ?, ?, 0)
    """, (code, datetime.utcnow().isoformat(), created_by))
    conn.commit()
    conn.close()
    return code

def redeem_local_premium_code(email: str, code: str):
    email_hash = hash_email(email)
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM premium_codes WHERE code = ?
    """, (code.strip().upper(),))
    row = cur.fetchone()

    if not row:
        conn.close()
        return False, "Invalid code."

    if row["redeemed"] == 1:
        conn.close()
        return False, "This code has already been used."

    cur.execute("""
        UPDATE premium_codes
        SET redeemed = 1,
            redeemed_at = ?,
            redeemed_by_email_hash = ?
        WHERE code = ?
    """, (datetime.utcnow().isoformat(), email_hash, code.strip().upper()))

    conn.commit()
    conn.close()

    set_premium(email, "local_code")
    return True, "Premium unlocked successfully."

def verify_gumroad_license(license_key: str):
    """
    Verifies a Gumroad license key.
    Requires GUMROAD_PRODUCT_ID in secrets.
    """
    if not GUMROAD_PRODUCT_ID:
        return False, "Missing GUMROAD_PRODUCT_ID in secrets."

    try:
        payload = {
            "product_id": GUMROAD_PRODUCT_ID,
            "license_key": license_key.strip(),
            "increment_uses_count": "false",
        }

        response = requests.post(
            "https://api.gumroad.com/v2/licenses/verify",
            data=payload,
            timeout=30,
        )
        data = response.json()

        if response.status_code != 200:
            return False, data.get("message", "License verification failed.")

        if not data.get("success"):
            return False, data.get("message", "Invalid Gumroad license.")

        purchase = data.get("purchase", {})
        if purchase is None:
            return False, "License verified response was incomplete."

        return True, "Gumroad license verified."
    except requests.RequestException:
        return False, "Network error while verifying Gumroad license."
    except Exception:
        return False, "Unexpected error while verifying Gumroad license."

def can_generate(email: str):
    user = get_user(email)
    if not user:
        return False, "User not found."

    if int(user["is_premium"]) == 1:
        return True, "Premium user."

    if int(user["generations_used"]) < FREE_LIMIT:
        return True, "Free generation available."

    return False, "Free limit reached. Upgrade to premium."

def generate_image_hf(prompt: str, negative_prompt: str, width: int, height: int):
    if not HF_TOKEN:
        raise RuntimeError(
            "HF_TOKEN is missing. Add your Hugging Face token in Streamlit secrets."
        )

    client = InferenceClient(api_key=HF_TOKEN)

    image = client.text_to_image(
        prompt=prompt,
        negative_prompt=negative_prompt if negative_prompt else None,
        model=HF_MODEL,
        width=width,
        height=height,
    )

    if isinstance(image, Image.Image):
        return image

    # fallback safety
    if isinstance(image, bytes):
        return Image.open(io.BytesIO(image))

    raise RuntimeError("Image generation did not return a valid image.")

# =========================================================
# SESSION STATE
# =========================================================
if "email" not in st.session_state:
    st.session_state.email = ""

if "premium" not in st.session_state:
    st.session_state.premium = False

if "last_image" not in st.session_state:
    st.session_state.last_image = None

# =========================================================
# HERO
# =========================================================
st.markdown(
    f"""
    <div class="hero-box">
        <div class="big-title">{APP_TITLE}</div>
        <div class="subtext">
            Beautiful AI image generation with free trial, premium unlock, Gumroad checkout, and one-time premium codes.
        </div>
        <span class="pill">Free limit = {FREE_LIMIT}</span>
        <span class="pill">Premium unlock</span>
        <span class="pill">Code-based access</span>
        <span class="pill">Gumroad ready</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.header("Account")
    email = st.text_input("Your email", value=st.session_state.email, placeholder="you@example.com")
    email = normalize_email(email)
    st.session_state.email = email

    if email and is_valid_email(email):
        ensure_user(email)
        user = get_user(email)
        st.session_state.premium = bool(user["is_premium"])

        st.success("Account ready")
        st.write(f"Generations used: **{user['generations_used']}**")
        st.write(f"Premium: **{'Yes' if int(user['is_premium']) == 1 else 'No'}**")
    elif email:
        st.warning("Enter a valid email address.")

    st.divider()
    st.header("Premium")
    st.markdown(f"[Buy Premium on Gumroad]({GUMROAD_URL})")

    license_key = st.text_input("Gumroad license key", type="password", placeholder="Paste Gumroad license key")
    if st.button("Verify Gumroad License", use_container_width=True):
        if not email or not is_valid_email(email):
            st.error("Enter a valid email first.")
        elif not license_key.strip():
            st.error("Paste your Gumroad license key.")
        else:
            ok, msg = verify_gumroad_license(license_key)
            if ok:
                set_premium(email, "gumroad_license")
                st.session_state.premium = True
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

    redeem_code = st.text_input("Unlock premium with code", placeholder="AIS-XXXX-XXXX-XXXX")
    if st.button("Redeem Code", use_container_width=True):
        if not email or not is_valid_email(email):
            st.error("Enter a valid email first.")
        elif not redeem_code.strip():
            st.error("Enter your premium code.")
        else:
            ok, msg = redeem_local_premium_code(email, redeem_code)
            if ok:
                st.session_state.premium = True
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

    st.divider()
    st.caption("Codes are one-time use and tied to the email that redeems them.")

# =========================================================
# MAIN LAYOUT
# =========================================================
left, right = st.columns([1.15, 0.85], gap="large")

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Image Generator")

    prompt = st.text_area(
        "Prompt",
        placeholder="Example: a luxury futuristic fashion portrait, cinematic lighting, ultra detailed, glossy editorial style",
        height=140,
    )

    negative_prompt = st.text_input(
        "Negative prompt",
        placeholder="blurry, low quality, deformed, text, watermark"
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        width = st.selectbox("Width", [512, 768, 1024], index=1)
    with c2:
        height = st.selectbox("Height", [512, 768, 1024], index=1)
    with c3:
        style = st.selectbox(
            "Style",
            ["Cinematic", "Realistic", "Anime", "Fantasy", "Luxury", "Minimal"],
            index=0,
        )

    enhance = st.checkbox("Enhance prompt automatically", value=True)

    final_prompt = prompt.strip()
    if enhance and final_prompt:
        style_map = {
            "Cinematic": "cinematic lighting, dramatic composition, high detail",
            "Realistic": "photorealistic, natural textures, sharp focus",
            "Anime": "anime illustration, expressive, vivid colors",
            "Fantasy": "fantasy art, magical atmosphere, detailed environment",
            "Luxury": "luxury aesthetic, glossy finish, elegant composition",
            "Minimal": "minimal clean design, refined composition, soft lighting",
        }
        final_prompt = f"{final_prompt}, {style_map.get(style, '')}"

    generate_clicked = st.button("Generate Image", type="primary", use_container_width=True)

    if generate_clicked:
        if not email or not is_valid_email(email):
            st.error("Please enter a valid email in the sidebar first.")
        elif not final_prompt:
            st.error("Please enter a prompt.")
        else:
            allowed, reason = can_generate(email)
            if not allowed:
                st.error(reason)
                st.info("Buy premium on Gumroad or redeem a premium code.")
            else:
                try:
                    with st.spinner("Generating your image..."):
                        img = generate_image_hf(
                            prompt=final_prompt,
                            negative_prompt=negative_prompt,
                            width=width,
                            height=height,
                        )

                    st.session_state.last_image = img

                    user = get_user(email)
                    if int(user["is_premium"]) == 0:
                        increment_generation(email)

                    st.success("Image generated successfully.")
                except Exception as e:
                    st.error(f"Generation failed: {str(e)}")

    if st.session_state.last_image is not None:
        st.image(st.session_state.last_image, caption="Generated Image", use_container_width=True)

        buf = io.BytesIO()
        st.session_state.last_image.save(buf, format="PNG")
        st.download_button(
            label="Download PNG",
            data=buf.getvalue(),
            file_name="ai_image_studio_output.png",
            mime="image/png",
            use_container_width=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("How Premium Works")
    st.markdown(
        f"""
        - **Free users:** {FREE_LIMIT} image only  
        - **Premium users:** unlimited generations  
        - **Buy link:** [Open Gumroad checkout]({GUMROAD_URL})  
        - **Unlock methods:** Gumroad license key or one-time premium code  
        """
    )
    st.markdown(
        """
        <div class="warning-box">
        Premium codes are stored locally in the app database and become invalid after one redemption.
        This helps reduce code sharing.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Admin: Generate Premium Codes")

    admin_pw = st.text_input("Admin password", type="password", placeholder="Enter admin password")
    count = st.number_input("Number of codes", min_value=1, max_value=20, value=3, step=1)

    if st.button("Generate Codes", use_container_width=True):
        if not ADMIN_PASSWORD:
            st.error("ADMIN_PASSWORD is missing in secrets.")
        elif admin_pw != ADMIN_PASSWORD:
            st.error("Wrong admin password.")
        else:
            created_codes = []
            for _ in range(int(count)):
                created_codes.append(create_local_premium_code(created_by="admin"))
            st.success("Codes generated successfully.")
            st.code("\n".join(created_codes), language="text")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Deployment Notes")
    st.markdown(
        """
        1. Add your secrets before deploying.  
        2. Enable Gumroad license keys for your product.  
        3. Add your Gumroad product ID to secrets.  
        4. Add your Hugging Face token to secrets for image generation.  
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)