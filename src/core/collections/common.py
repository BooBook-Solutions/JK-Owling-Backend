from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List

from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


class BaseCollection(ABC, Generic[T]):

    def __init__(self, database):
        self.collection = database.user

    def to_pydantic(self, item, model):
        if item is None:
            return None
        if getattr(model, '__origin__', None) is list:
            return [self.to_pydantic(i, model.__args__[0]) for i in item]
        return model(id=str(item["_id"]), **item)

    @abstractmethod
    async def get(self, **kwargs) -> T:
        pass

    @abstractmethod
    async def create(self, **kwargs) -> T:
        pass

    @abstractmethod
    async def update(self, **kwargs) -> T:
        pass

    @abstractmethod
    async def delete(self, **kwargs) -> T:
        pass

    @abstractmethod
    async def filter(self, **kwargs) -> List[T]:
        pass
