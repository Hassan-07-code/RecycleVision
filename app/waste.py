import os
import numpy as np
import cv2
import json
from tensorflow.keras.models import load_model #type: ignore

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "waste_model.keras")
LABEL_MAP_PATH = os.path.join(os.path.dirname(MODEL_PATH), "label_map.json")

# --- Load Class Names Dynamically ---
if os.path.exists(LABEL_MAP_PATH):
    with open(LABEL_MAP_PATH, "r") as f:
        label_map = json.load(f)
    # Sort labels by index to guarantee correct order for model output
    CLASS_NAMES = [k for k, v in sorted(label_map.items(), key=lambda item: item[1])]
else:
    # Fallback: hardcoded, may need update if classes change
    CLASS_NAMES = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

EMOJIS = {
    'cardboard': '📦',
    'glass': '🧃',
    'metal': '🥫',
    'paper': '📰',
    'plastic': '🧴',
    'trash': '❌',
}

# --- Efficient Model Loader (with cache for Streamlit) ---
_model_cache = {}

def load_waste_model():
    global _model_cache
    if "model" not in _model_cache:
        _model_cache["model"] = load_model(MODEL_PATH)
    return _model_cache["model"]

# --- Waste Prediction with Robust Error Handling ---
def predict_waste(img, model):
    # Preprocess: resize to match model input, normalize
    img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_LANCZOS4)
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)

    # Safely predict
    preds = model.predict(img)
    if preds.shape[1] != len(CLASS_NAMES):
        raise ValueError(
            f"Prediction size {preds.shape[1]} does not match number of class labels {len(CLASS_NAMES)}. "
            "Check your label_map.json and dataset folders."
        )
    class_idx = int(np.argmax(preds[0]))
    class_name = CLASS_NAMES[class_idx]
    confidence = float(preds[0][class_idx])
    emoji = EMOJIS.get(class_name, '')

    return class_name, confidence, emoji
