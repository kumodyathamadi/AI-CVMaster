from pymongo import MongoClient
from config import config
import sys
import certifi
import traceback

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None
        self.ca = certifi.where()

    def connect(self):
        print(f"Connecting to MongoDB with URI: {config.MONGODB_URI[:20]}...")
        try:
            if not config.MONGODB_URI:
                print("Error: MONGODB_URI not found in configuration.")
                return None
            
            # Using basic TLS settings that usually work across platforms
            self.client = MongoClient(
                config.MONGODB_URI,
                tls=True,
                tlsCAFile=self.ca,
                tlsAllowInvalidCertificates=True, # Bypass common Windows cert issues
                serverSelectionTimeoutMS=5000,   # Don't wait too long
                connectTimeoutMS=5000
            )
            self.db = self.client[config.DATABASE_NAME]
            
            # Send a ping to confirm a successful connection
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB!")
            return self.db
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            # print(traceback.format_exc())
            return None

    def get_db(self):
        if self.db is None:
            return self.connect()
        return self.db

db_instance = MongoDB()

def get_db():
    return db_instance.get_db()
