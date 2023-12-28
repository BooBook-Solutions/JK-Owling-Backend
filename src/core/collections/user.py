from typing import List

from core.collections.common import BaseCollection
from core.schemas import User


class UserCollection(BaseCollection[User]):

    def __init__(self, database):
        super().__init__(database)
        self.collection = database.user

    async def get(self, user_id: int) -> User:
        pass

    async def filter(self) -> List[User]:
        pass

    async def create(self, user) -> User:
        new_user = await self.collection.insert_one({
            "name": user.name,
            "email": user.email,
            "password": user.password,
            "role": user.role
        })
        return new_user

    async def update(self) -> User:
        pass

    async def delete(self) -> User:
        pass
