# 📁 pages/chat_bot.py

import os
import sys
import streamlit as st

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from rest.openrouter_client import chat_with_openrouter

# Chat logic
def generate_response(user_input):
    if not user_input.strip():
        return "⚠️ Please enter a valid question."

    try:
        response = chat_with_openrouter(user_input)
        
        # ✅ Increment chat count
        if "chat_count" not in st.session_state:
            st.session_state.chat_count = 0
        st.session_state.chat_count += 1

        return response or "🤔 Hmm... I couldn't figure that out. Try rephrasing!"
    except Exception as e:
        return f"⚠️ API Error: {str(e)}"

# Chat UI – this runs automatically
st.set_page_config(page_title="☠ Mysterious", layout="centered")
st.title("☠ Mysterious")
st.caption("Ask about ♻️recycling, sustainability, or anything else!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here...")
    send = st.form_submit_button("Send")

    if send and user_input.strip():
        st.session_state.chat_history.append(("user", user_input.strip()))
        reply = generate_response(user_input)
        st.session_state.chat_history.append(("bot", reply))
        st.rerun()

# Display messages
for sender, msg in st.session_state.chat_history:
    align = "flex-end" if sender == "user" else "flex-start"
    color = "#1a9909" if sender == "user" else "#115811"
    st.markdown(f"""
        <div style='display: flex; justify-content: {align}; margin: 6px 0;'>
            <div style='background-color: {color}; color: white; padding: 10px 16px;
                        border-radius: 16px; max-width: 75%;'>
                {msg}
            </div>
        </div>
    """, unsafe_allow_html=True)
