from typing import List, Optional

from bson import ObjectId

from core.database.collections.mongodb.common import BaseMongoCollection
from core.schemas import Order


class OrderCollection(BaseMongoCollection[Order]):

    def __init__(self, database):
        super().__init__(database)
        self.collection = database.order
        self.instance_class = Order

    async def filter(self, user_id: Optional[str] = None, **kwargs) -> List[Order]:
        if user_id is None:
            items = await self.collection.find().to_list(length=None)
        else:
            items = await self.collection.find({"user": user_id}).to_list(length=None)
        return self.to_pydantic(items, List[Order])

    async def update(self, order_id: str, **kwargs) -> Order:
        status = kwargs.get('status')
        self.collection.update_one({'_id': ObjectId(order_id)}, {'$set': {"status": status}})
        item = await self.collection.find_one({"_id": ObjectId(order_id)})
        return self.to_pydantic(item, Order)
