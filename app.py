import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

# 1. APP INITIALIZATION & BRANDING
st.set_page_config(
    page_title="PROMPT MAKER FROM KING KAELANJASM SEEDANCE 2.0 EDITION",
    page_icon="👑",
    layout="centered" # Tetap centered agar layout padat dan rapi saat di-scroll di Android
)

st.title("👑 PROMPT MAKER FROM KING KAELANJASM")
st.subheader("🚀 SEEDANCE 2.0 EDITION")
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

# 3. THE MAGIC REASONING ENGINE (ANTI GENDER-MISMATCH)
def generate_king_prompts(prod_image, model_image):
    system_instruction = """
    You are the absolute master prompt engine for Seedance 2.0 and Nano Banana 2, personally tuned for KING KAELANJASM.
    Your main task is to create 4 distinct genre variations, perfectly blending a model image and a product garment image with zero errors.

    ULTRA-CRITICAL BRAIN STEP (GENDER & OUTFIT LOCK):
    1. Scan the Model Image: Determine the exact gender (Male or Female), ethnicity, facial features, and hair structure. 
    2. Scan the Product Image: Analyze the garment type, fit, micro-details (zippers, drawstrings, fabrics, logos).
    3. Mandatory Alignment: You must NEVER change the gender of the model. If the model image is a Female, the generated video character MUST be strictly a woman/female, even if the garment text or tags say 'Pria/Men'. The garment must adapt to the model's actual gender and body structure in the scene.

    VARIATION VARIETY RULES:
    You must output exactly 4 options representing 4 completely different filmmaking genres (e.g., Casual Streetwear, Cyberpunk/Techwear, Luxury High-Fashion Editorial, High-Energy Athletic/Sport).
    - Every option MUST use completely different camera angles (e.g., extreme close-up, low-angle tracking, wide panoramic cinematic shot).
    - Every option MUST take place in completely different settings and lighting conditions (e.g., neon-lit rainy Tokyo streets, bright sun-drenched minimalist studio, moody urban concrete warehouse).
    - Order of presentation: Always sort the array from the absolute highest-converting, most visually striking integration style at the very top (Index 0).

    JSON FORMAT OUTPUT:
    Return exactly 4 items in a clean, raw JSON array with keys: 'genre', 'judul', 'alur_cerita', and 'seedance_prompt'. Do not include markdown code block syntax.

    STRICT PROMPT TEMPLATE FOR 'seedance_prompt':
    Start with: "13s duration, 9:16 vertical aspect ratio, seamless looping animation, ultra-high-fidelity 8k commercial [GENRE_NAME] videography."
    Followed by: Extreme detailed description of the model's actual gender/face from the image wearing the product garment with its microscopic hardware (zippers, drawstrings, exact textures).
    Followed by: A sequence of 8 fast-cut cinematic movements showing varied camera lenses, lightning systems, and high-end scene placements.
    End with: "STRICT NEGATIVE: human, skin, text, words, letters, graphics, logos, choppy edits, music, bgm."
    """

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config={
            "temperature": 0.3, # Diturunkan ke 0.3 agar tingkat kecerdasan dan kepatuhan analitis mencapai titik maksimal
            "response_mime_type": "application/json"
        },
        system_instruction=system_instruction
    )

    response = model.generate_content([
        "Analyze both images. Lock the model's actual gender, map the product garment perfectly, and generate 4 diverse genre-based JSON objects sorted by best output.",
        Image.open(prod_image),
        Image.open(model_image)
    ])
    
    return json.loads(response.text)

# 4. MAIN INTERACTION INTERFACE
if not uploaded_product or not uploaded_model:
    st.info("💡 **Panduan HP Android:** Tap tombol `>` di ujung kiri atas layar untuk meng-upload Foto Baju dan Foto Wajah Model Talent Anda!")
else:
    if st.button("👑 RACIK PROMPT KING KAELANJASM v2.0 👑", type="primary", use_container_width=True):
        with st.spinner("🧠 Sistem Ajaib sedang mencocokkan anatomi gender dan mengunci micro-detail produk..."):
            try:
                results = generate_king_prompts(uploaded_product, uploaded_model)
                st.session_state['king_suite_outputs'] = results
                st.success("🎉 Sukses! 4 Genre Premium Berhasil Diracik Sempurna!")
            except Exception as e:
                st.error(f"Gagal memproses gambar, pastikan format benar. Error: {e}")

# 5. HIGH-END RESPONSIVE MOBILE DISPLAY
if 'king_suite_outputs' in st.session_state:
    st.write("---")
    st.markdown("### 📱 Rencana Konten 4 Genre Teratas (Urutan Terbaik):")
    
    for idx, item in enumerate(st.session_state['king_suite_outputs'], start=1):
        with st.container(border=True):
            # Menampilkan tag nomor urut dan genre dengan format tebal menonjol
            st.markdown(f"### 🔥 OPSI {idx} | Genre: {item['genre'].upper()}")
            st.markdown(f"**📌 Judul Iklan:** {item['judul']}")
            
            # Box Alur Cerita Berwarna Biru Kontras
            st.markdown("**🎬 Alur Cerita Video (13 Detik - 8 Dynamic Scenes):**")
            st.info(item['alur_cerita'])
            
            # Box Copy Prompt Instan Sekali Tap
            st.markdown("**📋 Teks Prompt Seedance 2.0 / Nano Banana 2:**")
            st.code(item['seedance_prompt'], language="text")
