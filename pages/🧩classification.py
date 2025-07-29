import streamlit as st
import numpy as np
from PIL import Image
import os, json, sys

# 🔧 Path fix for multi-page import
current_dir = os.path.dirname(os.path.abspath(__file__))         # pages/
project_root = os.path.abspath(os.path.join(current_dir, ".."))  # root
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.waste import load_waste_model, predict_waste
from app.info import waste_details
from app.batch import process_batch_images

@st.cache_resource
def get_model():
    return load_waste_model()

model = get_model()

@st.cache_data
def load_class_display():
    label_map_path = os.path.join("model", "label_map.json")
    if os.path.exists(label_map_path):
        with open(label_map_path) as f:
            return {v: k for k, v in json.load(f).items()}
    return {}

class_display = load_class_display()

# 🧠 Session Init
if "total_predictions" not in st.session_state:
    st.session_state.total_predictions = 0
if "class_counts" not in st.session_state:
    st.session_state.class_counts = {}
if "classify_count" not in st.session_state:
    st.session_state.classify_count = 0

def track_prediction(label):
    st.session_state.total_predictions += 1
    st.session_state.classify_count += 1  # 👈 Realtime update for dashboard
    label = label.lower()
    if label not in st.session_state.class_counts:
        st.session_state.class_counts[label] = 1
    else:
        st.session_state.class_counts[label] += 1

def display_prediction(img_array):
    label, confidence, emoji = predict_waste(img_array, model)
    track_prediction(label)
    st.success(f"**Prediction:** {label.capitalize()} {emoji}")
    st.info(f"**Confidence:** {confidence:.2%}")
    if label in waste_details:
        info = waste_details[label]
        st.markdown(f"**Description:** {info['description']}")
        st.markdown(f"**Examples:** {info['examples']}")
        st.markdown(f"**Disposal:** {info['disposal']}")
    else:
        st.warning("No info found for this category.")

def show_classifier():
    st.title("🚮 Smart Waste Classifier")
    st.markdown("Let AI detect and describe waste categories for better recycling. 🌍")

    with st.expander("📈 Classification Stats", expanded=False):
        st.write(f"**Total Predictions:** {st.session_state.total_predictions}")
        for category, count in st.session_state.class_counts.items():
            st.write(f"🔹 **{category.capitalize()}**: {count}")

    mode = st.selectbox("Choose Mode:", ["Single Mode", "Batch Mode"])
    input_method = st.selectbox(
        "Input Source:",
        ["Upload Image", "Use Webcam"] if mode == "Single Mode" else ["Upload Images", "Use Webcam"]
    )

    if mode == "Batch Mode" and input_method == "Use Webcam":
        batch_count = st.number_input("📸 Capture Count", min_value=2, max_value=5, value=2)

    if mode == "Single Mode":
        if input_method == "Upload Image":
            uploaded = st.file_uploader("📤 Upload a waste image", type=["jpg", "jpeg", "png"])
            if uploaded:
                image_pil = Image.open(uploaded).convert("RGB")
                img_array = np.array(image_pil)
                st.image(img_array, caption="Uploaded Image", use_container_width=True)
                if st.button("🚀 Classify Waste"):
                    with st.spinner("Analyzing..."):
                        display_prediction(img_array)
        elif input_method == "Use Webcam":
            camera_image = st.camera_input("📷 Capture image")
            if camera_image:
                image_pil = Image.open(camera_image).convert("RGB")
                img_array = np.array(image_pil)
                st.image(img_array, caption="Captured Image", use_container_width=True)
                if st.button("🚀 Classify Waste"):
                    with st.spinner("Analyzing..."):
                        display_prediction(img_array)

    elif mode == "Batch Mode":
        images = []
        if input_method == "Upload Images":
            files = st.file_uploader("📁 Upload multiple images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
            if files:
                images = [Image.open(f).convert("RGB") for f in files]
        elif input_method == "Use Webcam":
            for i in range(int(batch_count)):
                snap = st.camera_input(f"📸 Capture image {i+1}")
                if snap:
                    images.append(Image.open(snap).convert("RGB"))

        if images:
            st.info(f"🧪 Processing {len(images)} images...")
            results = process_batch_images(images)
            for res in results:
                st.image(res["image"], caption=res.get("filename", "Image"), use_container_width=True)
                st.success(f"Prediction: {res['class']} {res['emoji']}")
                st.info(f"Confidence: {res['confidence']:.2%}")
                track_prediction(res['class'])
                if "description" in res:
                    st.markdown(f"**Description:** {res['description']}")
                    st.markdown(f"**Examples:** {res['examples']}")
                    st.markdown(f"**Disposal:** {res['disposal']}")

# 🚀 Render the Classifier
show_classifier()
