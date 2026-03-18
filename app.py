import streamlit as st
import hashlib
import random
import string
import time
import io
import datetime
from PIL import Image
from huggingface_hub import InferenceClient

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Image Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# CUSTOM CSS – dark luxury aesthetic
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

:root {
  --gold:   #e8c97a;
  --gold2:  #f5dfa0;
  --dark:   #0a0a0f;
  --card:   #13131c;
  --border: rgba(232,201,122,0.18);
  --text:   #e8e4d8;
  --muted:  #7a7870;
}

html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif;
  background: var(--dark);
  color: var(--text);
}

.stApp {
  background: var(--dark);
}

.block-container {
  padding-top: 1rem !important;
  max-width: 1100px;
}

.hero {
  text-align: center;
  padding: 3.5rem 1rem 2rem;
}
.hero-badge {
  display: inline-block;
  background: linear-gradient(90deg,#e8c97a22,#e8c97a44);
  border: 1px solid var(--gold);
  color: var(--gold);
  font-family: 'Syne', sans-serif;
  font-size: 0.72rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  padding: 0.3rem 1rem;
  border-radius: 999px;
  margin-bottom: 1.2rem;
}
.hero h1 {
  font-family: 'Syne', sans-serif;
  font-size: clamp(2.4rem, 5vw, 4rem);
  font-weight: 800;
  background: linear-gradient(135deg, #f5dfa0 0%, #e8c97a 40%, #c9973a 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.1;
  margin: 0;
}
.hero p {
  color: var(--muted);
  font-size: 1.05rem;
  margin-top: 0.8rem;
}

.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1.6rem;
  margin-bottom: 1.2rem;
}
.card-title {
  font-family: 'Syne', sans-serif;
  font-size: 0.8rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--gold);
  margin-bottom: 0.8rem;
}
.premium-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: linear-gradient(90deg,#e8c97a,#c9973a);
  color: #0a0a0f;
  font-family: 'Syne', sans-serif;
  font-weight: 700;
  font-size: 0.78rem;
  letter-spacing: 0.1em;
  padding: 0.3rem 0.9rem;
  border-radius: 999px;
}
.free-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.12);
  color: var(--muted);
  font-family: 'Syne', sans-serif;
  font-size: 0.78rem;
  padding: 0.3rem 0.9rem;
  border-radius: 999px;
}
.gumroad-btn {
  display: block;
  width: 100%;
  text-align: center;
  background: linear-gradient(135deg,#e8c97a,#c9973a);
  color: #0a0a0f !important;
  font-family: 'Syne', sans-serif;
  font-weight: 700;
  font-size: 1rem;
  letter-spacing: 0.04em;
  text-decoration: none !important;
  padding: 0.95rem 2rem;
  border-radius: 12px;
  margin: 0.4rem 0;
}
.stat-strip {
  display: flex;
  gap: 1px;
  background: var(--border);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 1.4rem;
}
.stat-item {
  flex: 1;
  background: var(--card);
  padding: 1rem;
  text-align: center;
}
.stat-num {
  font-family: 'Syne', sans-serif;
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--gold);
}
.stat-label {
  font-size: 0.74rem;
  color: var(--muted);
  margin-top: 0.2rem;
}

.limit-bar-bg {
  height: 6px;
  background: rgba(255,255,255,0.08);
  border-radius: 999px;
  overflow: hidden;
  margin-top: 0.5rem;
}
.limit-bar-fill {
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg,#e8c97a,#c9973a);
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
  background: #1a1a26 !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  color: var(--text) !important;
}

.stButton > button {
  background: linear-gradient(135deg,#e8c97a,#c9973a) !important;
  color: #0a0a0f !important;
  font-family: 'Syne', sans-serif !important;
  font-weight: 700 !important;
  border: none !important;
  border-radius: 10px !important;
  letter-spacing: 0.04em !important;
}

div[data-testid="stExpander"] {
  background: var(--card);
  border: 1px solid var(--border) !important;
  border-radius: 12px;
}

#MainMenu, footer, header {
  visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONSTANTS & STATE INIT
# ─────────────────────────────────────────────
FREE_LIMIT = 1
GUMROAD_URL = "https://aiimagestudio.gumroad.com/l/yrpblj"

try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
except Exception:
    HF_TOKEN = ""

MODEL_OPTIONS = {
    "Premium XL": "black-forest-labs/FLUX.1-Krea-dev",
    "Fast FLUX": "black-forest-labs/FLUX.1-schnell",
    "Qwen Image": "Qwen/Qwen-Image",
}

STYLE_HINTS = {
    "Photorealistic": "ultra realistic, detailed lighting, natural textures, professional photography",
    "Cinematic": "cinematic lighting, dramatic atmosphere, film still, moody composition",
    "Oil Painting": "oil painting, rich brushstrokes, gallery artwork, classical details",
    "Watercolour": "watercolour painting, soft edges, pastel blending, elegant wash",
    "Anime / Manga": "anime style, vibrant colors, clean line art, expressive composition",
    "Pixel Art": "pixel art, retro game style, crisp pixels, stylized shading",
    "Concept Art": "concept art, highly detailed, environmental design, polished composition",
    "Sketch": "pencil sketch, hand drawn, fine detail, artistic shading",
    "Surrealist": "surreal dreamlike imagery, unexpected composition, imaginative visuals",
    "Minimalist": "minimalist design, clean composition, elegant simplicity",
}

for key, default in [
    ("premium_codes", {}),
    ("is_premium", False),
    ("free_uses", 0),
    ("generated_images", []),
    ("activated_code", None),
    ("show_unlock", False),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def get_user_id() -> str:
    if "user_id" not in st.session_state:
        st.session_state.user_id = hashlib.md5(
            str(time.time() + random.random()).encode()
        ).hexdigest()[:12]
    return st.session_state.user_id


def generate_unique_code() -> str:
    chars = string.ascii_uppercase + string.digits
    raw = "".join(random.choices(chars, k=16))
    h = hashlib.sha256((raw + str(time.time())).encode()).hexdigest()[:6].upper()
    return f"AIS-{raw[:4]}-{raw[4:8]}-{h}"


def register_new_code() -> str:
    for _ in range(10):
        code = generate_unique_code()
        if code not in st.session_state.premium_codes:
            st.session_state.premium_codes[code] = {"used": False, "activated_by": None}
            return code
    raise RuntimeError("Code generation failed")


def verify_and_activate(code: str, user_id: str) -> dict:
    code = code.strip().upper()
    if not code:
        return {"ok": False, "message": "Please enter a code."}
    if code not in st.session_state.premium_codes:
        return {"ok": False, "message": "Invalid code. Purchase a license at Gumroad."}

    entry = st.session_state.premium_codes[code]

    if entry["used"]:
        if entry["activated_by"] == user_id:
            return {"ok": True, "message": "Premium restored!", "code": code}
        return {"ok": False, "message": "This code has already been used. Codes are non-transferable."}

    st.session_state.premium_codes[code] = {"used": True, "activated_by": user_id}
    return {"ok": True, "message": "Premium unlocked!", "code": code}


def can_generate() -> bool:
    return st.session_state.is_premium or st.session_state.free_uses < FREE_LIMIT


def build_final_prompt(prompt: str, style: str, aspect: str) -> str:
    style_text = STYLE_HINTS.get(style, "")
    aspect_text = f"Aspect ratio {aspect}."
    return f"{prompt}. {style_text}. {aspect_text}"


def generate_image_hf(prompt: str, style: str, aspect: str, model_label: str) -> dict:
    final_prompt = build_final_prompt(prompt, style, aspect)
    model_id = MODEL_OPTIONS[model_label]

    if not HF_TOKEN:
        return {
            "ok": False,
            "error": "HF_TOKEN is missing in Streamlit secrets."
        }

    try:
        client = InferenceClient(
            provider="hf-inference",
            api_key=HF_TOKEN,
        )

        image = client.text_to_image(
            final_prompt,
            model=model_id
        )

        return {
            "ok": True,
            "image": image,
            "prompt_used": final_prompt,
            "style": style,
            "aspect": aspect,
            "timestamp": datetime.datetime.now().strftime("%H:%M · %b %d"),
            "model": model_label,
        }

    except Exception as e:
        return {"ok": False, "error": str(e)}

# ─────────────────────────────────────────────
# UI
# ─────────────────────────────────────────────
user_id = get_user_id()

st.markdown("""
<div class="hero">
  <div class="hero-badge">✦ Powered by Hugging Face</div>
  <h1>AI Image Studio</h1>
  <p>Transform your ideas into stunning visuals — instantly.</p>
</div>
""", unsafe_allow_html=True)

tier_label = "✦ PREMIUM" if st.session_state.is_premium else "FREE"
uses_left = "∞" if st.session_state.is_premium else str(max(0, FREE_LIMIT - st.session_state.free_uses))

st.markdown(f"""
<div class="stat-strip">
  <div class="stat-item">
    <div class="stat-num">{uses_left}</div>
    <div class="stat-label">Generations left</div>
  </div>
  <div class="stat-item">
    <div class="stat-num">{len(st.session_state.generated_images)}</div>
    <div class="stat-label">Images created</div>
  </div>
  <div class="stat-item">
    <div class="stat-num">{tier_label}</div>
    <div class="stat-label">Current plan</div>
  </div>
</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([1.1, 0.9], gap="large")

with col_left:
    st.markdown('<div class="card"><div class="card-title">🎨 Image Generator</div>', unsafe_allow_html=True)

    prompt = st.text_area(
        "Describe your image",
        placeholder="e.g. A neon-lit Tokyo alley at midnight, rain-soaked cobblestones reflecting pink signage, cinematic...",
        height=110,
        label_visibility="collapsed",
    )

    c1, c2 = st.columns(2)
    with c1:
        style = st.selectbox("Style", list(STYLE_HINTS.keys()))
    with c2:
        aspect = st.selectbox("Aspect Ratio", [
            "1:1 Square", "16:9 Landscape", "9:16 Portrait", "4:3 Classic", "3:2 Photo"
        ])

    if st.session_state.is_premium:
        model_label = st.selectbox("Model", list(MODEL_OPTIONS.keys()))
    else:
        model_label = "Premium XL"
        st.caption("Free mode uses Premium XL model.")

    if not st.session_state.is_premium:
        pct = int((st.session_state.free_uses / FREE_LIMIT) * 100)
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;font-size:0.78rem;color:var(--muted);margin-top:0.8rem;">
          <span>Free usage</span><span>{st.session_state.free_uses}/{FREE_LIMIT}</span>
        </div>
        <div class="limit-bar-bg">
          <div class="limit-bar-fill" style="width:{pct}%"></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    generate_btn = st.button("✦ Generate Image", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if generate_btn:
        if not prompt.strip():
            st.warning("Please enter a prompt first.")
        elif not can_generate():
            st.error("🔒 Free limit reached. Unlock Premium below to continue.")
            st.session_state.show_unlock = True
        else:
            with st.spinner("Crafting your image…"):
                result = generate_image_hf(prompt, style, aspect, model_label)

            if result.get("ok"):
                if not st.session_state.is_premium:
                    st.session_state.free_uses += 1
                st.session_state.generated_images.insert(0, result)
                st.success("Image generated successfully!")
                st.rerun()
            else:
                st.error(f"Generation failed: {result.get('error', 'unknown error')}")

    if st.session_state.generated_images:
        latest = st.session_state.generated_images[0]
        st.markdown('<div class="card"><div class="card-title">🖼 Latest Output</div>', unsafe_allow_html=True)

        st.image(latest["image"], use_container_width=True)

        buffer = io.BytesIO()
        latest["image"].save(buffer, format="PNG")
        st.download_button(
            label="Download PNG",
            data=buffer.getvalue(),
            file_name="ai-image-studio.png",
            mime="image/png",
            use_container_width=True,
        )

        st.markdown(f"""
        <div style="margin-top:0.8rem;font-size:0.82rem;color:var(--muted);line-height:1.7;">
          <strong style="color:var(--gold);">Prompt Used:</strong><br>
          <span style="color:var(--text);">{latest.get('prompt_used','')[:300]}</span><br><br>
          <strong style="color:var(--gold);">Style:</strong> {latest.get('style','')} &nbsp;·&nbsp;
          <strong style="color:var(--gold);">Ratio:</strong> {latest.get('aspect','')} &nbsp;·&nbsp;
          <strong style="color:var(--gold);">Model:</strong> {latest.get('model','')} &nbsp;·&nbsp;
          {latest.get('timestamp','')}
        </div>
        </div>
        """, unsafe_allow_html=True)

    if len(st.session_state.generated_images) > 1:
        with st.expander(f"📂 History ({len(st.session_state.generated_images)} images)"):
            for i, img in enumerate(st.session_state.generated_images[1:], 1):
                n = len(st.session_state.generated_images) - i
                st.markdown(f"""
                <div style="border-bottom:1px solid var(--border);padding:0.6rem 0;font-size:0.82rem;color:var(--muted);">
                  <strong style="color:var(--text);">#{n}</strong> &nbsp;
                  {img.get('style','')} · {img.get('aspect','')} · {img.get('model','')} · {img.get('timestamp','')}
                </div>
                """, unsafe_allow_html=True)

with col_right:
    if st.session_state.is_premium:
        st.markdown(f"""
        <div class="card" style="border-color:var(--gold);background:linear-gradient(135deg,#1a1508,#13131c);">
          <div class="card-title">Account Status</div>
          <div class="premium-badge">✦ PREMIUM ACTIVE</div>
          <p style="margin-top:0.9rem;font-size:0.88rem;color:var(--muted);">
            Unlimited generations · All styles unlocked<br>
            Code: <code style="color:var(--gold);">{st.session_state.activated_code}</code>
          </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="card">
          <div class="card-title">Account Status</div>
          <div class="free-badge">FREE — {st.session_state.free_uses}/{FREE_LIMIT} used</div>
          <p style="margin-top:0.9rem;font-size:0.88rem;color:var(--muted);">
            Upgrade to Premium for unlimited<br>image generation and all styles.
          </p>
        </div>
        """, unsafe_allow_html=True)

    if not st.session_state.is_premium:
        st.markdown('<div class="card"><div class="card-title">🔓 Unlock Premium</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <a href="{GUMROAD_URL}" target="_blank" class="gumroad-btn">
          ✦ Buy Premium on Gumroad →
        </a>
        <p style="text-align:center;font-size:0.78rem;color:var(--muted);margin:0.4rem 0 1.2rem;">
          You'll receive a unique activation code by email.
        </p>
        """, unsafe_allow_html=True)

        code_input = st.text_input(
            "Activation code",
            placeholder="AIS-XXXX-XXXX-XXXXXX",
            label_visibility="collapsed",
        )
        activate_btn = st.button("Activate Code", use_container_width=True)

        if activate_btn:
            res = verify_and_activate(code_input, user_id)
            if res["ok"]:
                st.session_state.is_premium = True
                st.session_state.activated_code = res["code"]
                st.session_state.show_unlock = False
                st.success(f"🎉 {res['message']}")
                st.rerun()
            else:
                st.error(res["message"])

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
      <div class="card-title">✦ Premium Features</div>
      <div style="display:flex;flex-direction:column;gap:0.65rem;font-size:0.88rem;">
        <div>✅ &nbsp;<strong>Unlimited</strong> image generations</div>
        <div>✅ &nbsp;All <strong>10 art styles</strong></div>
        <div>✅ &nbsp;All <strong>aspect ratios</strong></div>
        <div>✅ &nbsp;<strong>Multiple model</strong> options</div>
        <div>✅ &nbsp;Full <strong>generation history</strong></div>
        <div>✅ &nbsp;<strong>Priority</strong> processing</div>
        <div>✅ &nbsp;<strong>No ads</strong> — ever</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("⚙️ Admin — Generate Premium Codes"):
        st.caption("Generate codes to send to Gumroad buyers. Each code is single-use and non-transferable.")
        num = st.number_input("Number of codes", min_value=1, max_value=50, value=1, step=1)
        if st.button("Generate Codes"):
            new_codes = []
            for _ in range(int(num)):
                c = register_new_code()
                new_codes.append(c)
            st.success(f"✅ Generated {len(new_codes)} code(s):")
            for c in new_codes:
                st.code(c)

        total = len(st.session_state.premium_codes)
        used = sum(1 for v in st.session_state.premium_codes.values() if v["used"])
        st.caption(f"Pool: {total} total · {used} used · {total - used} available")

st.markdown(f"""
<div style="text-align:center;padding:2.5rem 0 1rem;color:var(--muted);font-size:0.78rem;
            border-top:1px solid var(--border);margin-top:2rem;">
  AI Image Studio &nbsp;·&nbsp; Powered by Hugging Face &nbsp;·&nbsp;
  <a href="{GUMROAD_URL}" target="_blank" style="color:var(--gold);text-decoration:none;">
    Get Premium →
  </a>
</div>
""", unsafe_allow_html=True)
