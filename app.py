import streamlit as st
import requests
from PIL import Image
import io
import datetime

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
APP_NAME = "AI Image Studio"
APP_TAGLINE = "Create stunning AI images for social media, ads, thumbnails, and creative projects."
FREE_DAILY_LIMIT = 1
PREMIUM_LINK = "https://aiimagestudio.gumroad.com/l/yrpblj"
PREMIUM_CODE = "AISTUDIO2026"

HF_TOKEN = st.secrets.get("HF_TOKEN", "")

# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------
st.set_page_config(
    page_title=APP_NAME,
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)
from huggingface_hub import InferenceClient
import streamlit as st
from PIL import Image

HF_TOKEN = st.secrets.get("HF_TOKEN", "")

def generate_image(prompt: str):
    if not HF_TOKEN:
        return {"ok": False, "error": "HF_TOKEN is missing in Streamlit Secrets."}

    try:
        client = InferenceClient(
            provider="hf-inference",
            api_key=HF_TOKEN,
        )

        image = client.text_to_image(
            prompt,
            model="black-forest-labs/FLUX.1-Krea-dev"
        )

        return {"ok": True, "image": image}

    except Exception as e:
        return {"ok": False, "error": str(e)}
# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
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

# --------------------------------------------------
# STYLING
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500;700&display=swap');

:root {
    --gold: #e8c97a;
    --gold-dark: #c9973a;
    --bg: #0a0a0f;
    --card: #13131c;
    --border: rgba(232,201,122,0.16);
    --text: #f4efe1;
    --muted: #a6a08f;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background: var(--bg);
    color: var(--text);
}

.stApp {
    background: linear-gradient(180deg, #09090d 0%, #101019 100%);
}

.block-container {
    max-width: 1150px;
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

.hero {
    text-align: center;
    padding: 3rem 1rem 2rem 1rem;
    margin-bottom: 1rem;
}

.hero-badge {
    display: inline-block;
    padding: 0.35rem 1rem;
    border-radius: 999px;
    border: 1px solid var(--gold);
    color: var(--gold);
    background: rgba(232,201,122,0.08);
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.5rem, 5vw, 4.2rem);
    font-weight: 800;
    line-height: 1.05;
    margin: 0;
    background: linear-gradient(135deg, #f7e7b3 0%, #e8c97a 45%, #bf8630 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    color: var(--muted);
    font-size: 1.03rem;
    max-width: 760px;
    margin: 0.9rem auto 0 auto;
    line-height: 1.8;
}

.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 1.35rem;
    margin-bottom: 1rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.22);
}

.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.82rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 0.8rem;
}

.stat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 1rem;
}

.stat-box {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1rem;
    text-align: center;
}

.stat-number {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: var(--gold);
}

.stat-label {
    font-size: 0.78rem;
    color: var(--muted);
    margin-top: 0.3rem;
}

.feature-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1rem;
    height: 100%;
}

.feature-head {
    font-family: 'Syne', sans-serif;
    color: var(--gold);
    font-size: 0.95rem;
    margin-bottom: 0.45rem;
}

.feature-text {
    color: var(--muted);
    font-size: 0.92rem;
    line-height: 1.65;
}

.price-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1rem;
}

.price-box.premium {
    border: 1px solid rgba(232,201,122,0.35);
    box-shadow: 0 0 0 1px rgba(232,201,122,0.08) inset;
}

.price-name {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    color: var(--gold);
}

.price-value {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    margin: 0.35rem 0 0.8rem 0;
}

.note-box {
    border-radius: 14px;
    padding: 1rem;
    margin-bottom: 1rem;
    border: 1px solid var(--border);
    background: rgba(255,255,255,0.03);
    color: var(--text);
}

.note-warning {
    background: rgba(120, 35, 35, 0.18);
    border: 1px solid rgba(255, 120, 120, 0.22);
    color: #ffd2d2;
}

.note-success {
    background: rgba(35, 120, 60, 0.18);
    border: 1px solid rgba(120, 255, 170, 0.18);
    color: #d7ffe6;
}

.output-box {
    background: #0b0b12;
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1rem;
}

.footer {
    text-align: center;
    color: var(--muted);
    font-size: 0.82rem;
    padding-top: 1.4rem;
}

.stTextInput input,
.stTextArea textarea,
.stSelectbox > div > div {
    background: #171722 !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}

.stButton > button {
    background: linear-gradient(135deg, var(--gold), var(--gold-dark)) !important;
    color: #111 !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
}

@media (max-width: 900px) {
    .stat-grid {
        grid-template-columns: 1fr;
    }
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HELPERS
# --------------------------------------------------
def build_prompt(prompt: str, style: str, aspect: str) -> str:
    style_map = {
        "Photorealistic": "ultra realistic, natural lighting, detailed textures, premium photography",
        "Cinematic": "cinematic lighting, dramatic shadows, film still, moody atmosphere",
        "Anime": "anime style, vibrant colors, crisp lines, expressive composition",
        "Fantasy": "fantasy art, dreamy atmosphere, magical details, epic composition",
        "Minimal": "minimalist, clean composition, elegant design, balanced framing",
    }
    return f"{prompt}, {style_map.get(style, '')}, aspect ratio {aspect}"

def generate_image(prompt: str, style: str, aspect: str) -> dict:
    final_prompt = build_prompt(prompt, style, aspect)

    if not HF_TOKEN:
        return {"ok": False, "error": "HF_TOKEN is missing in Streamlit Secrets."}

    api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}

    try:
        response = requests.post(
            api_url,
            headers=headers,
            json={"inputs": final_prompt},
            timeout=120,
        )

        if response.status_code == 200:
            image = Image.open(io.BytesIO(response.content))
            return {
                "ok": True,
                "image": image,
                "prompt_used": final_prompt,
                "style": style,
                "aspect": aspect,
                "time": datetime.datetime.now().strftime("%H:%M · %b %d"),
            }

        if response.status_code == 503:
            return {"ok": False, "error": "Model is loading. Wait 20–30 seconds and try again."}

        if response.status_code == 401:
            return {"ok": False, "error": "Invalid HF_TOKEN in Streamlit Secrets."}

        return {"ok": False, "error": f"API error {response.status_code}"}

    except requests.exceptions.Timeout:
        return {"ok": False, "error": "Request timed out. Try again."}
    except Exception as e:
        return {"ok": False, "error": str(e)}

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.markdown("## 💎 Premium Access")
    st.link_button("Buy Premium on Gumroad", "https://aiimagestudio.gumroad.com/l/yrpblj")

    code_input = st.text_input("Enter Premium Code", type="password")

    if st.button("Unlock Premium"):
        if code_input.strip() == PREMIUM_CODE:
            st.session_state.premium_unlocked = True
            st.success("Premium unlocked successfully.")
        else:
            st.error("Invalid premium code.")

    st.markdown("---")

    if st.session_state.premium_unlocked:
        st.success("Premium mode active")
        remaining_text = "Unlimited"
    else:
        remaining = max(FREE_DAILY_LIMIT - st.session_state.usage_count, 0)
        remaining_text = str(remaining)
        st.info(f"Free images left today: {remaining}")

    st.markdown("### Recent Prompts")
    if st.session_state.history:
        for item in st.session_state.history[:5]:
            st.caption(item)
    else:
        st.caption("No prompts yet")

# --------------------------------------------------
# HERO
# --------------------------------------------------
st.markdown("""
<div class="hero">
  <div class="hero-badge">✦ Powered by Hugging Face</div>
  <div class="hero-title">AI Image Studio</div>
  <div class="hero-sub">
    Create stunning AI images instantly for social media, ads, thumbnails, product promos, and creative projects.
  </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# STATS
# --------------------------------------------------
created_count = len(st.session_state.history)
plan_name = "Premium" if st.session_state.premium_unlocked else "Free"
uses_left = "∞" if st.session_state.premium_unlocked else max(FREE_DAILY_LIMIT - st.session_state.usage_count, 0)

st.markdown(f"""
<div class="stat-grid">
  <div class="stat-box">
    <div class="stat-number">{uses_left}</div>
    <div class="stat-label">Images Left</div>
  </div>
  <div class="stat-box">
    <div class="stat-number">{created_count}</div>
    <div class="stat-label">Images Created</div>
  </div>
  <div class="stat-box">
    <div class="stat-number">{plan_name}</div>
    <div class="stat-label">Current Plan</div>
  </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# FEATURES
# --------------------------------------------------
st.markdown('<div class="card"><div class="card-title">Powerful Features</div></div>', unsafe_allow_html=True)

f1, f2, f3 = st.columns(3)
with f1:
    st.markdown("""
    <div class="feature-box">
      <div class="feature-head">Smart Generation</div>
      <div class="feature-text">Turn simple prompts into polished visuals for posts, ads, thumbnails, and creative designs.</div>
    </div>
    """, unsafe_allow_html=True)
with f2:
    st.markdown("""
    <div class="feature-box">
      <div class="feature-head">Luxury Design</div>
      <div class="feature-text">A premium interface that feels elegant, modern, and creator-friendly on desktop and mobile.</div>
    </div>
    """, unsafe_allow_html=True)
with f3:
    st.markdown("""
    <div class="feature-box">
      <div class="feature-head">Premium Upgrade</div>
      <div class="feature-text">Start free, then unlock unlimited access for regular content creation and commercial use.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --------------------------------------------------
# ABOUT + PRICING
# --------------------------------------------------
left_info, right_info = st.columns([1.2, 1])

with left_info:
    st.markdown("""
    <div class="card">
      <div class="card-title">About AI Image Studio</div>
      <div style="color:var(--muted);line-height:1.8;font-size:0.95rem;">
        AI Image Studio is built for creators, students, marketers, and business owners who want
        fast, high-quality visuals without complicated workflows. It helps transform simple ideas
        into beautiful AI-generated images for real-world use.
      </div>
    </div>
    """, unsafe_allow_html=True)

with right_info:
    st.markdown("""
    <div class="card">
      <div class="card-title">Pricing</div>
      <div class="price-box">
        <div class="price-name">Free</div>
        <div class="price-value">$0</div>
        <div style="color:var(--muted);line-height:1.8;">
          • 1 image per day<br>
          • Standard model access<br>
          • Instant image download
        </div>
      </div>
      <br>
      <div class="price-box premium">
        <div class="price-name">Premium</div>
        <div class="price-value">Code Access</div>
        <div style="color:var(--muted);line-height:1.8;">
          • Unlimited images<br>
          • Premium access<br>
          • Better creator workflow
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# STATUS
# --------------------------------------------------
if st.session_state.premium_unlocked:
    st.markdown('<div class="note-box note-success">💎 Premium unlocked — unlimited access is active in this session.</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="note-box note-warning">🔒 Free plan allows only 1 image per day. Upgrade to Premium for unlimited generation.</div>', unsafe_allow_html=True)

# --------------------------------------------------
# GENERATOR
# --------------------------------------------------
st.markdown('<div class="card"><div class="card-title">Generate Image</div></div>', unsafe_allow_html=True)

col_a, col_b = st.columns([1.2, 0.8])

with col_a:
    prompt = st.text_area(
        "Describe your image",
        placeholder="Example: A luxury perfume bottle on marble with dramatic studio lighting and premium product photography style",
        height=130,
    )
    negative_prompt = st.text_area(
        "Negative prompt (optional)",
        placeholder="blurry, watermark, low quality, distorted face",
        height=80,
    )

with col_b:
    style = st.selectbox("Style", ["Photorealistic", "Cinematic", "Anime", "Fantasy", "Minimal"])
    aspect = st.selectbox("Aspect Ratio", ["1:1", "16:9", "9:16", "4:3", "3:2"])

if st.button("✦ Generate Image", use_container_width=True):
    if not prompt.strip():
        st.warning("Please enter a prompt first.")
    elif (not st.session_state.premium_unlocked) and st.session_state.usage_count >= FREE_DAILY_LIMIT:
        st.error("Free limit reached.")
        st.link_button("Upgrade to Premium", "https://aiimagestudio.gumroad.com/l/yrpblj")
    else:
        with st.spinner("Generating your image..."):
            result = generate_image(prompt, style, aspect)

        if result["ok"]:
            if not st.session_state.premium_unlocked:
                st.session_state.usage_count += 1

            st.session_state.history.insert(0, prompt)

            st.markdown('<div class="card"><div class="card-title">Latest Output</div>', unsafe_allow_html=True)
            st.markdown('<div class="output-box">', unsafe_allow_html=True)
            st.image(result["image"], use_container_width=True)

            buffer = io.BytesIO()
            result["image"].save(buffer, format="PNG")
            st.download_button(
                "Download Image",
                buffer.getvalue(),
                file_name="ai-image-studio.png",
                mime="image/png",
                use_container_width=True,
            )

            st.markdown(f"""
            <div style="margin-top:0.9rem;color:var(--muted);font-size:0.88rem;line-height:1.7;">
                <strong style="color:var(--gold);">Prompt Used:</strong> {result["prompt_used"]}<br>
                <strong style="color:var(--gold);">Style:</strong> {result["style"]} &nbsp;·&nbsp;
                <strong style="color:var(--gold);">Ratio:</strong> {result["aspect"]} &nbsp;·&nbsp;
                {result["time"]}
            </div>
            """, unsafe_allow_html=True)

            st.markdown('</div></div>', unsafe_allow_html=True)
        else:
            st.error(result["error"])

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("""
<div class="footer">
  AI Image Studio · Powered by Hugging Face · Premium available on Gumroad
</div>
""", unsafe_allow_html=True)
