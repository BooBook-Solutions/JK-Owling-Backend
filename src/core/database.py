import motor.motor_asyncio

import settings
from core.collections.user import UserCollection


class Database:

    def __init__(self):
        client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
        self.database = client.jk_owling
        self.collections = {
            "user": UserCollection(self.database),
        }

    def get_collection(self, collection_name):
        return self.database[collection_name]
