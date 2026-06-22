import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

# 1. PAGE CONFIGURATION & MOBILE OPTIMIZED UI
st.set_page_config(
    page_title="Master Elka's Seedance Suite v3",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Seedance 2.0 Content Planner (High-Fidelity)")
st.markdown("Kunci Detail Produk 100% Akurat untuk Menghindari Pelanggaran Komisi Affiliate.")
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

# 3. BACKEND AI ENGINE (STRICT PRODUCT LOCK RULES)
def generate_content_plan(prod_image, model_image):
    system_instruction = """
    You are an expert AI Fashion Director and strict E-commerce Compliance Officer for TikTok Shop and Shopee Video Affiliate.
    Your absolute priority is 100% PRODUCT FIDELITY. Misrepresenting garment details will cause seller policy violations.

    CRITICAL STEP FOR PRODUCT ANALYSIS:
    Before writing any prompt, zoom into the product outfit image and extract the exact physical specifications:
    1. Material & Texture: Is it shiny nylon, matte crinkle parachute fabric, fleece, or polyester?
    2. Front Closures: Full-zip, half-zip, pullover, buttoned? What color is the zipper track?
    3. Hood & Collar features: Are there drawstrings? What shape are the toggles/strings? (e.g., round black elastic strings with plastic tips).
    4. Cuffs & Hems: Are the wrist cuffs elasticated, ribbed, velcro-strapped, or open?
    5. Pockets: Are there zippered side pockets, kangaroo pockets, chest pockets?

    PROMPT GENERATION ENGINE INSTRUCTIONS (Output exactly 5 options):
    - 'judul': High-conversion Indonesian marketing hook title.
    - 'alur_cerita': 13-second chronological video flow breakdown (In Indonesian).
    - 'seedance_prompt': The video prompt for Seedance 2.0 / Nano Banana 2.

    STRICT RULES FOR 'seedance_prompt':
    - Must enforce: "13s duration, 9:16 vertical aspect ratio, seamless looping animation".
    - MUST accurately text-lock the model's ethnicity, hair, and facial structure from the model image.
    - DO NOT just write a generic jacket name. You MUST explicitly embed the extracted micro-details (e.g., 'wearing the exact matte black windproof crinkle nylon parachute jacket featuring a matching full-length black front zipper closure, an attached hood with visible black round elastic drawstrings, two zippered side hand pockets, and tight elasticated wrist cuffs') into the motion scenes. Every scene must maintain these exact specifications to lock the image-to-video consistency.
    - End with: "STRICT NEGATIVE: human, skin, text, words, letters, graphics, logos, choppy edits, music, bgm."

    OUTPUT FORMAT REQUIREMENT:
    Return response strictly as a raw JSON array containing exactly 5 objects with keys 'judul', 'alur_cerita', and 'seedance_prompt'. No markdown wrappers.
    """

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config={
            "temperature": 0.7, # Sedikit diturunkan agar AI lebih patuh pada detail gambar asli
            "response_mime_type": "application/json"
        },
        system_instruction=system_instruction
    )

    response = model.generate_content([
        "Strictly analyze all micro-hardware and cloth details of the product image. Combine it with the model face to build 5 high-fidelity JSON packages.",
        Image.open(prod_image),
        Image.open(model_image)
    ])
    
    return json.loads(response.text)

# 4. MAIN INTERACTION SCREEN
if not uploaded_product or not uploaded_model:
    st.info("💡 **Tips Android:** Klik tombol `>` di pojok kiri atas untuk upload foto baju & model wajah lo!")
else:
    if st.button("✨ Racik 5 Opsi Konten (Akurasi Tinggi)", type="primary", use_container_width=True):
        with st.spinner("🤖 AI sedang membedah kancing, sleting, dan tali produk secara mikro..."):
            try:
                results = generate_content_plan(uploaded_product, uploaded_model)
                st.session_state['mobile_content_results'] = results
                st.success("🎉 Sukses! Detail produk terkunci rapat di semua prompt.")
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")

# 5. DISPLAY RESULTS
if 'mobile_content_results' in st.session_state:
    st.markdown("---")
    st.markdown("### 📱 Hasil Rencana Konten Anti-Pelanggaran")
    
    for idx, item in enumerate(st.session_state['mobile_content_results'], start=1):
        with st.container(border=True):
            st.markdown(f"#### 🌟 OPSI {idx}: {item['judul']}")
            
            st.markdown("**🎬 Alur Cerita Video (13 Detik, 8 Fast-Cuts):**")
            st.info(item['alur_cerita'])
            
            st.markdown("**📋 Teks Prompt Seedance 2.0 (Gila Detail):**")
            st.code(item['seedance_prompt'], language="text")
