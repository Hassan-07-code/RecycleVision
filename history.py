import json
import os
import csv
from datetime import datetime

# Path to the JSON history file
HISTORY_FILE = "history.json"

# ─── Log Prediction to JSON ───
def log_prediction(label, confidence):
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "prediction": label,
        "confidence": round(confidence * 100, 2)  # store as percentage
    }

    # Load existing history or start fresh
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                data = json.load(f)
                if isinstance(data, list):
                    history = data
        except json.JSONDecodeError:
            history = []

    # Append new entry and save
    history.append(entry)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

# ─── Export History to CSV ───
def export_to_csv(json_path=HISTORY_FILE, csv_path="history.csv"):
    """
    Reads the JSON history and writes it to a CSV file.
    Returns the CSV path if successful, or None if no data.
    """
    # Load history list
    if not os.path.exists(json_path):
        return None

    try:
        with open(json_path, "r") as f:
            history = json.load(f)
            if not isinstance(history, list) or not history:
                return None
    except (json.JSONDecodeError, ValueError):
        return None

    # Write to CSV
    try:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["timestamp", "prediction", "confidence"])
            writer.writeheader()
            writer.writerows(history)
    except Exception:
        return None

    return csv_path
