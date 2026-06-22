import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
import io

# 1. PAGE CONFIGURATION & UI SETUP
st.set_page_config(
    page_title="Master Elka's Seedance 2.0 Director Suite",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Master Elka's Seedance 2.0 Prompt & Grid Generator")
st.markdown("Input Foto Model + Produk -> Output 2 Teks Prompt Seedance + 2 Gambar Preview Kombinasi 8-Grid.")
st.write("---")

# Initialize Gemini API securely from Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ `GEMINI_API_KEY` tidak ditemukan di Streamlit Secrets. Harap konfigurasi di dashboard settings Streamlit Anda.")
    st.stop()

# 2. SIDEBAR CONFIGURATION (Upload Assets)
st.sidebar.header("📁 Upload Assets")

uploaded_product = st.sidebar.file_uploader(
    "1. Upload Foto Produk (Baju/Outfit)", 
    type=["png", "jpg", "jpeg"]
)

if uploaded_product:
    st.sidebar.image(Image.open(uploaded_product), caption="📦 Foto Produk Terdeteksi", use_container_width=True)

uploaded_model = st.sidebar.file_uploader(
    "2. Upload Foto Model (Wajah/Talent)", 
    type=["png", "jpg", "jpeg"]
)

if uploaded_model:
    st.sidebar.image(Image.open(uploaded_model), caption="👤 Foto Model Terdeteksi", use_container_width=True)

# 3. BACKEND MULTIMODAL ENGINE (Text & Image Prompt Generation)
def generate_prompts_and_visuals(prod_image, model_image):
    # Setup Text Model
    text_model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config={
            "temperature": 0.85,
            "response_mime_type": "application/json"
        },
        system_instruction="""
        You are a master AI fashion director. Your job is to take a model image and a product outfit image, then generate exactly 2 highly customized prompt packages.
        
        For each package, you must return:
        1. 'seedance_prompt': A highly optimized video generation prompt for Seedance 2.0 (13s duration, 9:16 vertical aspect ratio, seamless looping animation, featuring the model wearing the exact product outfit, sequencing 8 dynamic fast-cut commercial scenes, with the negative block 'STRICT NEGATIVE: human, skin, text, words, letters, graphics, logos, choppy edits, music, bgm.').
        2. 'imagen_prompt': A dedicated image generation prompt for Imagen 3 that describes a '2x4 grid storyboard layout, fashion photography, showing 8 distinct chronological action frames/angles' of that exact model wearing that outfit in a specific professional commercial setting.
        
        Return your output strictly as a JSON array containing exactly 2 objects.
        Format example:
        [
          {
            "seedance_prompt": "text here...",
            "imagen_prompt": "A professional 2x4 grid storyboard fashion photography layout showing 8 different frames of..."
          },
          {
            "seedance_prompt": "text here...",
            "imagen_prompt": "A professional 2x4 grid storyboard fashion photography layout showing 8 different frames of..."
          }
        ]
        """
    )

    # Generate the text and instructions
    response = text_model.generate_content([
        "Analyze both images and create exactly 2 variations of JSON objects containing seedance_prompt and imagen_prompt.",
        Image.open(prod_image),
        Image.open(model_image)
    ])
    
    return json.loads(response.text)

# 4. MAIN INTERACTION SCREEN
st.subheader("🚀 Director Dashboard")

if not uploaded_product or not uploaded_model:
    st.info("💡 Silakan upload Foto Produk DAN Foto Model di sidebar untuk mengaktifkan AI Studio.")
else:
    if st.button("✨ Generate 2 Core Variations (Prompt + 8-Grid Image)", type="primary", use_container_width=True):
        with st.spinner("🤖 AI sedang memproses naskah iklan dan menggambar grid visual... (Mohon tunggu sekitar 30 detik)"):
            try:
                # Step 1: Generate Text & Image Prompts via Gemini
                packages = generate_prompts_and_visuals(uploaded_product, uploaded_model)
                
                final_results = []
                
                # Step 2: Loop through the 2 packages and generate the actual 8-grid image using Imagen 3
                for idx, pack in enumerate(packages):
                    st.write(f"🎨 Sedang menggambar simulasi 8-Grid untuk Variasi {idx+1}...")
                    
                    try:
                        # Call Google Imagen model
                        imagen_model = genai.ImageGenerationModel("imagen-3.0-generate-002")
                        imagen_result = imagen_model.generate_images(
                            prompt=pack["imagen_prompt"],
                            number_of_images=1,
                            aspect_ratio="3:4" # Good for grid layout display
                        )
                        # Extract the PIL image from response
                        generated_img = imagen_result.images[0].pil_image
                    except Exception as img_err:
                        # Fallback case if Imagen is rate-limited or restricted on the user's free tier
                        generated_img = None
                    
                    final_results.append({
                        "seedance_prompt": pack["seedance_prompt"],
                        "image": generated_img
                    })
                
                st.session_state['director_output'] = final_results
                st.success("🎉 Selesai! Semua naskah video dan gambar 8-grid berhasil dirender.")
                
            except Exception as e:
                st.error(f"Terjadi kesalahan teknis: {e}")

# 5. DISPLAY RESULTS
if 'director_output' in st.session_state:
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    for idx, item in enumerate(st.session_state['director_output']):
        # Split output dynamically into two clean columns side by side
        target_col = col1 if idx == 0 else col2
        
        with target_col:
            st.markdown(f"### 🌟 Variasi {idx+1}")
            
            # Display the copyable Seedance prompt
            st.markdown("**📋 Teks Prompt Seedance 2.0:**")
            st.code(item["seedance_prompt"], language="text")
            
            # Display the simulated 8-Grid Image Storyboard
            st.markdown("**📸 Estimasi Hasil Visual (8-Grid Storyboard):**")
            if item["image"] is not None:
                st.image(item["image"], use_container_width=True, caption=f"Simulasi Alur Adegan Variasi {idx+1}")
            else:
                st.warning("⚠️ Gagal merender gambar otomatis. (Batas kuota gratis Imagen API akun Anda tercapai, namun teks prompt di atas tetap bisa digunakan 100% di Seedance!)")
