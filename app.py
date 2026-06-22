import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

# 1. PAGE CONFIGURATION & MOBILE OPTIMIZED UI
st.set_page_config(
    page_title="Master Elka's Seedance Suite",
    page_icon="🎬",
    layout="centered" # Menggunakan 'centered' agar pas dan proporsional saat dibuka di layar HP
)

st.title("🎬 Seedance 2.0 Content Planner")
st.markdown("Gabungkan Foto Model + Produk untuk menghasilkan **Judul, Alur Cerita (13 detik), dan Prompt Video**.")
st.write("---")

# Initialize Gemini API securely from Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ `GEMINI_API_KEY` tidak ditemukan di Streamlit Secrets. Harap isi terlebih dahulu di dashboard Streamlit Anda.")
    st.stop()

# 2. SIDEBAR CONFIGURATION (Upload Tempat Aset)
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

# 3. BACKEND AI ENGINE (5 OPSI - JUDUL, ALUR, PROMPT)
def generate_content_plan(prod_image, model_image):
    system_instruction = """
    You are an expert AI Fashion Director and TikTok/Shorts Affiliate Marketing Expert.
    You will analyze two images: a model image and a product outfit image.
    Your job is to output exactly 5 unique, high-conversion commercial video asset plans.

    For each of the 5 options, you must generate:
    1. 'judul': A catchy, clickbait, or high-hook marketing title tailored for Indonesian fashion commercial/affiliate content (In Indonesian).
    2. 'alur_cerita': A clear, chronological 13-second timestamped breakdown of exactly 8 fast-cut dynamic scenes showing how the video flows (In Indonesian). Example: '00:00-00:02: Scene 1... | 00:02-00:03: Scene 2...'.
    3. 'seedance_prompt': The exact text prompt optimized for Seedance 2.0 (Must strictly follow: 13s duration, 9:16 vertical aspect ratio, seamless looping animation, description of the model from the image wearing the exact outfit from the product image, sequencing 8 dynamic commercial cuts smoothly, ending with 'STRICT NEGATIVE: human, skin, text, words, letters, graphics, logos, choppy edits, music, bgm.').

    OUTPUT FORMAT REQUIREMENT:
    Return your response strictly as a raw JSON array containing exactly 5 objects with keys 'judul', 'alur_cerita', and 'seedance_prompt'. Do not wrap it in ```json blocks.
    Format example:
    [
      {
        "judul": "Judul Disini",
        "alur_cerita": "Detail Alur Disini",
        "seedance_prompt": "Prompt Seedance Disini"
      }
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

    response = model.generate_content([
        "Analyze the provided model and product images to generate exactly 5 distinct JSON packages containing 'judul', 'alur_cerita', and 'seedance_prompt' inside an array.",
        Image.open(prod_image),
        Image.open(model_image)
    ])
    
    return json.loads(response.text)

# 4. MAIN INTERACTION SCREEN (Mobile Friendly Layout)
if not uploaded_product or not uploaded_model:
    st.info("💡 **Tips HP Android:** Klik tombol ikon `>` di pojok kiri atas layar HP lo untuk membuka menu upload foto Produk & Model!")
else:
    if st.button("✨ Racik 5 Opsi Konten Sekarang", type="primary", use_container_width=True):
        with st.spinner("🤖 AI Gemini sedang menyusun strategi konten dan menulis prompt..."):
            try:
                results = generate_content_plan(uploaded_product, uploaded_model)
                st.session_state['mobile_content_results'] = results
                st.success("🎉 Berhasil meracik 5 Opsi Konten Premium!")
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")

# 5. DISPLAY RESULTS AS MOBILE CARDS
if 'mobile_content_results' in st.session_state:
    st.markdown("---")
    st.markdown("### 📱 Hasil Rencana Konten (Tinggal Copas)")
    
    for idx, item in enumerate(st.session_state['mobile_content_results'], start=1):
        # Menggunakan container berbayang/berborder agar rapi seperti kartu aplikasi di HP
        with st.container(border=True):
            st.markdown(f"#### 🌟 OPSI {idx}: {item['judul']}")
            
            # Alur Cerita Box
            st.markdown("**🎬 Alur Cerita Video (13 Detik, 8 Fast-Cuts):**")
            st.info(item['alur_cerita'])
            
            # Prompt Box (Satu ketukan di HP langsung tersalin semua kodenya)
            st.markdown("**📋 Teks Prompt Seedance 2.0:**")
            st.code(item['seedance_prompt'], language="text")
