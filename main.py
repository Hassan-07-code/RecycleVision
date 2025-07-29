import streamlit as st
import os
import sys
import base64

# --- Page Config ---
st.set_page_config(page_title="♻️ RecycleVision", layout="wide", initial_sidebar_state="expanded")

# --- Sidebar ---
with st.sidebar:
    st.image("images/logo.png", width=80)
    st.title("♻️ RecycleVision")
    st.markdown("---")  # Optional divider above built-in page navigation

# Ensure the parent dir is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def set_background(image_filename: str):
    path = os.path.join("images", image_filename)
    if os.path.exists(path):
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <style>
                .stApp {{
                    background-image: url("data:image/jpeg;base64,{encoded}");
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                }}
            </style>
        """, unsafe_allow_html=True)

set_background("bg4.jpg")  # Set the background image

# --- Session State Setup ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Main Landing Content ---
st.title("♻️ Welcome to RecycleVision")
st.markdown("""
– Your smart assistant for eco-friendly waste management.  
Identify, classify, and learn about waste using AI-powered tools — all in one place.
- 🧠 Waste Classifier
- ☠ Mysterious
- 🏠 Home Dashboard
""")
st.subheader("For proper understanding, see this video:")
st.video("https://youtu.be/qSI22-A8dMA?si=cErqZPcqkVMBHAGS")  # video introduction

# st.image("assets/banner.jpg", use_column_width=True)  # Optional visual
