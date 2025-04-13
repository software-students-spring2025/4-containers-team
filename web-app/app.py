import base64
import os
import requests
from datetime import datetime
from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Get environment variables with defaults
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
ML_API_URL = os.getenv("ML_API_URL", "http://localhost:5001/detect")

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client["feeder_db"]
collection = db["detections"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/detect", methods=["POST"])
def detect():
    try:
        # Get image from request
        data_url = request.json["image"]
        header, encoded = data_url.split(",", 1)

        # Call the ML API using the environment variable
        response = requests.post(
            ML_API_URL,  # This uses the ML_API_URL from environment
            json={"image": data_url},
            timeout=30  # Add timeout to prevent hanging requests
        )

        if response.status_code != 200:
            return jsonify({"success": False, "error": f"ML API error: {response.text}"})

        result = response.json()

        # Save results to MongoDB
        detection = {
            "label": result.get("label"),
            "confidence": result.get("confidence"),
            "is_dog": (result.get("label") or "").lower() == "dog",
            "timestamp": datetime.utcnow(),
            "image": encoded[:100] + "...",
        }

        collection.insert_one(detection)

        return jsonify({"success": True, "is_dog": detection.get("is_dog", False)})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
