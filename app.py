import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

# 1. PAGE CONFIGURATION & UI SETUP
st.set_page_config(
    page_title="Master Elka's Seedance 2.0 Prompt Generator",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Master Elka's Seedance 2.0 Prompt Generator")
st.markdown("Optimize your outfit & apparel marketing workflow for Seedance 2.0 using advanced GenAI.")
st.write("---")

# Initialize Gemini API securely from Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ `GEMINI_API_KEY` tidak ditemukan di Streamlit Secrets. Harap konfigurasi di dashboard settings Streamlit Anda.")
    st.stop()

# 2. SIDEBAR CONFIGURATION
st.sidebar.header("📁 Configuration & Assets")

# File Uploader
uploaded_file = st.sidebar.file_uploader(
    "Upload Product Screenshot", 
    type=["png", "jpg", "jpeg"],
    help="Upload foto screenshot baju/outfit yang mau dipasang ke model."
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.sidebar.image(image, caption="Uploaded Product Screenshot", use_container_width=True)

# Model Selection
model_selection = st.sidebar.radio(
    "Select Model Profile:",
    options=["Perempuan (Nana)", "Laki-laki (El)"],
    index=0,
    help="Pilih identitas avatar digital untuk video Seedance."
)

# 3. BACKEND SYSTEM INSTRUCTIONS & LOGIC
def generate_seedance_prompts(uploaded_image, model_type):
    if model_type == "Perempuan (Nana)":
        model_profile_instruction = """
        - Character Identity: 28 years old, Indonesian Chinese-Sundanese (Chindo-Sunda) female, beautiful natural face, signature "messy bun" hairstyle.
        - Face Lock Requirement: You MUST explicitly include the phrase 'using reference file 402363.jpg for face lock' inside every prompt string.
        """
    else:  # Laki-laki (El)
        model_profile_instruction = """
        - Character Identity: Indonesian male, sharp nose (mancung), height 189 cm, weight 90 kg, athletic build, authentic Indonesian tan skin (kulit sawo matang).
        - Face Lock Requirement: No external face lock reference file required. Rely explicitly on the character identity tokens.
        """

    system_instruction = f"""
    You are an expert AI Video Prompt Engineer specialized in Seedance 2.0 video generation for high-end fashion and streetwear apparel marketing.
    Your objective is to analyze the attached outfit/apparel image and generate exactly 10 unique, diverse, and ready-to-use prompt variations.

    MODEL SPECIFICATION PROFILES:
    {model_profile_instruction}

    SEEDANCE 2.0 PROMPT ARCHITECTURE RULES (Apply to all 10 variations):
    1. Duration & Aspect Ratio: Every variation must start by enforcing "13s duration, 9:16 vertical aspect ratio, seamless looping animation".
    2. Apparel Styling: The character specified above must wear the exact outfit/apparel from the uploaded image with 100% design, texture, and structural consistency.
    3. Motion & Cinematic Sequencing Structure: Each variation must sequence exactly 8 fast-cut, high-energy dynamic lifestyle or commercial scenes. Compress these scenes seamlessly across the 13-second runtime. 
       - Examples of scenes to mix, randomize, and match: runway walk, tight macro details of apparel stitching/texture, crisp studio poses, lookbook angles, interactive zipper or clothing adjustments, dramatic urban turns, or slow-motion fabric waves. 
       - Ensure each of the 10 variations has a totally distinct narrative structure, backdrop setting (e.g., minimalist studio, Tokyo neon street, brutalist concrete wall, editorial studio), and sequence layout.
    4. Anti-Sensor & Safety Guardrails: Every variation must append this exact negative prompt token block at the absolute end: "STRICT NEGATIVE: human, skin, text, words, letters, graphics, logos, choppy edits, music, bgm."

    OUTPUT FORMAT REQUIREMENT:
    Return your response strictly as a raw JSON array containing exactly 10 string items, with no markdown formatting wraps like ```json or ```. Each string item represents one fully formed, single-paragraph prompt. 
    Example format:
    [
      "Prompt text 1...",
      "Prompt text 2..."
    ]
    """

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config={
            "temperature": 0.85,
            "response_mime_type": "application/json"
        },
        system_instruction=system_instruction
    )

    pil_image = Image.open(uploaded_image)
    response = model.generate_content([
        "Analyze this outfit file and generate the 10 distinct Seedance 2.0 JSON prompt strings according to your system instructions.", 
        pil_image
    ])
    
    return json.loads(response.text)

# 4. MAIN INTERACTION SCREEN
st.subheader("🚀 Generator Dashboard")

if not uploaded_file:
    st.info("💡 Silakan upload foto produk di sidebar terlebih dahulu untuk mengaktifkan AI Generator.")
else:
    if st.button("✨ Generate 10 Prompt Variations", type="primary", use_container_width=True):
        with st.spinner("🤖 AI Gemini sedang menganalisis baju dan menyusun struktur prompt Seedance..."):
            try:
                prompts = generate_seedance_prompts(uploaded_file, model_selection)
                st.session_state['generated_prompts'] = prompts
                st.success("🎉 Berhasil membuat 10 Variasi Prompt Seedance 2.0!")
            except Exception as e:
                st.error(f"Terjadi kesalahan saat membuat prompt: {e}")

if 'generated_prompts' in st.session_state:
    st.markdown("### 📋 Copy-Pasteable Prompt Variations")
    st.caption("Klik tombol di pojok kanan setiap kotak untuk langsung menyalin teks prompt.")
    
    for idx, prompt_text in enumerate(st.session_state['generated_prompts'], start=1):
        with st.expander(f"🔍 Variasi {idx}", expanded=True):
            st.code(prompt_text, language="text")
