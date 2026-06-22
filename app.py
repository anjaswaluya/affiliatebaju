import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

# 1. PAGE CONFIGURATION & MOBILE OPTIMIZED UI
st.set_page_config(
    page_title="Master Elka's Seedance Ultra-Detail Engine",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Seedance 2.0 Ultra-Detail Content Planner")
st.markdown("Membongkar detail produk secara mikro untuk akurasi video 100% konsisten.")
st.write("---")

# Initialize Gemini API securely from Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ `GEMINI_API_KEY` tidak ditemukan di Streamlit Secrets.")
    st.stop()

# 2. SIDEBAR CONFIGURATION
st.sidebar.header("📁 Upload Assets")

uploaded_product = st.sidebar.file_uploader(
    "1. Upload Foto Produk (Baju)", 
    type=["png", "jpg", "jpeg"]
)
if uploaded_product:
    st.sidebar.image(Image.open(uploaded_product), caption="📦 Foto Produk", use_container_width=True)

uploaded_model = st.sidebar.file_uploader(
    "2. Upload Foto Model (Wajah)", 
    type=["png", "jpg", "jpeg"]
)
if uploaded_model:
    st.sidebar.image(Image.open(uploaded_model), caption="👤 Foto Model", use_container_width=True)

# 3. BACKEND AI ENGINE (ULTRA DETAIL GARMENT LOCKING)
def generate_content_plan(prod_image, model_image):
    system_instruction = """
    You are a master AI Fashion Director and a High-Fidelity Prompt Engineer for Seedance 2.0 and Nano Banana 2.
    Your absolute mandate is to eliminate all visual hallucinations and guarantee 100% garment continuity across video frames.

    CRITICAL INSTRUCTION FOR ANALYSIS:
    Analyze the product image with microscopic focus. You must explicitly identify and describe:
    1. Precise Fabric Material: (e.g., crinkle waterproof nylon, matte windbreaker texture, semi-glossy polyester, tech-fleece).
    2. Zipper Anatomy: Exact location, type (e.g., full-length central black zipper track), and the visible zipper pull tab.
    3. Hood & Drawstring Architecture: Detailed shape of the hood, tracking the exact color, thickness, and structure of the drawstrings (e.g., 'round woven black elastic drawstrings hanging from the hood collar with hard plastic cylinder tips').
    4. Hardware & Accents: Text, small logos, elastic wrist cuffs, or specific pocket styles (e.g., 'zippered vertical welt side pockets').

    PROMPT GENERATION RULES (Output exactly 5 options):
    For each option, you must output a JSON object containing:
    - 'judul': Catchy Indonesian fashion affiliate marketing title.
    - 'alur_cerita': 13-second chronological video flow breakdown (In Indonesian).
    - 'seedance_prompt': The ultra-detailed prompt string.

    STRICT PROMPT STRUCTURE FOR 'seedance_prompt':
    1. Technical Prefix: Start with "13s duration, 9:16 vertical aspect ratio, seamless looping animation, ultra-high-fidelity 8k commercial fashion videography."
    2. Model Absolute Lock: Explicitly describe the man's features from the model image (e.g., 'an Indonesian male model with short dark hair, distinct mustache, defined jawline, confident expression, sawo matang skin tone').
    3. Garment Micro-Specification: Describe the outfit by stitching ALL extracted hardware/fabric specs together. You MUST repeat the micro-details of the jacket (fabric texture, zipper track, hood drawstrings with plastic tips, cuff style) throughout the motion descriptions to anchor the AI's rendering.
    4. Hyper-Detailed Scene Actions: Break down the 8 fast-cuts within the prompt paragraph by emphasizing how the jacket hardware interacts with light and motion (e.g., 'macro close-up shot tracking the full-length central black zipper gliding up', 'close-up on the hood showing the round woven black drawstrings swaying naturally', 'medium shot of the model walking, highlighting the wrinkled texture of the matte black waterproof nylon fabric under studio lights').
    5. Technical Suffix: End with "STRICT NEGATIVE: human, skin, text, words, letters, graphics, logos, choppy edits, music, bgm."

    OUTPUT FORMAT REQUIREMENT:
    Return response strictly as a raw JSON array containing exactly 5 objects with keys 'judul', 'alur_cerita', and 'seedance_prompt'. No markdown wrappers like ```json.
    """

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config={
            "temperature": 0.45, # Diturunkan secara ekstrem agar AI fokus pada detail faktual gambar, bukan improvisasi kreatif
            "response_mime_type": "application/json"
        },
        system_instruction=system_instruction
    )

    response = model.generate_content([
        "Perform a micro-hardware and texture analysis on the product image. Merge it flawlessly with the model's physical features to construct 5 ultra-detailed JSON packages.",
        Image.open(prod_image),
        Image.open(model_image)
    ])
    
    return json.loads(response.text)

# 4. MAIN INTERACTION SCREEN
if not uploaded_product or not uploaded_model:
    st.info("💡 **Tips Android:** Klik tombol `>` di pojok kiri atas untuk upload foto baju & model wajah lo!")
else:
    if st.button("✨ Racik 5 Opsi Konten (Ultra-Detail Mode)", type="primary", use_container_width=True):
        with st.spinner("🤖 AI sedang membedah serat kain, sleting, dan ujung tali secara mikro..."):
            try:
                results = generate_content_plan(uploaded_product, uploaded_model)
                st.session_state['mobile_content_results'] = results
                st.success("🎉 Sukses! Prompt ultra-detail siap dicopas.")
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")

# 5. DISPLAY RESULTS
if 'mobile_content_results' in st.session_state:
    st.markdown("---")
    st.markdown("### 📱 Hasil Rencana Konten Ultra-Detail")
    
    for idx, item in enumerate(st.session_state['mobile_content_results'], start=1):
        with st.container(border=True):
            st.markdown(f"#### 🌟 OPSI {idx}: {item['judul']}")
            
            st.markdown("**🎬 Alur Cerita Video (13 Detik, 8 Fast-Cuts):**")
            st.info(item['alur_cerita'])
            
            st.markdown("**📋 Teks Prompt Seedance 2.0 (Ultra-Detail Text Tokens):**")
            st.code(item['seedance_prompt'], language="text")
