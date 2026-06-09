from pymongo import MongoClient
from config import config
import sys

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    def connect(self):
        try:
            if not config.MONGODB_URI:
                print("Error: MONGODB_URI not found in configuration.")
                return None
            
            self.client = MongoClient(config.MONGODB_URI)
            self.db = self.client[config.DATABASE_NAME]
            
            # Send a ping to confirm a successful connection
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB!")
            return self.db
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            return None

    def get_db(self):
        if self.db is None:
            return self.connect()
        return self.db

db_instance = MongoDB()

def get_db():
    return db_instance.get_db()
