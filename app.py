import streamlit as st
import requests
from PIL import Image
import io
from datetime import datetime

# =========================================================
# APP CONFIG — EDIT THESE
# =========================================================
APP_NAME = "AI Image Studio"
APP_TAGLINE = "Create stunning AI images in seconds for social media, ads, and creative projects."
PREMIUM_LINK = "https://your-payment-link.com"  # Replace later
FREE_DAILY_LIMIT = 3

# Hugging Face token from Streamlit Secrets
# Add in Streamlit Secrets:
# HF_TOKEN = "hf_your_token_here"
HF_TOKEN = st.secrets.get("HF_TOKEN", "")

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title=APP_NAME,
    page_icon="🎨",
    layout="wide",
)

# =========================================================
# SESSION STATE
# =========================================================
if "generation_count" not in st.session_state:
    st.session_state.generation_count = 0

if "history" not in st.session_state:
    st.session_state.history = []

# =========================================================
# MODELS AND PRESETS
# =========================================================
MODELS = {
    "Stable Diffusion XL - Fast and detailed": "stabilityai/stable-diffusion-xl-base-1.0",
    "FLUX.1-schnell - Ultra fast": "black-forest-labs/FLUX.1-schnell",
    "Dreamlike Photoreal - Realistic photos": "dreamlike-art/dreamlike-photoreal-2.0",
}

PROMPT_PRESETS = {
    "None": "",
    "Cinematic City": "A futuristic city street at night, neon reflections, rainy atmosphere, cinematic lighting, ultra detailed, 8k",
    "Fantasy Forest": "A magical forest with glowing mushrooms, floating lights, fantasy art, dreamy, highly detailed",
    "Luxury Product": "Luxury perfume bottle on marble surface, premium ad photography, soft shadows, realistic",
    "Fashion Portrait": "Elegant woman in studio lighting, high fashion photography, realistic, detailed face",
    "Village Sunrise": "A peaceful mountain village at sunrise, soft golden light, cinematic atmosphere, realistic, ultra detailed",
    "Anime Scene": "A beautiful anime-style scene with cherry blossoms, soft lighting, vibrant colors, dreamy composition",
}

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(180deg, #080911 0%, #0f172a 100%);
    color: #f8fafc;
}

.stApp {
    background: linear-gradient(180deg, #080911 0%, #0f172a 100%);
}

h1, h2, h3, h4 {
    font-family: 'Syne', sans-serif !important;
    color: #ffffff !important;
}

.block-container {
    max-width: 1250px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

.hero {
    padding: 2.5rem 2rem;
    border-radius: 28px;
    background:
        radial-gradient(circle at top left, rgba(124,58,237,0.28), transparent 35%),
        radial-gradient(circle at top right, rgba(59,130,246,0.25), transparent 32%),
        linear-gradient(135deg, rgba(15,23,42,0.96), rgba(17,24,39,0.93));
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 15px 50px rgba(0,0,0,0.28);
    margin-bottom: 1rem;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 800;
    line-height: 1.02;
    margin-bottom: 0.6rem;
    background: linear-gradient(135deg, #f3e8ff, #bfdbfe, #7dd3fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    color: #cbd5e1;
    font-size: 1.05rem;
    max-width: 760px;
    line-height: 1.7;
}

.badges {
    margin-top: 1rem;
}

.badge {
    display: inline-block;
    padding: 0.45rem 0.85rem;
    margin: 0.25rem 0.35rem 0 0;
    border-radius: 999px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    color: #dbeafe;
    font-size: 0.84rem;
}

.section-card {
    background: rgba(15,23,42,0.88);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 1.2rem;
    box-shadow: 0 12px 35px rgba(0,0,0,0.18);
    margin-bottom: 1rem;
}

.section-title {
    font-size: 1.5rem;
    font-weight: 800;
    margin-bottom: 0.35rem;
}

.section-sub {
    color: #94a3b8;
    font-size: 0.96rem;
    margin-bottom: 1rem;
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
}

.feature-card {
    background: rgba(30,41,59,0.72);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 1rem;
}

.feature-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    margin-bottom: 0.4rem;
}

.feature-text {
    color: #cbd5e1;
    font-size: 0.92rem;
    line-height: 1.6;
}

.about-box {
    background: rgba(30,41,59,0.60);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 1rem;
    color: #cbd5e1;
    line-height: 1.75;
}

.price-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}

.price-card {
    background: rgba(15,23,42,0.95);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 1.2rem;
}

.price-card.premium {
    border: 1px solid rgba(168,85,247,0.45);
    box-shadow: 0 12px 30px rgba(124,58,237,0.16);
}

.price-name {
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
}

.price-amount {
    font-size: 2rem;
    font-weight: 800;
    margin: 0.35rem 0 0.8rem 0;
}

.price-list {
    color: #dbeafe;
    line-height: 1.9;
    font-size: 0.95rem;
}

.info-box {
    background: rgba(30,41,59,0.65);
    border: 1px solid rgba(129,140,248,0.25);
    border-left: 4px solid #818cf8;
    border-radius: 14px;
    padding: 1rem;
    color: #dbeafe;
    font-size: 0.92rem;
    margin-top: 0.8rem;
}

.success-box {
    background: rgba(20,35,28,0.82);
    border: 1px solid rgba(74,222,128,0.25);
    border-left: 4px solid #4ade80;
    border-radius: 14px;
    padding: 1rem;
    color: #bbf7d0;
    font-size: 0.92rem;
    margin-top: 0.8rem;
}

.prompt-box {
    background: rgba(15,23,42,0.7);
    border: 1px dashed rgba(255,255,255,0.12);
    border-radius: 14px;
    padding: 0.9rem 1rem;
    color: #cbd5e1;
    font-size: 0.92rem;
    margin-top: 0.8rem;
}

.history-card {
    background: rgba(30,41,59,0.55);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 0.85rem;
    margin-bottom: 0.7rem;
    color: #dbeafe;
}

.stTextArea textarea,
.stTextInput input {
    background: #0f172a !important;
    color: #f8fafc !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
}

.stSelectbox > div > div {
    background: #0f172a !important;
    color: #f8fafc !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
}

div.stButton > button,
a[data-testid="stLinkButton"] {
    width: 100%;
    border-radius: 14px !important;
    font-weight: 700 !important;
}

div.stButton > button {
    border: none;
    padding: 0.85rem 1rem;
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    color: white;
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    box-shadow: 0 10px 25px rgba(59,130,246,0.22);
}

.footer {
    text-align: center;
    color: #64748b;
    font-size: 0.85rem;
    padding: 1rem 0 0.5rem 0;
}

@media (max-width: 900px) {
    .feature-grid { grid-template-columns: 1fr; }
    .price-grid { grid-template-columns: 1fr; }
    .hero-title { font-size: 2.5rem; }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.title("🎛️ Studio Panel")
    st.caption("AI image generation for creators and businesses")

    free_left = max(FREE_DAILY_LIMIT - st.session_state.generation_count, 0)
    st.markdown(f"**Free images left:** {free_left}")

    preset_choice = st.selectbox("Quick prompt preset", list(PROMPT_PRESETS.keys()))

    st.markdown("---")
    st.subheader("Upgrade")
    st.write("Unlock more power and premium features.")
    st.link_button("💎 Buy Premium", PREMIUM_LINK)

    st.markdown("---")
    st.subheader("Recent prompts")
    if st.session_state.history:
        for item in st.session_state.history[:5]:
            st.caption(item["time"])
            st.write(item["prompt"][:70] + ("..." if len(item["prompt"]) > 70 else ""))
            st.markdown("---")
    else:
        st.caption("No prompts yet.")

# =========================================================
# HERO
# =========================================================
st.markdown(f"""
<div class="hero">
    <div class="hero-title">{APP_NAME}</div>
    <div class="hero-sub">
        {APP_TAGLINE}
    </div>
    <div class="badges">
        <span class="badge">🎨 AI Art Generator</span>
        <span class="badge">⚡ Fast Results</span>
        <span class="badge">📱 Social Media Ready</span>
        <span class="badge">⬇️ Instant Download</span>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# FEATURES
# =========================================================
st.markdown("""
<div class="section-card">
    <div class="section-title">Powerful features</div>
    <div class="section-sub">Everything users need in a modern AI image generation website.</div>
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-title">Smart text-to-image</div>
            <div class="feature-text">Turn simple words into cinematic scenes, portraits, product shots, and creative visuals.</div>
        </div>
        <div class="feature-card">
            <div class="feature-title">Fast and easy workflow</div>
            <div class="feature-text">Generate high-quality images quickly with a clean and simple interface designed for everyone.</div>
        </div>
        <div class="feature-card">
            <div class="feature-title">Business-ready layout</div>
            <div class="feature-text">Use it as a public AI tool, creator platform, or startup-style website for monetization.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# ABOUT + PRICING
# =========================================================
col_about, col_pricing = st.columns([1.2, 1])

with col_about:
    st.markdown("""
    <div class="section-card">
        <div class="section-title">About us</div>
        <div class="section-sub">A polished AI product page for your visitors.</div>
        <div class="about-box">
            <b>AI Image Studio</b> helps people create beautiful AI-generated images quickly and easily.
            This platform is designed for creators, students, marketers, business owners, and anyone
            who needs high-quality visuals without a complicated workflow.
            <br><br>
            Our goal is to make AI image generation simple, attractive, and useful for everyday creative work.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_pricing:
    st.markdown("""
    <div class="section-card">
        <div class="section-title">Pricing plans</div>
        <div class="section-sub">Simple monetization display.</div>
        <div class="price-grid">
            <div class="price-card">
                <div class="price-name">Free</div>
                <div class="price-amount">$0</div>
                <div class="price-list">
                    • Limited daily images<br>
                    • Standard generation<br>
                    • Basic model access<br>
                    • Instant download
                </div>
            </div>
            <div class="price-card premium">
                <div class="price-name">Premium</div>
                <div class="price-amount">$9/mo</div>
                <div class="price-list">
                    • More daily images<br>
                    • Better models<br>
                    • Faster workflow<br>
                    • Premium features
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# GENERATOR
# =========================================================
st.markdown("""
<div class="section-card">
    <div class="section-title">AI image generator</div>
    <div class="section-sub">Create images directly from your website.</div>
</div>
""", unsafe_allow_html=True)

default_prompt = PROMPT_PRESETS[preset_choice] if preset_choice != "None" else ""

left, right = st.columns([1.15, 0.85])

with left:
    prompt = st.text_area(
        "Prompt",
        value=default_prompt,
        placeholder="Example: A luxury perfume bottle on a marble table, premium ad photography, soft shadows, realistic, ultra detailed",
        height=150,
    )

    negative_prompt = st.text_area(
        "Negative prompt",
        placeholder="Optional: blurry, watermark, extra fingers, distorted face, low quality, text",
        height=90,
    )

    with st.expander("Sample prompt ideas"):
        st.write("**Product ad:** Luxury skincare bottle, studio light, premium ad photography, realistic")
        st.write("**Portrait:** Elegant woman in soft studio lighting, fashion magazine style, detailed face")
        st.write("**Fantasy:** Magical forest with glowing flowers, dreamy atmosphere, epic fantasy art")
        st.write("**Thumbnail:** Cyberpunk city skyline, dramatic lighting, vibrant neon colors")

with right:
    model_label = st.selectbox("Model", list(MODELS.keys()))
    model_id = MODELS[model_label]

    style_choice = st.selectbox(
        "Style direction",
        ["Realistic", "Cinematic", "Fantasy", "Anime", "Product Photography", "Minimal"]
    )

    st.markdown("""
    <div class="info-box">
        <b>Free mode:</b> visitors can generate a limited number of images each day.
        Upgrade users can be redirected to your premium page.
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="prompt-box">
        <b>Selected model:</b> {model_label}<br>
        <b>Style:</b> {style_choice}
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# GENERATE LOGIC
# =========================================================
generate = st.button("🎨 Generate Image")

if generate:
    if not HF_TOKEN:
        st.error("HF_TOKEN is missing. Add it in Streamlit Secrets.")
    elif not prompt.strip():
        st.error("Please enter a prompt.")
    elif st.session_state.generation_count >= FREE_DAILY_LIMIT:
        st.warning("Free limit reached. Please upgrade to Premium.")
        st.link_button("💎 Upgrade to Premium", PREMIUM_LINK)
    else:
        final_prompt = f"{prompt}, {style_choice.lower()} style"

        api_url = f"https://api-inference.huggingface.co/models/{model_id}"
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        payload = {
            "inputs": final_prompt,
            "parameters": {
                "negative_prompt": negative_prompt or "",
                "guidance_scale": 7.5,
                "num_inference_steps": 20,
            }
        }

        with st.spinner("Generating your image..."):
            try:
                response = requests.post(api_url, headers=headers, json=payload, timeout=120)

                if response.status_code == 200:
                    image = Image.open(io.BytesIO(response.content))
                    st.image(image, use_container_width=True)

                    buf = io.BytesIO()
                    image.save(buf, format="PNG")

                    st.download_button(
                        label="⬇️ Download image",
                        data=buf.getvalue(),
                        file_name="ai-image-studio.png",
                        mime="image/png",
                    )

                    st.session_state.generation_count += 1
                    st.session_state.history.insert(0, {
                        "time": datetime.now().strftime("%d %b %Y • %I:%M %p"),
                        "prompt": final_prompt
                    })

                    st.markdown("""
                    <div class="success-box">
                        <b>Success:</b> Your image was generated successfully.
                    </div>
                    """, unsafe_allow_html=True)

                elif response.status_code == 503:
                    st.warning("The model is loading. Wait 20–30 seconds and try again.")
                elif response.status_code == 401:
                    st.error("Invalid HF token in Streamlit Secrets.")
                else:
                    st.error(f"API Error {response.status_code}: {response.text[:300]}")

            except requests.exceptions.Timeout:
                st.error("Request timed out. Please try again.")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

# =========================================================
# HISTORY
# =========================================================
st.markdown("""
<div class="section-card">
    <div class="section-title">Recent generations</div>
    <div class="section-sub">Generated prompts will appear here.</div>
</div>
""", unsafe_allow_html=True)

if st.session_state.history:
    for item in st.session_state.history[:4]:
        st.markdown(
            f'<div class="history-card"><b>{item["time"]}</b><br>{item["prompt"]}</div>',
            unsafe_allow_html=True
        )
else:
    st.markdown('<div class="prompt-box">No generated history yet.</div>', unsafe_allow_html=True)

# =========================================================
# CTA
# =========================================================
cta1, cta2 = st.columns(2)

with cta1:
    st.link_button("💎 Upgrade to Premium", PREMIUM_LINK)

with cta2:
    st.button("🚀 Start Creating")

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div class="footer">
    © 2026 AI Image Studio - Professional AI image generation platform
</div>
""", unsafe_allow_html=True)
