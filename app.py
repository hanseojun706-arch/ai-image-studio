import base64
import io
import json
import os
import textwrap
from datetime import datetime
from typing import Optional, Tuple

import requests
import streamlit as st
from PIL import Image

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(
    page_title="Nova AI Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------
# APP SETTINGS
# ------------------------------------------------------------
APP_NAME = "Nova AI Studio"
TAGLINE = "Clean AI Image & Media Studio"
CONTACT_EMAIL = "yourmail@example.com"   # <<< replace this
ABOUT_TEXT = """
Nova AI Studio helps users create visuals in a simple and professional way.
Generate AI images from prompts, upload an existing image for restyling,
preview uploaded videos, and explore media features in one clean website.
"""

INTRO_TEXT = """
Welcome to Nova AI Studio — a modern AI-powered creative space for image creation,
image restyling, media uploads, and elegant presentation. This app is designed
to be easy for anyone to understand and use.
"""

# Pollinations currently documents that generation requests require an API key.
# Put your key in Streamlit Secrets:
# [secrets]
# POLLINATIONS_API_KEY = "YOUR_KEY"
POLLINATIONS_API_KEY = st.secrets.get("POLLINATIONS_API_KEY", "")

# Pollinations base URL
POLLINATIONS_BASE = "https://gen.pollinations.ai"

# Optional app behavior flags
ENABLE_VIDEO_GENERATION = True
ENABLE_IMAGE_EDIT = True

# ============================================================
# STYLES
# ============================================================
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(126, 87, 255, 0.16), transparent 25%),
        radial-gradient(circle at top right, rgba(0, 194, 255, 0.12), transparent 25%),
        radial-gradient(circle at bottom left, rgba(255, 0, 140, 0.10), transparent 18%),
        linear-gradient(135deg, #0b1020 0%, #12172a 50%, #0c1326 100%);
    color: #f5f7ff;
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    max-width: 1280px;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(15,22,45,0.95), rgba(9,14,29,0.98));
    border-right: 1px solid rgba(255,255,255,0.08);
}

.hero-card, .glass-card, .feature-card, .footer-card {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    box-shadow: 0 10px 35px rgba(0,0,0,0.25);
}

.hero-card {
    padding: 30px;
    margin-bottom: 18px;
}

.glass-card {
    padding: 18px;
    margin-bottom: 16px;
}

.feature-card {
    padding: 20px;
    min-height: 170px;
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
    font-weight: 600;
    color: #dce4ff;
    margin-bottom: 14px;
}

.hero-title {
    font-size: 3rem;
    line-height: 1.1;
    font-weight: 900;
    letter-spacing: -0.03em;
    margin-bottom: 10px;
    color: #ffffff;
}

.hero-subtitle {
    font-size: 1.08rem;
    line-height: 1.8;
    color: #d7defa;
    max-width: 850px;
}

.section-title {
    font-size: 1.4rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.25rem;
}

.section-subtitle {
    font-size: 0.98rem;
    color: #cfd8ff;
    margin-bottom: 1rem;
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
    font-weight: 800;
}

.kpi p {
    margin: 0.3rem 0 0;
    color: #c7d2ff;
    font-size: 0.92rem;
}

.stButton > button {
    width: 100%;
    border-radius: 14px;
    border: none;
    padding: 0.82rem 1rem;
    font-weight: 700;
    background: linear-gradient(135deg, #7b61ff 0%, #12b5ff 100%);
    color: white;
    box-shadow: 0 8px 25px rgba(95, 94, 255, 0.30);
}

.stDownloadButton > button {
    width: 100%;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.12);
    padding: 0.82rem 1rem;
    font-weight: 700;
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
    border-color: rgba(255,255,255,0.08);
}

.small-note {
    color: #c8d1fb;
    font-size: 0.88rem;
    line-height: 1.7;
}

.success-chip {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 999px;
    background: rgba(45, 206, 137, 0.12);
    color: #b7ffd8;
    border: 1px solid rgba(45, 206, 137, 0.25);
    font-size: 12px;
    font-weight: 700;
}

.warning-chip {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 999px;
    background: rgba(255, 196, 0, 0.10);
    color: #ffe8a3;
    border: 1px solid rgba(255, 196, 0, 0.18);
    font-size: 12px;
    font-weight: 700;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ============================================================
# HELPERS
# ============================================================
def render_card_open(class_name="glass-card"):
    st.markdown(f'<div class="{class_name}">', unsafe_allow_html=True)

def render_card_close():
    st.markdown('</div>', unsafe_allow_html=True)

def prompt_is_valid(prompt: str) -> bool:
    return bool(prompt and len(prompt.strip()) >= 6)

def build_enhanced_prompt(prompt: str, style: str, quality: str) -> str:
    style_addon = {
        "Realistic": "highly detailed realistic photography, natural lighting, cinematic depth",
        "Anime": "beautiful anime illustration, expressive details, vibrant visual storytelling",
        "Fantasy": "epic fantasy concept art, magical atmosphere, dramatic lighting",
        "Minimal": "clean minimalist composition, elegant shapes, soft balanced layout",
        "3D": "high quality 3D render, depth, polished materials, studio lighting",
        "Portrait": "professional portrait composition, balanced face details, refined skin tones",
        "Product": "premium product photography, studio shot, commercial lighting",
        "Cinematic": "cinematic composition, mood lighting, ultra-detailed atmosphere",
    }.get(style, "high quality composition")

    quality_addon = {
        "Standard": "sharp details, clean composition",
        "High": "high detail, refined textures, polished output",
        "Ultra": "ultra detailed, premium quality, crisp focus, visually striking",
    }.get(quality, "sharp details")

    return f"{prompt.strip()}, {style_addon}, {quality_addon}"

def img_to_bytes(img: Image.Image, format_: str = "PNG") -> bytes:
    buffer = io.BytesIO()
    img.save(buffer, format=format_)
    buffer.seek(0)
    return buffer.getvalue()

def safe_filename(name: str) -> str:
    return "".join(c for c in name if c.isalnum() or c in ("-", "_")).strip() or "download"

def download_link_bytes(data: bytes, filename: str, mime: str) -> None:
    st.download_button(
        label=f"Download {filename}",
        data=data,
        file_name=filename,
        mime=mime,
        use_container_width=True,
    )

def show_intro():
    render_card_open("hero-card")
    st.markdown('<div class="brand-chip">✨ Clean • Professional • Easy to Use</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-title">{APP_NAME}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="hero-subtitle">{INTRO_TEXT}</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="kpi"><h3>AI Images</h3><p>Prompt-based generation</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="kpi"><h3>Uploads</h3><p>Image & video support</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="kpi"><h3>Professional UI</h3><p>Clean sections and layout</p></div>', unsafe_allow_html=True)
    render_card_close()

def sidebar():
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
        ],
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Quick Information")
    st.sidebar.info(
        "This app supports AI image generation, image upload/restyle, "
        "video upload/preview, and a clean presentation layout."
    )

    if POLLINATIONS_API_KEY:
        st.sidebar.markdown(
            '<div class="success-chip">API Key Connected</div>',
            unsafe_allow_html=True
        )
    else:
        st.sidebar.markdown(
            '<div class="warning-chip">API Key Missing</div>',
            unsafe_allow_html=True
        )
        st.sidebar.caption("Add POLLINATIONS_API_KEY in Streamlit Secrets.")

    st.sidebar.markdown("---")
    st.sidebar.caption("Replace the contact email and branding text in the code before deployment.")

    return page

# ============================================================
# API FUNCTIONS
# ============================================================
def pollinations_headers() -> dict:
    headers = {"Content-Type": "application/json"}
    if POLLINATIONS_API_KEY:
        headers["Authorization"] = f"Bearer {POLLINATIONS_API_KEY}"
    return headers

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
    """
    Uses OpenAI-compatible image generation endpoint.
    Returns (image_bytes, error_message)
    """
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
        response = requests.post(url, headers=pollinations_headers(), json=payload, timeout=120)
        if response.status_code != 200:
            return None, f"API error {response.status_code}: {response.text}"

        data = response.json()
        items = data.get("data", [])
        if not items:
            return None, "No image returned by the API."

        b64_data = items[0].get("b64_json")
        if not b64_data:
            return None, "Image data missing in API response."

        image_bytes = base64.b64decode(b64_data)
        return image_bytes, None
    except requests.Timeout:
        return None, "Request timed out. Please try again."
    except Exception as e:
        return None, f"Generation failed: {str(e)}"

def edit_image_pollinations(
    image_bytes: bytes,
    prompt: str,
    model: str = "flux",
) -> Tuple[Optional[bytes], Optional[str]]:
    """
    Uses image edit endpoint with multipart upload.
    """
    if not POLLINATIONS_API_KEY:
        return None, "Missing POLLINATIONS_API_KEY in Streamlit Secrets."

    url = f"{POLLINATIONS_BASE}/v1/images/edits"
    headers = {}
    if POLLINATIONS_API_KEY:
        headers["Authorization"] = f"Bearer {POLLINATIONS_API_KEY}"

    files = {
        "image": ("upload.png", image_bytes, "image/png")
    }
    data = {
        "prompt": prompt,
        "model": model,
    }

    try:
        response = requests.post(url, headers=headers, data=data, files=files, timeout=180)
        if response.status_code != 200:
            return None, f"API error {response.status_code}: {response.text}"

        # Some providers return JSON, some may return binary.
        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type:
            res_json = response.json()
            items = res_json.get("data", [])
            if items and items[0].get("b64_json"):
                return base64.b64decode(items[0]["b64_json"]), None
            if items and items[0].get("url"):
                image_url = items[0]["url"]
                img_res = requests.get(image_url, timeout=120)
                if img_res.status_code == 200:
                    return img_res.content, None
                return None, "Failed to download edited image from returned URL."
            return None, "Unexpected JSON response from image edit API."

        return response.content, None
    except requests.Timeout:
        return None, "Edit request timed out. Please try again."
    except Exception as e:
        return None, f"Edit failed: {str(e)}"

def generate_video_pollinations(
    prompt: str,
    model: str = "wan",
    duration: int = 4,
    aspect_ratio: str = "16:9",
) -> Tuple[Optional[bytes], Optional[str]]:
    """
    Uses GET /image/{prompt} that Pollinations documents as returning image/jpeg or video/mp4
    depending on the model. Many video models are paid/preview.
    """
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
            return None, "The API did not return a video file."

        return response.content, None
    except requests.Timeout:
        return None, "Video generation timed out. Try a shorter prompt or smaller duration."
    except Exception as e:
        return None, f"Video generation failed: {str(e)}"

# ============================================================
# SESSION STATE
# ============================================================
if "gallery" not in st.session_state:
    st.session_state.gallery = []

def save_to_gallery(kind: str, title: str, data: bytes, mime: str):
    st.session_state.gallery.insert(0, {
        "kind": kind,
        "title": title,
        "data": data,
        "mime": mime,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })

# ============================================================
# PAGE SECTIONS
# ============================================================
def home_page():
    show_intro()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="section-title">Image Generator</div>
                <div class="section-subtitle">Turn text prompts into visual artwork</div>
                <div class="small-note">
                    Enter your prompt, choose style and quality, and create high-quality images
                    in a simple guided workflow.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="section-title">Upload & Restyle</div>
                <div class="section-subtitle">Transform uploaded images with AI</div>
                <div class="small-note">
                    Upload an image and describe the new visual style you want.
                    Great for portraits, posters, fantasy looks, and creative redesigns.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="section-title">Video Studio</div>
                <div class="section-subtitle">Upload, preview, and optionally generate</div>
                <div class="small-note">
                    Upload and preview your video files directly in the website.
                    Optional prompt-to-video generation can be enabled when your provider supports it.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    render_card_open()
    st.markdown('<div class="section-title">How this website works</div>', unsafe_allow_html=True)
    st.markdown(
        """
        1. Go to **Image Generator** to create visuals from a prompt.  
        2. Use **Image Restyle** to upload an image and transform it.  
        3. Use **Video Studio** to upload and preview videos, and optionally generate videos if your API plan supports it.  
        4. Open **Gallery** to view and download your generated or uploaded content.  
        """)
    render_card_close()

    render_card_open()
    st.markdown('<div class="section-title">Easy-to-understand information</div>', unsafe_allow_html=True)
    st.write(
        "This website is made for simplicity. The layout is clean, the sections are separated clearly, "
        "and each page explains what the user should do. You can customize the logo, colors, text, "
        "contact email, and media features before deployment."
    )
    render_card_close()

def image_generator_page():
    render_card_open()
    st.markdown('<div class="section-title">AI Image Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Generate images from text prompts</div>', unsafe_allow_html=True)
    render_card_close()

    col_left, col_right = st.columns([1.05, 0.95], gap="large")

    with col_left:
        render_card_open()
        prompt = st.text_area(
            "Describe your image",
            placeholder="Example: A luxury glass perfume bottle on a marble table, soft studio lighting, premium product photography",
            height=140,
        )

        style = st.selectbox(
            "Style",
            ["Realistic", "Anime", "Fantasy", "Minimal", "3D", "Portrait", "Product", "Cinematic"],
            index=0,
        )

        c1, c2 = st.columns(2)
        with c1:
            quality = st.selectbox("Quality", ["Standard", "High", "Ultra"], index=1)
            model = st.selectbox("Model", ["flux", "zimage", "gptimage"], index=0)
        with c2:
            size = st.selectbox(
                "Aspect / Size",
                ["1024x1024", "1024x1536", "1536x1024", "768x1344", "1344x768"],
                index=0,
            )
            safe_mode = st.toggle("Safe mode", value=True)

        negative_prompt = st.text_input(
            "Negative prompt",
            value="blurry, low quality, distorted face, bad anatomy, text, watermark, extra fingers"
        )

        enhance = st.toggle("Enhance prompt automatically", value=True)

        seed_mode = st.selectbox("Seed mode", ["Random", "Fixed"], index=0)
        seed_value = st.number_input("Seed", min_value=-1, max_value=999999, value=-1, step=1)

        generate_clicked = st.button("Generate Image")

        render_card_close()

    with col_right:
        render_card_open()
        st.markdown("### Result Preview")
        result_box = st.empty()
        details_box = st.empty()
        render_card_close()

    if generate_clicked:
        if not prompt_is_valid(prompt):
            st.error("Please enter a more detailed prompt.")
            return

        width, height = map(int, size.split("x"))
        final_prompt = build_enhanced_prompt(prompt, style, quality)
        final_seed = -1 if seed_mode == "Random" else int(seed_value)

        with st.spinner("Generating your image..."):
            img_bytes, error = generate_image_pollinations(
                prompt=final_prompt,
                model=model,
                width=width,
                height=height,
                negative_prompt=negative_prompt,
                seed=final_seed,
                enhance=enhance,
                safe=safe_mode,
            )

        if error:
            st.error(error)
            st.info(
                "Tip: add your API key in Streamlit Secrets and try again. "
                "Also try a more specific prompt with style details."
            )
            return

        result_box.image(img_bytes, caption="Generated Image", use_container_width=True)
        details_box.success("Image generated successfully.")
        save_to_gallery("image", "generated_image.png", img_bytes, "image/png")
        download_link_bytes(img_bytes, "generated_image.png", "image/png")

        with st.expander("Show final prompt used"):
            st.code(final_prompt)

def image_restyle_page():
    render_card_open()
    st.markdown('<div class="section-title">Upload Image & Restyle</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Upload your image and describe how you want it transformed</div>',
        unsafe_allow_html=True
    )
    render_card_close()

    c1, c2 = st.columns([1, 1], gap="large")

    with c1:
        render_card_open()
        uploaded = st.file_uploader(
            "Upload an image",
            type=["png", "jpg", "jpeg", "webp"],
            help="Upload a clear image for best results.",
        )

        edit_prompt = st.text_area(
            "Describe the new style or transformation",
            placeholder="Example: Make it look like a high-end cinematic portrait with elegant lighting and premium color grading",
            height=120
        )

        edit_model = st.selectbox("Edit model", ["flux", "gptimage", "klein"], index=0)
        edit_clicked = st.button("Restyle Image")
        render_card_close()

    with c2:
        render_card_open()
        st.markdown("### Preview")
        if uploaded:
            st.image(uploaded, caption=f"Uploaded: {uploaded.name}", use_container_width=True)
        else:
            st.info("Your uploaded image preview will appear here.")
        render_card_close()

    if edit_clicked:
        if not uploaded:
            st.error("Please upload an image first.")
            return
        if not prompt_is_valid(edit_prompt):
            st.error("Please enter a clear transformation prompt.")
            return

        try:
            pil_image = Image.open(uploaded).convert("RGBA")
            image_bytes = img_to_bytes(pil_image, "PNG")
        except Exception as e:
            st.error(f"Could not process uploaded image: {str(e)}")
            return

        with st.spinner("Restyling image..."):
            out_bytes, error = edit_image_pollinations(
                image_bytes=image_bytes,
                prompt=edit_prompt,
                model=edit_model,
            )

        if error:
            st.error(error)
            st.info("Make sure your API key is valid and your provider plan supports image editing.")
            return

        st.success("Image restyled successfully.")
        st.image(out_bytes, caption="Restyled Image", use_container_width=True)
        save_to_gallery("image", "restyled_image.png", out_bytes, "image/png")
        download_link_bytes(out_bytes, "restyled_image.png", "image/png")

def video_studio_page():
    render_card_open()
    st.markdown('<div class="section-title">Video Studio</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Upload, preview, and optionally generate videos</div>',
        unsafe_allow_html=True
    )
    render_card_close()

    tab1, tab2 = st.tabs(["Upload Video", "Generate Video"])

    with tab1:
        render_card_open()
        up_video = st.file_uploader(
            "Upload a video",
            type=["mp4", "mov", "avi", "mkv", "webm"],
            help="You can preview uploaded videos directly in the app."
        )

        if up_video:
            st.video(up_video)
            video_bytes = up_video.read()
            save_to_gallery("video", up_video.name, video_bytes, "video/mp4")
            download_link_bytes(video_bytes, up_video.name, "video/mp4")
            st.success("Video uploaded and ready.")
        else:
            st.info("Upload a video to preview it here.")
        render_card_close()

    with tab2:
        render_card_open()
        st.markdown("### Prompt to Video")
        st.caption(
            "This section is optional. Many current video models require paid/preview API access."
        )
        v_prompt = st.text_area(
            "Describe the video",
            placeholder="Example: A cinematic slow camera move through a glowing futuristic city at night, neon reflections, dramatic atmosphere",
            height=120
        )
        vc1, vc2, vc3 = st.columns(3)
        with vc1:
            v_model = st.selectbox("Video model", ["wan", "ltx-2", "seedance"], index=0)
        with vc2:
            v_duration = st.slider("Duration (seconds)", min_value=2, max_value=10, value=4)
        with vc3:
            v_ratio = st.selectbox("Aspect ratio", ["16:9", "9:16"], index=0)

        gen_video = st.button("Generate Video")

        if gen_video:
            if not prompt_is_valid(v_prompt):
                st.error("Please enter a more detailed video prompt.")
            else:
                with st.spinner("Generating video..."):
                    video_bytes, error = generate_video_pollinations(
                        prompt=v_prompt,
                        model=v_model,
                        duration=v_duration,
                        aspect_ratio=v_ratio,
                    )
                if error:
                    st.error(error)
                    st.info(
                        "Your provider may require a paid plan or may not have video access enabled."
                    )
                else:
                    st.video(video_bytes)
                    save_to_gallery("video", "generated_video.mp4", video_bytes, "video/mp4")
                    download_link_bytes(video_bytes, "generated_video.mp4", "video/mp4")
                    st.success("Video generated successfully.")
        render_card_close()

def gallery_page():
    render_card_open()
    st.markdown('<div class="section-title">Gallery</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">View your generated and uploaded content</div>', unsafe_allow_html=True)
    render_card_close()

    items = st.session_state.gallery
    if not items:
        st.info("No items in gallery yet. Generate or upload something first.")
        return

    for idx, item in enumerate(items):
        render_card_open()
        st.markdown(f"### {item['title']}")
        st.caption(f"{item['kind'].title()} • {item['time']}")
        if item["kind"] == "image":
            st.image(item["data"], use_container_width=True)
        elif item["kind"] == "video":
            st.video(item["data"])
        download_link_bytes(item["data"], item["title"], item["mime"])
        render_card_close()

def about_page():
    render_card_open()
    st.markdown('<div class="section-title">About Us</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Professional, simple, and user-friendly creative platform</div>', unsafe_allow_html=True)
    st.write(ABOUT_TEXT)
    st.write(
        "This website is designed to help users understand AI creation tools without confusion. "
        "The design is clean, the features are separated clearly, and the workflow is easy for beginners."
    )
    render_card_close()

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="section-title">Our Mission</div>
                <div class="small-note">
                    To provide a beautiful and understandable AI media website where anyone can
                    generate images, upload media, and explore creative tools with confidence.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="section-title">Why This Website</div>
                <div class="small-note">
                    Many websites feel confusing or too technical. This one focuses on clarity,
                    elegant layout, smooth sections, and an overall professional experience.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

def contact_page():
    render_card_open()
    st.markdown('<div class="section-title">Contact</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Let users reach you easily</div>', unsafe_allow_html=True)
    st.write("You can customize the contact section before deploying.")
    st.markdown(f"**Contact email:** {CONTACT_EMAIL}")
    st.write(
        "You may also add social links, business inquiry details, or a support form later."
    )
    render_card_close()

    render_card_open()
    with st.form("contact_form"):
        name = st.text_input("Your name")
        email = st.text_input("Your email")
        message = st.text_area("Your message", height=140)
        submitted = st.form_submit_button("Send Message")
        if submitted:
            if not name or not email or not message:
                st.error("Please fill in all fields.")
            else:
                st.success(
                    "Form submitted in the demo UI. For real email sending, connect an email backend service."
                )
    render_card_close()

# ============================================================
# FOOTER
# ============================================================
def footer():
    st.markdown(
        f"""
        <div class="footer-card">
            <b>{APP_NAME}</b><br>
            <span class="small-note">
                {TAGLINE} • Easy to understand • Professional layout • Image and media focused
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# MAIN
# ============================================================
page = sidebar()

if page == "Home":
    home_page()
elif page == "Image Generator":
    image_generator_page()
elif page == "Image Restyle":
    image_restyle_page()
elif page == "Video Studio":
    video_studio_page()
elif page == "Gallery":
    gallery_page()
elif page == "About Us":
    about_page()
elif page == "Contact":
    contact_page()

footer()
