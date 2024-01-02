from motor import motor_asyncio
from pymongo import MongoClient

from app.settings import MONGODB_URL
from core.collections.book import BookCollection
from core.collections.order import OrderCollection
from core.collections.user import UserCollection


class Database:

    def __init__(self):
        self.client = motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
        # self.client = MongoClient(MONGODB_URL)
        self.database = self.client.melius
        self.collections = {
            "user": UserCollection(self.database),
            "book": BookCollection(self.database),
            "order": OrderCollection(self.database)
        }

    def get_collection(self, collection_name):
        return self.collections[collection_name]

    def close(self):
        self.database.client.close()
