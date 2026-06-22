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
st.subheader("🚀 SEEDANCE 2.0 EDITION (Bandar Lampung Vibes)")
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

# 3. THE MAGIC REASONING ENGINE (GENDER, ALLURE, & LOCALIZATION LOCK)
def generate_king_prompts(prod_image, model_image):
    system_instruction = """
    You are the absolute master prompt engine for Seedance 2.0 and Nano Banana 2, personally tuned for KING KAELANJASM.
    Your priority is maximizing commercial conversion ("menjual") by maintaining high-end visual appeal, exact physical proportions, and an authentic Indonesian atmosphere.

    ULTRA-CRITICAL SILHOUETTE & GENDER LOCK:
    1. Scan the Model Image: Detect gender, facial aesthetics, and exact body silhouette. 
    2. Capture Body Allure: If the input model features a well-proportioned, curvaceous, stunning, or hourglass body shape, you MUST explicitly lock and translate this into the prompt text tokens. Do NOT default to a flat, overly skinny body description.
    3. Mandatory Gender Alignment: Ensure the outfit wraps perfectly around the model's actual gender as displayed in the input photo.

    STRICT INDONESIA & BANDAR LAMPUNG LOCALIZATION RULES:
    - EVERY background scene, angle, and location across all cuts MUST be grounded in authentic Indonesian vibes, specifically localized to Bandar Lampung.
    - Alternated beautifully between high-end INDOOR spaces and cinematic OUTDOOR settings.
    - Utilize hyper-specific local backdrops in the prompt descriptions, such as: modern minimalist cafes in Enggal, scenic outdoor lookouts overlooking Lampung bay, tropical city vibes of Pahoman, moody urban textures of Teluk Betung, or premium Indonesian photography studio setups.

    VARIATION VARIETY RULES (4 Genres):
    Output exactly 4 distinct genres (Casual Streetwear, Cyberpunk/Techwear, Luxury High-Fashion Editorial, High-Energy Athletic/Sport), sorted with the highest-converting, most stunning variation at Index 0.
    - Every option MUST use highly diverse camera angles across its 8 fast-cuts.

    JSON FORMAT OUTPUT:
    Return exactly 4 items in a clean, raw JSON array with keys: 'genre', 'judul', 'alur_cerita', and 'seedance_prompt'. Do not include markdown code block syntax.

    STRICT PROMPT TEMPLATE FOR 'seedance_prompt':
    Start with: "13s duration, 9:16 vertical aspect ratio, seamless looping animation, ultra-high-fidelity 8k commercial [GENRE_NAME] fashion videography, Indonesian cinematic style."
    Followed by: Microscopic description of the model's actual gender, face, and stunning curvaceous body silhouette wearing the product garment with its exact micro-hardware details perfectly fitted.
    Followed by: A seamless integration of 8 fast-cut cinematic movements changing angles while moving through realistic indoor and outdoor Bandar Lampung backdrops (e.g., pacing through a neon cafe in Enggal, walking along a sunny street in Pahoman).
    End with: "STRICT NEGATIVE: human, skin, text, words, letters, graphics, logos, choppy edits, music, bgm."
    """

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config={
            "temperature": 0.35, 
            "response_mime_type": "application/json"
        },
        system_instruction=system_instruction
    )

    response = model.generate_content([
        "Analyze both images. Lock the model's gorgeous body shape, apply strict Bandar Lampung indoor/outdoor background localization across all 8 cuts, and generate 4 high-conversion commercial prompts.",
        Image.open(prod_image),
        Image.open(model_image)
    ])
    
    return json.loads(response.text)

# 4. MAIN INTERACTION INTERFACE
if not uploaded_product or not uploaded_model:
    st.info("💡 **Panduan HP Android:** Tap tombol `>` di ujung kiri atas layar untuk meng-upload Foto Baju dan Foto Wajah Model Talent Anda!")
else:
    if st.button("👑 RACIK PROMPT KING KAELANJASM v2.0 👑", type="primary", use_container_width=True):
        with st.spinner("🧠 Mengunci lekuk tubuh model dan menyuntikkan vibes Bandar Lampung..."):
            try:
                results = generate_king_prompts(uploaded_product, uploaded_model)
                st.session_state['king_suite_outputs'] = results
                st.success("🎉 Sukses! 4 Genre Allure Khas Lampung Berhasil Diracik Sempurna!")
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
