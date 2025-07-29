# 📁 utils/openrouter_client.py

import os
import httpx
from dotenv import load_dotenv

import os
import sys

# ✅ Fix path so 'utils' can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://recycle-vision-by-hassan.streamlit.app/",  # replace with your app URL if deployed
    "X-Title": "RecycleBot",
}

def chat_with_openrouter(message, model="qwen/qwen3-14b:free"):
    body = {
        "model": model,
        "messages": [{"role": "user", "content": message}],
        "temperature": 0.7,
    }

    try:
        response = httpx.post(BASE_URL, headers=HEADERS, json=body)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except httpx.RequestError as e:
        return f"⚠️ Network error: {e}"
    except Exception as e:
        return f"❌ API error: {e}"
