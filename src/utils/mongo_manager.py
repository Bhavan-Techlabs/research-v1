import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class MongoDBManager:
    """
    Generic MongoDB manager for reusable CRUD operations on any collection.
    Implements a singleton pattern per (mongodb_uri, database_name, collection_name).
    Subclass this for specific document types.
    """

    _instances = {}

    def __new__(
        cls, collection_name, mongodb_uri=None, database_name="research_assistant"
    ):
        mongodb_uri = mongodb_uri or os.getenv("MONGODB_URI")
        if not mongodb_uri:
            raise ValueError(
                "MongoDB URI not provided. Set MONGODB_URI environment variable or pass it as parameter."
            )
        key = (mongodb_uri, database_name, collection_name)
        if key not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[key] = instance
            instance._initialized = False
        return cls._instances[key]

    def __init__(
        self, collection_name, mongodb_uri=None, database_name="research_assistant"
    ):
        if getattr(self, "_initialized", False):
            return
        self.mongodb_uri = mongodb_uri or os.getenv("MONGODB_URI")
        self.database_name = database_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None
        self._connect()
        self._initialized = True

    def _connect(self):
        try:
            self.client = MongoClient(self.mongodb_uri)
            self.client.admin.command("ping")
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]
            print(f"✅ Connected to MongoDB collection: {self.collection_name}")
        except ConnectionFailure as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            raise

    def insert_one(self, doc):
        return self.collection.insert_one(doc)

    def find_one(self, query):
        return self.collection.find_one(query)

    def find(self, query=None):
        return list(self.collection.find(query or {}))

    def update_one(self, query, updates):
        return self.collection.update_one(query, {"$set": updates})

    def delete_one(self, query):
        return self.collection.delete_one(query)

    def distinct(self, key):
        return self.collection.distinct(key)

    def insert_many(self, docs):
        return self.collection.insert_many(docs)

    def close(self):
        if self.client:
            self.client.close()
            print("✅ MongoDB connection closed")
