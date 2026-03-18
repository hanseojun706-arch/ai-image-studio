import streamlit as st
import requests
from PIL import Image
import io
import datetime

# -----------------------------
# Config
# -----------------------------
APP_NAME = "AI Image Studio"
APP_TAGLINE = "Create AI images instantly"
FREE_DAILY_LIMIT = 1
PREMIUM_LINK = "https://aiimagestudio.gumroad.com/l/yrpblj"
PREMIUM_CODE = "AISTUDIO2026"

HF_TOKEN = st.secrets.get("HF_TOKEN", "")

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(page_title=APP_NAME, page_icon="🎨", layout="centered")

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
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("Premium")
    st.link_button("💎 Buy Premium", PREMIUM_LINK)

    premium_code_input = st.text_input("Enter Premium Code", type="password")

    if st.button("Unlock Premium"):
        if premium_code_input.strip() == PREMIUM_CODE:
            st.session_state.premium_unlocked = True
            st.success("Premium unlocked successfully.")
        else:
            st.error("Invalid premium code.")

    st.markdown("---")
    if st.session_state.premium_unlocked:
        st.success("Premium: Unlimited access")
    else:
        remaining = max(FREE_DAILY_LIMIT - st.session_state.usage_count, 0)
        st.info(f"Free images left today: {remaining}")

# -----------------------------
# Main UI
# -----------------------------
st.title("🎨 AI Image Studio")
st.write(APP_TAGLINE)

st.subheader("What you can create")
st.write("- Instagram posts")
st.write("- YouTube thumbnails")
st.write("- Product ads")
st.write("- Wallpapers and AI art")

st.markdown("---")

prompt = st.text_area(
    "Enter your prompt",
    placeholder="Example: A luxury perfume bottle on a marble table, premium ad photography, soft shadows, realistic, ultra detailed"
)

# -----------------------------
# Generate image
# -----------------------------
if st.button("Generate Image"):
    if not HF_TOKEN:
        st.error("HF_TOKEN is missing in Streamlit Secrets.")
    elif not prompt.strip():
        st.error("Please enter a prompt.")
    elif (not st.session_state.premium_unlocked) and st.session_state.usage_count >= FREE_DAILY_LIMIT:
        st.error("Free limit reached.")
        st.link_button("💎 Upgrade to Premium", PREMIUM_LINK)
    else:
        api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}

        with st.spinner("Generating image..."):
            try:
                response = requests.post(
                    api_url,
                    headers=headers,
                    json={"inputs": prompt},
                    timeout=120
                )

                if response.status_code == 200:
                    image = Image.open(io.BytesIO(response.content))
                    st.image(image, caption="Generated Image", use_container_width=True)

                    download_buffer = io.BytesIO()
                    image.save(download_buffer, format="PNG")

                    st.download_button(
                        label="Download Image",
                        data=download_buffer.getvalue(),
                        file_name="ai-image-studio.png",
                        mime="image/png"
                    )

                    if not st.session_state.premium_unlocked:
                        st.session_state.usage_count += 1

                    st.session_state.history.insert(0, prompt)

                elif response.status_code == 503:
                    st.warning("Model is loading. Wait a little and try again.")
                elif response.status_code == 401:
                    st.error("Invalid HF token.")
                else:
                    st.error(f"Generation failed. Status code: {response.status_code}")

            except requests.exceptions.Timeout:
                st.error("Request timed out. Please try again.")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

# -----------------------------
# History
# -----------------------------
st.markdown("---")
st.subheader("Recent Prompts")

if st.session_state.history:
    for item in st.session_state.history[:5]:
        st.write(f"- {item}")
else:
    st.write("No prompts yet.")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.write("© 2026 AI Image Studio")
