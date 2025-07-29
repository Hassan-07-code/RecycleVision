# ♻️ RecycleVision: Smart Waste Classifier & Eco Chatbot

**RecycleVision** is an AI-powered Streamlit app that helps users identify types of waste (e.g., plastic, metal, cardboard) and get eco-friendly disposal instructions. It also features a floating chatbot assistant for sustainability tips and recycling guidance — all in a sleek, mobile-ready UI.

---

## 🚀 Features

✅ **Smart Waste Classification**  
→ Detect waste type from single image, webcam, or batch upload using a MobileNetV2 model.

✅ **Eco-Assistant Chatbot**  
→ Floating WhatsApp-style chatbot powered by OpenRouter's LLM, offering recycling tips and weather-aware disposal advice.

✅ **Real-Time Webcam Mode**  
→ Supports capturing waste via camera for immediate classification.

✅ **Batch Mode Support**  
→ Classify multiple images at once with full label/emoji overlays and tracking.

✅ **Dashboard Tracking**  
→ View number of predictions, class frequency, and eco-stats on the home screen.

✅ **Custom Styling**  
→ A vibrant, mysterious-themed UI with animations, read receipts, and responsive layout.

---

## 🧠 Tech Stack

| Layer       | Technology                         |
|-------------|------------------------------------|
| Frontend    | Streamlit                          |
| Backend     | Python, NumPy, Pillow              |
| ML Model    | MobileNetV2 (TensorFlow / Keras)   |
| LLM API     | OpenRouter (e.g., GPT-4.1)         |
| Deployment  | Streamlit Cloud                    |
| Chat Styling| Custom CSS + JS injection          |

---

## 📁 Folder Structure

RecycleVision/
├── app/
│ ├── chat_bot.py # LLM logic via OpenRouter
│ ├── batch.py # Batch image classification
│ ├── info.py # Waste info data
│ ├── utils.py # Utilities for chat
│ └── waste.py # Model loading & prediction
├── model/
│ └── label_map.json # Label mapping for MobileNetV2
├── pages/
│ ├── Home.py # Dashboard screen
│ └── classification.py # Waste classification UI
├── images/
│ └── bg5.jpg # Background for Home
├── main.py # Root Streamlit app with chatbot
├── requirements.txt # Dependencies
└── README.md # You're reading it :

