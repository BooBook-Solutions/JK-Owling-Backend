from abc import ABC


class BaseCollection(ABC):

    def __init__(self, database):
        self.collection = database.user

    def find(self, query):
        return self.collection.find(query)

    async def find_one(self, query):
        return await self.collection.find_one(query)

    async def insert_one(self, document):
        return await self.collection.insert_one(document)

    async def update_one(self, query, update):
        return await self.collection.update_one(query, update)

    async def delete_one(self, query):
        return await self.collection.delete_one(query)
