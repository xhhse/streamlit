import streamlit as st
import sys
import torch
from transformers import pipeline
import os

# -------------------------------
# Dependency Check
# -------------------------------
def check_package(pkg_name, install_hint=""):
    try:
        __import__(pkg_name)
        return True
    except ImportError:
        st.error(f"⚠️ Package {pkg_name} is not installed. Suggested command: {install_hint}")
        return False

deps_ok = True
deps_ok &= check_package("torch", "pip install torch")
deps_ok &= check_package("transformers", "pip install transformers")
deps_ok &= check_package("sentencepiece", "pip install sentencepiece")
deps_ok &= check_package("sacremoses", "pip install sacremoses")
deps_ok &= check_package("huggingface_hub", "pip install 'huggingface_hub[hf_xet]'")

# stop app if dependencies are missing
if not deps_ok:
    st.stop()

# -------------------------------
# Streamlit Page Setup
# -------------------------------
st.set_page_config(
    page_title="English → Chinese Translator",
    page_icon="🌐",
    layout="centered"
)

st.title("🌐 English → Chinese Translator")
st.markdown("""
- Translate text input directly  
- Upload an English `.txt` file to translate and download the Chinese version
""")
st.markdown(f"Device: {'GPU' if torch.cuda.is_available() else 'CPU'}")

# -------------------------------
# Load translation pipeline
# -------------------------------
@st.cache_resource(show_spinner=False)
def load_translator():
    device = 0 if torch.cuda.is_available() else -1
    return pipeline(
        "translation_en_to_zh",
        model="Helsinki-NLP/opus-mt-en-zh",
        device=device
    )

translator = load_translator()

# -------------------------------
# Text Input Translation
# -------------------------------
st.subheader("Text Translation")
input_text = st.text_area("Enter English text here:", height=150)

if st.button("Translate Text"):
    if not input_text.strip():
        st.warning("⚠️ Please enter some text.")
    else:
        try:
            result = translator(input_text.strip(), max_length=200)[0]['translation_text']
            st.success("👉 Chinese Translation:")
            st.write(result)
        except Exception as e:
            st.error(f"❌ Translation failed: {e}")

# -------------------------------
# File Upload Translation
# -------------------------------
st.subheader("File Translation (.txt)")
uploaded_file = st.file_uploader("Upload an English .txt file", type=["txt"])

if uploaded_file is not None:
    try:
        text_content = uploaded_file.read().decode("utf-8")
        st.text_area("File content preview", text_content, height=200)

        if st.button("Translate File"):
            translated_text = translator(text_content, max_length=10000)[0]['translation_text']

            st.success("✅ File translation completed")
            st.text_area("Translated content", translated_text, height=200)

            # Download translated file
            st.download_button(
                label="Download Chinese File",
                data=translated_text,
                file_name=os.path.splitext(uploaded_file.name)[0] + "_zh.txt",
                mime="text/plain"
            )

    except Exception as e:
        st.error(f"❌ File read or translation failed: {e}")