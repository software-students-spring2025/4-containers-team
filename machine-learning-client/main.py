"""ResNet object detection model.
Run using:
    python3 testing.py --image 1.jpg
"""

import argparse

import torch
import torchvision
from PIL import Image, ImageDraw
from torchvision.models.detection import FasterRCNN_ResNet50_FPN_Weights
from torchvision.transforms import functional as F


#take in arguments from terminal
parser = argparse.ArgumentParser()
parser.add_argument('--image', type=str, required=True,
                    help="Path to the image")
parser.add_argument('--threshold', type=float, default=0.5,
                    help="Detection confidence")
args = parser.parse_args()


def load_image(image_path):
    """Load image"""
    return Image.open(image_path).convert("RGB")


def draw_bounding_boxes(img, det_boxes, det_labels, det_scores, threshold=0.5):
    """Draw bounding boxes on the image"""
    draw = ImageDraw.Draw(img)
    for i, box in enumerate(det_boxes):
        if det_scores[i] >= threshold:
            label = det_labels[i]
            score = det_scores[i]
            draw.rectangle(box.tolist(), outline="red", width=3)
            draw.text((box[0], box[1] - 10),
                      f"{label} ({score:.2f})", fill="red")
    return img



#get model
weights = FasterRCNN_ResNet50_FPN_Weights.COCO_V1
model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights=weights)
model.eval()

#get the categories
categories = weights.meta["categories"]

#run the detection
input_image = load_image(args.image)
image_tensor = F.to_tensor(input_image)

with torch.no_grad():
    predictions = model([image_tensor])[0]

boxes = predictions["boxes"]
scores = predictions["scores"]
labels = [categories[i] for i in predictions["labels"]]

#draw bounding boxes
image_with_boxes = draw_bounding_boxes(
    input_image.copy(), boxes, labels, scores, args.threshold)

#output result
OUTPUT_PATH = "output_detected.jpg"
image_with_boxes.save(OUTPUT_PATH)
print(f"Detection result saved to {OUTPUT_PATH}")
