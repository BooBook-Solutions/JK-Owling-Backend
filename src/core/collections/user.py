from core.collections.common import BaseCollection
from core.schemas import User


class UserCollection(BaseCollection[User]):

    def __init__(self, database):
        super().__init__(database)
        self.collection = database.user
        self.instance_class = User

    async def get(self, email: str) -> User:
        user = await self.collection.find_one({"email": email})
        return self.to_pydantic(user, User)
