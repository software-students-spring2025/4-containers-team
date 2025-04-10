import base64
import io
import os
from datetime import datetime
from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
from PIL import Image
import numpy as np

# Later we'll import detect_human from ml_utils
# from ml_utils import detect_human

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/")
client = MongoClient(MONGO_URI)
db = client["dog_feeder"]
collection = db["detections"]

def dummy_detect_human(image):
    # Simulated detection: just say "yes" half the time
    import random
    return random.choice([True, False]), "person", 0.92

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/detect", methods=["POST"])
def detect():
    try:
        data_url = request.json["image"]
        header, encoded = data_url.split(",", 1)
        image_data = base64.b64decode(encoded)
        image = Image.open(io.BytesIO(image_data)).convert("RGB")

        # Convert PIL to NumPy array (no OpenCV)
        frame = np.array(image)  # stays in RGB

        # Call the dummy model (replace with real YOLO later)
        is_human, label, confidence = dummy_detect_human(frame)

        # Save image and detection result to MongoDB
        image_base64 = encoded
        result = {
            "label": label,
            "confidence": confidence,
            "is_human": is_human,
            "timestamp": datetime.utcnow(),
            "image": image_base64,
        }
        collection.insert_one(result)

        return jsonify({"success": True, "is_human": is_human})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
