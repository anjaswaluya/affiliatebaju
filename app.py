import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

# 1. PAGE CONFIGURATION & UI SETUP
st.set_page_config(
    page_title="Master Elka's Seedance 2.0 Prompt Generator v2",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Master Elka's Seedance 2.0 Prompt Generator (Multi-Image v2)")
st.markdown("Generasikan 5 prompt Seedance / Nano Banana 2 otomatis hanya dengan menggabungkan foto Model + foto Produk.")
st.write("---")

# Initialize Gemini API securely from Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ `GEMINI_API_KEY` tidak ditemukan di Streamlit Secrets. Harap konfigurasi di dashboard settings Streamlit Anda.")
    st.stop()

# 2. SIDEBAR CONFIGURATION (Dua Tempat Upload)
st.sidebar.header("📁 Upload Assets")

# Uploader 1: Foto Produk
uploaded_product = st.sidebar.file_uploader(
    "1. Upload Foto Produk (Baju/Outfit)", 
    type=["png", "jpg", "jpeg"],
    help="Upload foto screenshot baju yang mau dipromosikan."
)

if uploaded_product:
    prod_img = Image.open(uploaded_product)
    st.sidebar.image(prod_img, caption="📦 Foto Produk Terdeteksi", use_container_width=True)

# Uploader 2: Foto Model
uploaded_model = st.sidebar.file_uploader(
    "2. Upload Foto Model (Wajah/Talent)", 
    type=["png", "jpg", "jpeg"],
    help="Upload foto wajah model/talent (bisa foto diri sendiri atau model bebas)."
)

if uploaded_model:
    model_img = Image.open(uploaded_model)
    st.sidebar.image(model_img, caption="👤 Foto Model Terdeteksi", use_container_width=True)

# 3. BACKEND MULTIMODAL PROMPT ENGINE
def generate_multimodal_prompts(prod_image, model_image):
    
    system_instruction = """
    You are an expert AI Video Prompt Engineer specialized in Seedance 2.0 and Nano Banana 2 video generation.
    You will be provided with TWO images:
    1. A product image (apparel/clothing/outfit).
    2. A model image (the person who will wear the outfit).

    YOUR TASK:
    Analyze the physical features, facial structure, skin tone, and gender of the person in the model image. 
    Analyze the exact style, color, pattern, and texture of the apparel in the product image.
    Then, generate exactly 5 unique, high-end commercial video prompt variations blending them together perfectly.

    SEEDANCE 2.0 / NANO BANANA 2 PROMPT ARCHITECTURE RULES:
    1. Duration & Aspect Ratio: Every variation must start by enforcing "13s duration, 9:16 vertical aspect ratio, seamless looping animation".
    2. Character & Styling Locking: Describe the model from the provided model image accurately in text tokens (ethnicity, hair, age look, facial structure) and state that this character is wearing the exact outfit from the product image with 100% material consistency.
    3. Motion Sequencing: Each variation must sequence exactly 8 fast-cut, high-energy dynamic commercial scenes (e.g., modern runway walk, macro close-up of cloth texture, clean studio posing, lookbook angles, interactive cloth adjustments, slow-motion turns) smoothly compressed into 13 seconds.
    4. Settings Variation: Randomize the background environment across the 5 options (e.g., minimalist lighting studio, industrial concrete background, sleek retail store, modern city street).
    5. Anti-Sensor & Safety Guardrails: Every variation must append this exact negative prompt token block at the absolute end: "STRICT NEGATIVE: human, skin, text, words, letters, graphics, logos, choppy edits, music, bgm."

    OUTPUT FORMAT REQUIREMENT:
    Return your response strictly as a raw JSON array containing exactly 5 string items, with no markdown formatting wraps like ```json or 
```. Each string item represents one fully formed, single-paragraph prompt.
    Example format:
    [
      "Prompt text 1...",
      "Prompt text 2...",
      "Prompt text 3...",
      "Prompt text 4...",
      "Prompt text 5..."
    ]
    """

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config={
            "temperature": 0.85,
            "response_mime_type": "application/json"
        },
        system_instruction=system_instruction
    )

    # Kirim kedua gambar sekaligus ke Gemini 2.5 Flash
    response = model.generate_content([
        "Analyze both the model image and the product image to construct 5 highly detailed commercial video prompt strings for Seedance 2.0.",
        Image.open(prod_image),
        Image.open(model_image)
    ])
    
    return json.loads(response.text)

# 4. MAIN INTERACTION SCREEN
st.subheader("🚀 Generator Dashboard")

if not uploaded_product or not uploaded_model:
    st.info("💡 Hubungkan kedua aset! Silakan upload Foto Produk DAN Foto Model di sidebar untuk mengaktifkan AI.")
else:
    if st.button("✨ Generate 5 Premium Prompt Variations", type="primary", use_container_width=True):
        with st.spinner("🤖 AI Gemini sedang memadukan wajah model dan detail produk Anda..."):
            try:
                prompts = generate_multimodal_prompts(uploaded_product, uploaded_model)
                st.session_state['multimodal_prompts'] = prompts
                st.success("🎉 Berhasil memadukan aset! 5 Prompt Seedance 2.0 siap digunakan.")
            except Exception as e:
                st.error(f"Terjadi kesalahan saat memproses gambar: {e}")

if 'multimodal_prompts' in st.session_state:
    st.markdown("### 📋 Copy-Pasteable Prompt Variations")
    st.caption("Salin prompt di bawah ini ke Seedance / Nano Banana 2 untuk melihat keajaibannya.")
    
    for idx, prompt_text in enumerate(st.session_state['multimodal_prompts'], start=1):
        with st.expander(f"🔍 Variasi {idx} (8 Scenes Dynamic Commercial)", expanded=True):
            st.code(prompt_text, language="text")
