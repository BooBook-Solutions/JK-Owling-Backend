import motor.motor_asyncio

from app import settings
from core.collections.book import BookCollection
from core.collections.user import UserCollection


class Database:

    def __init__(self):
        client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
        self.database = client.jk_owling
        self.collections = {
            "user": UserCollection(self.database),
            "book": BookCollection(self.database),
        }

    def get_collection(self, collection_name):
        return self.database[collection_name]

    def close(self):
        self.database.client.close()
