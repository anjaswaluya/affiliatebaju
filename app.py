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
st.subheader("🚀 SEEDANCE 2.0 EDITION (Absolute Gender Lock)")
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

# 3. THE ULTRA REASONING ENGINE (GENDER BLINDFOLD & LOCALIZATION LOCK)
def generate_king_prompts(prod_image, model_image):
    system_instruction = """
    You are the absolute master prompt engine for Seedance 2.0 and Nano Banana 2, personally tuned for KING KAELANJASM.
    Your absolute number one priority is to match the exact visual gender of the human model image.

    THE ABSOLUTE GENDER BLINDFOLD RULE (ANTI-HALLUCINATION):
    1. IGNORE ALL TEXT INSIDE THE PRODUCT IMAGE. The product image is an e-commerce screenshot that may contain words like 'PRIA', 'MEN', 'COWOK', or 'SINGLET PRIA'. YOU MUST COMPLETELY BLIND YOURSELF TO THESE WORDS. Do NOT use them to determine gender.
    2. LOOK ONLY AT THE SECOND IMAGE (MODEL IMAGE): Identify if the human talent is FEMALE or MALE based ONLY on visual inspection of their face and body.
    3. IF THE MODEL IS FEMALE: The entire output inside 'alur_cerita' MUST strictly use female references ('model wanita', 'perempuan', 'cewek'). The 'seedance_prompt' MUST strictly use female tokens ('an alluring female model', 'beautiful woman', 'stunning female silhouette'). NEVER use the words 'male', 'man', 'pria', or 'cowok' anywhere in the output if the model is a woman.

    STREET/STUDIO BANDAR LAMPUNG LOCALIZATION:
    - Alternated beautifully between high-end INDOOR spaces and cinematic OUTDOOR settings in Bandar Lampung across 8 cuts (e.g., modern aesthetic cafe in Enggal, sunny street scene in Pahoman, moody urban vibes in Teluk Betung).

    VARIATION VARIETY RULES (4 Genres):
    Output exactly 4 distinct genres (Casual Streetwear, Cyberpunk/Techwear, Luxury High-Fashion Editorial, High-Energy Athletic/Sport), sorted with the highest-converting variation at Index 0.

    JSON FORMAT OUTPUT:
    Return exactly 4 items in a clean, raw JSON array with keys: 'genre', 'judul', 'alur_cerita', and 'seedance_prompt'. Do not include markdown code block syntax.
    """

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config={
            "temperature": 0.2, # Diturunkan super ekstrem ke 0.2 agar AI patuh total pada perintah gembok gender dan tidak berimprovisasi
            "response_mime_type": "application/json"
        },
        system_instruction=system_instruction
    )

    response = model.generate_content([
        "CRITICAL: Visually inspect the model image. Blind yourself to any text in the product image. Force the model's actual visual gender into all 4 high-conversion localized Bandar Lampung prompts.",
        Image.open(prod_image),
        Image.open(model_image)
    ])
    
    return json.loads(response.text)

# 4. MAIN INTERACTION INTERFACE
if not uploaded_product or not uploaded_model:
    st.info("💡 **Panduan HP Android:** Tap tombol `>` di ujung kiri atas layar untuk meng-upload Foto Baju dan Foto Wajah Model Talent Anda!")
else:
    if st.button("👑 RACIK PROMPT KING KAELANJASM v2.0 👑", type="primary", use_container_width=True):
        with st.spinner("🧠 Menjalankan Gembok Gender Absolut & Menyuntikkan Vibes Lampung..."):
            try:
                results = generate_king_prompts(uploaded_product, uploaded_model)
                st.session_state['king_suite_outputs'] = results
                st.success("🎉 Sukses! 4 Genre Allure Cewek Khas Lampung Berhasil Diracik Sempurna!")
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
