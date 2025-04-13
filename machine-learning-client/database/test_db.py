import pymongo
from datetime import datetime


client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["feeder_db"]
collection = db["detections"]


sample_detection = {

  "_id": "ObjectId('67fbe0f549a5cff8ba1fa28a')",
  "label": "person",
  "confidence": 0.9937363862991333,
  "is_human": "false",
  "timestamp": "ISODate('2025-04-13T16:06:13.275Z')",
  "image": "/9j/4AAQSkZJRgABAQAAAQABAAD/4gHYSUNDX1BST0ZJTEUAAQEAAAHIAAAAAAQwAABtbnRyUkdCIFhZWiAH4AABAAEAAAAAAABh..."

}


inserted_id = collection.insert_one(sample_detection).inserted_id
print(f"Inserted document with _id: {inserted_id}")