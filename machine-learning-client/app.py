from flask import Flask, request, jsonify
import torch
import torchvision
import base64
import io
from PIL import Image
from torchvision.models.detection import FasterRCNN_ResNet50_FPN_Weights
from torchvision.transforms import functional as F
from datetime import datetime
from database.db import insert_detection

app = Flask(__name__)

# Load model globally for better performance
weights = FasterRCNN_ResNet50_FPN_Weights.COCO_V1
model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights=weights)
model.eval()
categories = weights.meta["categories"]


@app.route('/detect', methods=['POST'])
def detect():
    try:
        # Get image from request
        image_data = request.json.get('image')
        if not image_data:
            return jsonify({"success": False, "error": "No image provided"}), 400

        # Decode base64 image
        _, encoded = image_data.split(',', 1)
        image_bytes = base64.b64decode(encoded)

        # Load image
        input_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image_tensor = F.to_tensor(input_image)

        # Run detection
        with torch.no_grad():
            predictions = model([image_tensor])[0]

        # Get results
        boxes = predictions["boxes"].tolist()
        scores = predictions["scores"].tolist()
        labels = [categories[i] for i in predictions["labels"]]

        # Filter by threshold (0.5)
        threshold = 0.5
        detections = []
        is_detected = False
        highest_score = 0
        best_label = None

        for i, score in enumerate(scores):
            if score >= threshold:
                detections.append({
                    "box": boxes[i],
                    "label": labels[i],
                    "confidence": score
                })

                if score > highest_score:
                    highest_score = score
                    best_label = labels[i]
                    is_detected = True

        # Store in database if object detected
        if is_detected:
            detection_result = {
                "timestamp": datetime.utcnow(),
                "image": "base64_image",  
                "result": best_label,
                "confidence": highest_score,
            }


        return jsonify({
            "success": True,
            "is_detected": is_detected,
            "label": best_label,
            "confidence": highest_score,
            "detections": detections
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)