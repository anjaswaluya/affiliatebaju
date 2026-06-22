import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

# 1. APP INITIALIZATION & BRANDING
st.set_page_config(
    page_title="PROMPT MAKER FROM KING KAELANJASM SEEDANCE 2.0 EDITION",
    page_icon="👑",
    layout="centered"
)

st.title("👑 PROMPT MAKER FROM KING KAELANJASM")
st.subheader("🚀 SEEDANCE 2.0 EDITION (Dual-Anchor Precision)")
st.markdown("---")

# Initialize Gemini API securely from Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ `GEMINI_API_KEY` tidak ditemukan di Streamlit Secrets.")
    st.stop()

# 2. MOBILE-FRIENDLY SIDEBAR ASSETS UPLOADER
st.sidebar.header("📁 Upload Center")

uploaded_product = st.sidebar.file_uploader(
    "1. Foto Produk (Semua Jenis Outfit)", 
    type=["png", "jpg", "jpeg"]
)
if uploaded_product:
    st.sidebar.image(Image.open(uploaded_product), caption="📦 Baju/Produk Terkunci", use_container_width=True)

uploaded_model = st.sidebar.file_uploader(
    "2. Foto Model / Wajah Talent", 
    type=["png", "jpg", "jpeg"]
)
if uploaded_model:
    st.sidebar.image(Image.open(uploaded_model), caption="👤 Talent Terkunci", use_container_width=True)

# 3. DUAL-ANCHOR PRECISION ENGINE
def generate_king_prompts(prod_image, model_image):
    system_instruction = """
    You are the absolute master prompt engine for Seedance 2.0 and Nano Banana 2, tuned for KING KAELANJASM.
    You must maintain 100% identical product matching and 100% exact model gender matching simultaneously.

    ANCHOR 1: ABSOLUTE GENDER & SILHOUETTE LOCK
    - Look ONLY at the human model image. Detect her exact visual gender (strictly Female/Woman if the photo shows a woman).
    - Maintain her stunning, curvaceous hourglass silhouette and confident commercial allure. 
    - NEVER use male terms ('pria', 'cowok', 'man') if the model is a woman.

    ANCHOR 2: 100% PRODUCT FIDELITY & PRINT LOCK
    - Look at the garment garment in the product image. 
    - Separate e-commerce UI text (ignore words like 'Pria' in the app banners) from the ACTUAL TEXT/GRAPHIC PRINTED ON THE CLOTHING.
    - You MUST identify and read the exact words, font style, and graphic elements printed directly on the fabric (e.g., if it says 'Brooklyn 1991', you MUST write 'Brooklyn 1991 text print on the chest' inside the prompt). Describe the fabric texture, seams, and fit with absolute clone-like precision.

    INDONESIA & BANDAR LAMPUNG LOCALIZATION:
    - Distribute 8 fast-cuts beautifully between high-end INDOOR spaces and cinematic OUTDOOR settings in Bandar Lampung (e.g., aesthetic cafe in Enggal, sunny streets of Pahoman, modern urban spots in Teluk Betung).

    OUTPUT SPECS (4 Genres):
    - Output exactly 4 distinct genres, sorted from highest-converting to lowest.
    - Deliver output in a raw JSON array with keys: 'genre', 'judul', 'alur_cerita', and 'seedance_prompt'. No markdown wrappers.
    """

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config={
            "temperature": 0.25, # Keseimbangan optimal untuk kepatuhan logika gembok ganda
            "response_mime_type": "application/json"
        },
        system_instruction=system_instruction
    )

    response = model.generate_content([
        "Perform deep dual-anchor analysis. Lock the model's visual female gender/hourglass shape. Read and clone the exact print text/graphics from the garment fabric. Generate 4 high-conversion prompts localized to Bandar Lampung.",
        Image.open(prod_image),
        Image.open(model_image)
    ])
    
    return json.loads(response.text)

# 4. MAIN INTERACTION INTERFACE
if not uploaded_product or not uploaded_model:
    st.info("💡 **Panduan HP Android:** Tap tombol `>` di ujung kiri atas layar untuk meng-upload Foto Baju dan Foto Wajah Model Talent Anda!")
else:
    if st.button("👑 RACIK PROMPT KING KAELANJASM v2.0 👑", type="primary", use_container_width=True):
        with st.spinner("🧠 Mengunci Presisi Sablon Produk & Sinkronisasi Gender Model..."):
            try:
                results = generate_king_prompts(uploaded_product, uploaded_model)
                st.session_state['king_suite_outputs'] = results
                st.success("🎉 Sukses! Produk 100% Kembar & Gender Terkunci Sempurna!")
            except Exception as e:
                st.error(f"Gagal memproses gambar. Error: {e}")

# 5. HIGH-END RESPONSIVE MOBILE DISPLAY
if 'king_suite_outputs' in st.session_state:
    st.write("---")
    st.markdown("### 📱 Rencana Konten 4 Genre Teratas (Vibes Bandar Lampung):")
    
    for idx, item in enumerate(st.session_state['king_suite_outputs'], start=1):
        with st.container(border=True):
            st.markdown(f"### 🔥 OPSI {idx} | Genre: {item['genre'].upper()}")
            st.markdown(f"**📌 Judul Iklan:** {item['judul']}")
            
            st.markdown("**🎬 Alur Cerita Video (13 Detik - 8 Dynamic Scenes Khas Indo):**")
            st.info(item['alur_cerita'])
            
            st.markdown("**📋 Teks Prompt Seedance 2.0 / Nano Banana 2:**")
            st.code(item['seedance_prompt'], language="text")
