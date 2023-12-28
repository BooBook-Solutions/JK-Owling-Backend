from typing import List

from core.collections.common import BaseCollection
from core.schemas import User


class UserCollection(BaseCollection[User]):

    def __init__(self, database):
        super().__init__(database)
        self.collection = database.user

    def get(self, user_id: int) -> User:
        pass

    def filter(self) -> List[User]:
        pass

    def create(self) -> User:
        pass

    def update(self) -> User:
        pass

    def delete(self) -> User:
        pass
