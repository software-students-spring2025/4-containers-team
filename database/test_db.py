from pymongo import MongoClient
from datetime import datetime


def test_database():

    client = MongoClient("mongodb://localhost:27017/")
    db = client["dog_feeder"]

    detections = db["detections"]

    sample_detection = {
        "timestamp": datetime.utcnow(),
        "image": "sample_image.jpg",
        "result": "human",
        "confidence": 0.95,
    }

    result = detections.insert_one(sample_detection)
    print("Uploaded document with id:", result.inserted_id)

    retrieved = detections.find_one({"id": result.inserted_id})
    print("Retrieved document:")
    print(retrieved)


if __name__ == "__main__":
    test_database()
