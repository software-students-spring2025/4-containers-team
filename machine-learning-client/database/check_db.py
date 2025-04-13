import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db import get_recent_detections


results = get_recent_detections()
print("\n Recent MongoDB Detections:\n")
for doc in results:
    print(doc)
