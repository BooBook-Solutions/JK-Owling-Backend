from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, get_args

from bson import ObjectId
from pydantic import BaseModel

from core.schemas import User

T = TypeVar('T', bound=BaseModel)


class BaseCollection(ABC, Generic[T]):

    def __init__(self, database):
        self.database = database
        self.collection = None
        self.instance_class = None

    def to_pydantic(self, item, model):
        if item is None:
            return None
        if getattr(model, '__origin__', None) is list:
            return [self.to_pydantic(i, model.__args__[0]) for i in item]

        return self.instance_class(id=str(item["_id"]), **item)

    def to_mongo(self, item, exclude_id=False):
        if item is None:
            return None
        if exclude_id:
            d = {k: v for k, v in item.dict().items() if k != "id"}
        else:
            d = item.dict()
        return d

    async def get(self, item_id: str) -> T:
        item = await self.collection.find_one({"_id": ObjectId(item_id)})
        return self.to_pydantic(item, T)

    async def filter(self, **kwargs) -> List[T]:
        items = await self.collection.find().to_list(length=None)
        return self.to_pydantic(items, List[T])

    async def create(self, new_item: T, **kwargs) -> T:
        new_item_mongo = self.to_mongo(new_item, True)
        result = await self.collection.insert_one(new_item_mongo)
        created_item = self.instance_class(**new_item_mongo)
        created_item.id = str(result.inserted_id)
        return created_item

    async def update(self, item: T, **kwargs) -> T:
        mongo_item = self.to_mongo(item, True)
        self.collection.update_one({'_id': ObjectId(item.id)}, {'$set': mongo_item})
        return item

    async def delete(self, item_id) -> bool:
        result = await self.collection.delete_one({'_id': ObjectId(item_id)})
        return result.deleted_count > 0
