import streamlit as st
import requests
from PIL import Image
import io
from datetime import datetime

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Image Studio",
    page_icon="🎨",
    layout="centered",
)

# ── Session state ────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ── Prompt presets ───────────────────────────────────────────────────────────
PROMPT_PRESETS = {
    "None": "",
    "Cinematic City": "A futuristic city street at night, neon reflections, rainy atmosphere, cinematic lighting, ultra detailed, 8k",
    "Fantasy Forest": "A magical forest with glowing mushrooms, floating lights, fantasy art, dreamy, highly detailed",
    "Luxury Product": "Luxury perfume bottle on a marble surface, soft shadows, premium ad photography, elegant composition, realistic",
    "Fashion Portrait": "Elegant woman in royal blue dress, studio lighting, high fashion photography, detailed face, realistic skin texture",
    "Village Sunrise": "A dreamy mountain village at sunrise, soft golden light, cinematic atmosphere, ultra detailed, realistic, 8k",
}

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background: linear-gradient(180deg, #08080d 0%, #0d1020 100%);
    color: #f3f4f6;
}

.stApp {
    background: linear-gradient(180deg, #08080d 0%, #0d1020 100%);
}

h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    color: #ffffff !important;
}

.main-wrap {
    max-width: 860px;
    margin: auto;
}

.hero-box {
    background: linear-gradient(135deg, rgba(124,58,237,0.18), rgba(59,130,246,0.14));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 2rem 1.5rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 10px 40px rgba(0,0,0,0.25);
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    line-height: 1.05;
    text-align: center;
    background: linear-gradient(135deg, #e9d5ff, #a5b4fc, #7dd3fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

.hero-sub {
    text-align: center;
    color: #cbd5e1;
    font-size: 1rem;
    max-width: 650px;
    margin: 0 auto 1rem auto;
}

.badges {
    text-align: center;
    margin-top: 0.75rem;
}

.badge {
    display: inline-block;
    padding: 0.4rem 0.8rem;
    margin: 0.25rem;
    border-radius: 999px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    color: #dbeafe;
    font-size: 0.82rem;
}

.section-card {
    background: rgba(17,24,39,0.85);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.18);
}

.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #93c5fd;
    margin-bottom: 0.6rem;
}

.muted {
    color: #94a3b8;
    font-size: 0.92rem;
}

.info-box {
    background: rgba(30,41,59,0.65);
    border: 1px solid rgba(129,140,248,0.25);
    border-left: 4px solid #818cf8;
    border-radius: 14px;
    padding: 1rem;
    margin-top: 0.8rem;
    color: #dbeafe;
    font-size: 0.92rem;
}

.tip-box {
    background: rgba(20, 35, 28, 0.85);
    border: 1px solid rgba(74, 222, 128, 0.22);
    border-left: 4px solid #4ade80;
    border-radius: 14px;
    padding: 1rem;
    margin-top: 0.8rem;
    color: #bbf7d0;
    font-size: 0.92rem;
}

.sample-box {
    background: rgba(15,23,42,0.78);
    border: 1px dashed rgba(255,255,255,0.12);
    border-radius: 14px;
    padding: 0.9rem 1rem;
    color: #cbd5e1;
    font-size: 0.9rem;
    margin-top: 0.8rem;
}

.stTextInput input,
.stTextArea textarea {
    background: #0f172a !important;
    color: #f8fafc !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #818cf8 !important;
    box-shadow: 0 0 0 2px rgba(129,140,248,0.20) !important;
}

.stSelectbox > div > div,
.stNumberInput input {
    background: #0f172a !important;
    color: #f8fafc !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
}

.stSlider {
    color: #e5e7eb !important;
}

div.stButton > button {
    width: 100%;
    border: none;
    border-radius: 14px;
    padding: 0.85rem 1rem;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    color: white;
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    box-shadow: 0 10px 25px rgba(59,130,246,0.25);
    transition: all 0.25s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 32px rgba(124,58,237,0.35);
}

.image-caption {
    text-align: center;
    color: #94a3b8;
    font-size: 0.85rem;
    margin-top: 0.5rem;
}

.premium-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}

.price-card {
    background: rgba(15,23,42,0.9);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 1rem;
}

.price-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.35rem;
}

.price-sub {
    color: #94a3b8;
    margin-bottom: 0.8rem;
}

.price-list {
    color: #e2e8f0;
    font-size: 0.94rem;
    line-height: 1.8;
}

.history-item {
    background: rgba(15,23,42,0.65);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 0.8rem;
    margin-bottom: 0.6rem;
    color: #cbd5e1;
    font-size: 0.9rem;
}

.footer-note {
    text-align: center;
    color: #64748b;
    font-size: 0.82rem;
    padding-bottom: 1rem;
}

@media (max-width: 700px) {
    .hero-title { font-size: 2.2rem; }
    .premium-grid { grid-template-columns: 1fr; }
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🎨 Studio Tools")
    st.write("Use presets, view history, and plan premium upgrades.")

    selected_preset = st.selectbox("Quick prompt preset", list(PROMPT_PRESETS.keys()))

    st.markdown("---")
    st.subheader("Recent prompts")
    if st.session_state.history:
        for item in st.session_state.history[:5]:
            st.caption(item["time"])
            st.write(item["prompt"][:80] + ("..." if len(item["prompt"]) > 80 else ""))
            st.markdown("---")
    else:
        st.caption("No prompts yet.")

    st.subheader("Premium idea")
    st.write("Sell premium prompt packs, creator templates, or faster access.")
    st.link_button("Buy Premium", "https://gumroad.com/")

# ── Wrapper start ────────────────────────────────────────────────────────────
st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

# ── Hero section ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-box">
    <div class="hero-title">✨ AI Image Studio</div>
    <div class="hero-sub">
        Turn your words into stunning visuals with free AI image models.
        Generate art, posters, cinematic scenes, product mockups, and social content in seconds.
    </div>
    <div class="badges">
        <span class="badge">🎨 AI Art</span>
        <span class="badge">⚡ Fast Generation</span>
        <span class="badge">🆓 Free Models</span>
        <span class="badge">⬇️ Instant Download</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── API section ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Hugging Face API Token</div>', unsafe_allow_html=True)
st.markdown('<div class="muted">Enter your free Hugging Face token to generate images.</div>', unsafe_allow_html=True)

hf_token = st.text_input(
    "HF Token",
    placeholder="hf_xxxxxxxxxxxxxxxxxxxxx",
    type="password",
    label_visibility="collapsed"
)

st.markdown("""
<div class="info-box">
<b>How to get a free token:</b><br>
Go to <b>huggingface.co</b> → <b>Settings</b> → <b>Access Tokens</b> → <b>New Token</b> → choose <b>Read</b>.
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Model section ────────────────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Choose Your Model</div>', unsafe_allow_html=True)

MODELS = {
    "Stable Diffusion 3.5 Medium — Best overall quality": "stabilityai/stable-diffusion-3.5-medium",
    "Stable Diffusion XL — Fast and detailed": "stabilityai/stable-diffusion-xl-base-1.0",
    "FLUX.1-schnell — Ultra fast": "black-forest-labs/FLUX.1-schnell",
    "Dreamlike Photoreal — Realistic photos": "dreamlike-art/dreamlike-photoreal-2.0",
}

model_label = st.selectbox(
    "Model",
    list(MODELS.keys()),
    label_visibility="collapsed"
)
model_id = MODELS[model_label]

st.markdown(f"""
<div class="sample-box">
<b>Selected model:</b> {model_label}
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Prompt section ───────────────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Describe Your Image</div>', unsafe_allow_html=True)

default_prompt = PROMPT_PRESETS[selected_preset] if selected_preset != "None" else ""

prompt = st.text_area(
    "Prompt",
    value=default_prompt,
    placeholder="Example: A dreamy mountain village at sunrise, soft golden light, cinematic atmosphere, ultra detailed, realistic, 8k",
    height=120,
    label_visibility="collapsed"
)

negative_prompt = st.text_area(
    "Negative Prompt",
    placeholder="Optional: blurry, low quality, watermark, extra fingers, distorted face, text",
    height=80,
    label_visibility="collapsed"
)

st.markdown("""
<div class="tip-box">
<b>Prompt tip:</b> Add style words like <i>cinematic, realistic, soft lighting, ultra detailed, 8k, studio quality, pastel colors</i>.
</div>
""", unsafe_allow_html=True)

with st.expander("See sample prompts"):
    st.write("**Cinematic:** A futuristic city street at night, neon reflections, rainy atmosphere, cinematic lighting, ultra detailed")
    st.write("**Fantasy:** A magical forest with glowing mushrooms, floating lights, fantasy art, dreamy, highly detailed")
    st.write("**Product shot:** Luxury perfume bottle on marble surface, soft shadows, premium ad photography, realistic")
    st.write("**Portrait:** Elegant woman in royal blue dress, studio lighting, high fashion photography, detailed face")

with st.expander("Prompt preview"):
    if prompt.strip():
        st.code(prompt, language=None)
    else:
        st.caption("Your prompt preview will appear here.")
st.markdown('</div>', unsafe_allow_html=True)

# ── Settings section ─────────────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Generation Settings</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    guidance = st.slider("Guidance Scale", 1.0, 20.0, 7.5, 0.5)
with col2:
    num_steps = st.slider("Inference Steps", 10, 50, 25, 5)

st.markdown("""
<div class="sample-box">
Higher guidance follows your prompt more closely. Higher steps can improve quality but may take longer.
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Generate section ─────────────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Generate</div>', unsafe_allow_html=True)

generate = st.button("🎨 Generate Image")

if generate:
    if not hf_token:
        st.error("Please enter your Hugging Face API token.")
    elif not prompt.strip():
        st.error("Please enter a prompt.")
    else:
        api_url = f"https://api-inference.huggingface.co/models/{model_id}"
        headers = {"Authorization": f"Bearer {hf_token}"}
        payload = {
            "inputs": prompt,
            "parameters": {
                "negative_prompt": negative_prompt or "",
                "guidance_scale": guidance,
                "num_inference_steps": num_steps,
            }
        }

        with st.spinner("Generating your image... this can take a little time on free models."):
            try:
                response = requests.post(api_url, headers=headers, json=payload, timeout=120)

                if response.status_code == 200:
                    image = Image.open(io.BytesIO(response.content))
                    st.image(image, use_container_width=True)
                    st.markdown('<div class="image-caption">Image generated successfully</div>', unsafe_allow_html=True)

                    buf = io.BytesIO()
                    image.save(buf, format="PNG")

                    st.download_button(
                        label="⬇️ Download PNG",
                        data=buf.getvalue(),
                        file_name="ai_image.png",
                        mime="image/png",
                    )

                    st.session_state.history.insert(0, {
                        "time": datetime.now().strftime("%d %b %Y • %I:%M %p"),
                        "prompt": prompt
                    })

                elif response.status_code == 503:
                    st.warning("Model is loading right now. Wait around 20–30 seconds and try again.")
                elif response.status_code == 401:
                    st.error("Invalid Hugging Face token. Please check it and try again.")
                else:
                    st.error(f"API Error {response.status_code}: {response.text[:300]}")

            except requests.exceptions.Timeout:
                st.error("Request timed out. The model may be busy. Please try again.")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# ── Recent history section ───────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Recent Prompt History</div>', unsafe_allow_html=True)

if st.session_state.history:
    for item in st.session_state.history[:3]:
        st.markdown(
            f'<div class="history-item"><b>{item["time"]}</b><br>{item["prompt"]}</div>',
            unsafe_allow_html=True
        )
else:
    st.markdown('<div class="sample-box">Your generated prompt history will appear here.</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Premium section ──────────────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Upgrade Option</div>', unsafe_allow_html=True)

st.markdown("""
<div class="premium-grid">
    <div class="price-card">
        <div class="price-title">Free</div>
        <div class="price-sub">Great for testing</div>
        <div class="price-list">
            • Use your own Hugging Face token<br>
            • Access free models<br>
            • Generate and download images<br>
            • Basic usage
        </div>
    </div>
    <div class="price-card">
        <div class="price-title">Premium</div>
        <div class="price-sub">For creators and sellers</div>
        <div class="price-list">
            • Faster generation<br>
            • Premium prompt packs<br>
            • Advanced styles and templates<br>
            • Creator tools for social media
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.link_button("🔥 Buy Premium Prompts", "https://gumroad.com/")
st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-note">
Built with Streamlit + Hugging Face Inference API • Free starter version
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)