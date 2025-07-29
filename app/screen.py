# 📁 screen.py – Dashboard Home Screen for RecycleVision

import os
import streamlit as st
from PIL import Image
import base64

# ── Function to set background ──
def set_background(image_filename: str):
    img_path = os.path.join(os.path.dirname(__file__), "images", image_filename)
    if os.path.exists(img_path):
        with open(img_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
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
    else:
        st.warning("⚠️ Background image not found!")

# ── Main function to render dashboard ──
def show_dashboard():
    # Sidebar (st.sidebar used from parent)
    with st.sidebar:
        st.title("🧭 Navigation")
        if st.button("🏠 Home"):
            st.rerun()
        st.markdown("---")
        st.markdown("Welcome to **RecycleVision** Dashboard!")

    # Set background
    set_background("bg3.jpg")  # only filename, assuming 'images/' is within screen.py dir

    # Dashboard content
    st.markdown("""
        <div style="background-color: rgba(255,255,255,0.8); padding: 2rem; border-radius: 12px;">
            <h1 style="color:#2d572c;">📊 RecycleVision Dashboard</h1>
            <p>Track your eco-journey and view analytics from your recycling interactions!</p>
        </div>
    """, unsafe_allow_html=True)

    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="♻️ Items Recycled", value="248", delta="+12 this week")
    with col2:
        st.metric(label="🌍 CO₂ Saved", value="31.2 kg", delta="+2.3 kg")
    with col3:
        st.metric(label="🔥 Active Sessions", value="7")

    st.markdown("---")
    st.subheader("📈 Weekly Summary")
    st.line_chart([20, 30, 25, 40, 35, 50, 48])
