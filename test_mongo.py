from pymongo import MongoClient
import sys

try:
    MONGO_URI = "mongodb+srv://sandeeprana:sandeeprana@cluster0.c9l7xv5.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("MongoDB connection successful!")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    sys.exit(1)
