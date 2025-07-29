# 📁 pages/home.py

import streamlit as st
import os
import base64

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

st.set_page_config(page_title="🏠 Home - RecycleVision", layout="centered")
# set_background("bg5.jpg")

# 💾 Initialize tracking session states if not already set
if "chat_count" not in st.session_state:
    st.session_state.chat_count = 0
if "classify_count" not in st.session_state:
    st.session_state.classify_count = 0
if "active_sessions" not in st.session_state:
    st.session_state.active_sessions = 1  # start with 1 session per user

st.markdown("""
    <div style="background-color: rgba(0, 0, 0, 0); padding: 2rem; border-radius: 12px;">
        <h1 style="color:#2d572c;">📊 RecycleVision Dashboard</h1>
        <p>Track your eco-journey and view analytics from your recycling interactions!</p>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🧪 Waste Classifications", f"{st.session_state.classify_count}", "+1 per classify")
with col2:
    st.metric("🗨️ Chatbot Questions", f"{st.session_state.chat_count}", "+1 per chat")
with col3:
    st.metric("🔥 Active Session", f"{st.session_state.active_sessions}")

# Removed the chart
# st.subheader("📈 Weekly Summary")
# st.line_chart([20, 30, 25, 40, 35, 50, 48])
