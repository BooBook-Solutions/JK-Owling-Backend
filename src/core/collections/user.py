from typing import List

from core.collections.common import BaseCollection
from core.schemas import User


class UserCollection(BaseCollection[User]):

    def __init__(self, database):
        super().__init__(database)
        self.collection = database.user

    async def get(self, email: str) -> User:
        user = await self.collection.find_one({"email": email})
        return self.to_pydantic(user, User)

    async def filter(self) -> List[User]:
        pass

    async def create(self, user) -> User:
        new_user = {
            "name": user.name,
            "email": user.email,
            "password": user.password,
            "role": user.role
        }
        result = await self.collection.insert_one(new_user)
        new_user = User(**new_user)
        new_user.id = str(result.inserted_id)
        return new_user

    async def update(self) -> User:
        pass

    async def delete(self) -> User:
        pass
