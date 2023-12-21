from core.collections.common import BaseCollection


class UserCollection(BaseCollection):

    def __init__(self, database):
        super().__init__(database)
        self.collection = database.user
