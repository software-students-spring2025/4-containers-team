import pymongo
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

client = pymongo.MongoClient(MONGO_URI)
db = client["feeder_db"]
detections = db["detections"]

def insert_detection(doc):
    return detections.insert_one(doc).inserted_id

def get_recent_detections(limit=20):
    return list(detections.find().sort("timestamp", -1).limit(limit))
