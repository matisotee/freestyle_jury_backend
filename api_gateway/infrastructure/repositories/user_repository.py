from pymongo import MongoClient
from shared.settings import settings

from api_gateway.domain.exceptions.user import (
    ExistingUserError,
    NotExistentUserError,
)
from api_gateway.domain.user import User
from api_gateway.domain.repositories import UserRepository


class MongoUserRepository(UserRepository):

    def __init__(self):
        self.client = MongoClient(settings.MONGO_URL)
        self.db = self.client.user
        self.collection = self.db.user

    def create(self, user):
        if self.collection.count_documents({'provider_id': user.provider_id}) != 0:
            raise ExistingUserError()
        user._id = self.collection.insert_one(user.to_dict()).inserted_id
        return user

    def get_by_provider_id(self, provider_id):
        user_data = self.collection.find_one({'provider_id': provider_id})
        if not user_data:
            raise NotExistentUserError()
        return User(**user_data)

    def delete(self, user_id):
        self.collection.delete_one({'_id': user_id})
