# 📁 batch.py

import numpy as np
from PIL import Image
from app.waste import predict_waste
from app.info import waste_details

def process_batch_images(file_list, model=None):
    """Processes a list of uploaded or webcam-captured image files."""
    results = []

    if model is None:
        from app.waste import load_waste_model
        model = load_waste_model()

    for file in file_list:
        try:
            # 🧠 Determine source type
            if isinstance(file, Image.Image):  # From webcam
                image_pil = file
                filename = "webcam_image.png"
            else:  # From uploader
                image_pil = Image.open(file).convert("RGB")
                filename = file.name

            img_array = np.array(image_pil)
            label, confidence, emoji = predict_waste(img_array, model)

            info = waste_details.get(label, {})
            results.append({
                "filename": filename,
                "image": img_array,
                "class": label.capitalize(),
                "confidence": confidence,
                "emoji": emoji,
                "description": info.get("description", ""),
                "examples": info.get("examples", ""),
                "disposal": info.get("disposal", "")
            })

        except Exception as e:
            results.append({
                "filename": filename if 'filename' in locals() else "unknown",
                "image": None,
                "class": "Error",
                "confidence": 0.0,
                "emoji": "❌",
                "description": f"Could not process image: {e}"
            })

    return results
