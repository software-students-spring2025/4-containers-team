import pymongo
from datetime import datetime


client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["feeder_db"]
collection = db["detections"]


sample_doc = {
    
    "timestamp": datetime.utcnow(),
    "image": "images/test_image.jpg",
    "result": "dog",
    "confidence": 0.92,
}


inserted_id = collection.insert_one(sample_doc).inserted_id
print(f"Inserted document with _id: {inserted_id}")