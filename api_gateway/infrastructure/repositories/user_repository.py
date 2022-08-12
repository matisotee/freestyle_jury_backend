from bson import ObjectId
from bson.errors import InvalidId
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

    def create(self, user: User) -> User:
        if self.collection.count_documents({'provider_id': user.provider_id}) != 0:
            raise ExistingUserError()
        user_data = user.dict()
        user_data.pop('id')
        user.id = str(self.collection.insert_one(user_data).inserted_id)
        return user

    def get_by_id(self, user_id: str) -> User:
        try:
            mongo_id = ObjectId(user_id)
        except InvalidId:
            raise NotExistentUserError()

        user_data = self.collection.find_one({'_id': mongo_id})
        if not user_data:
            raise NotExistentUserError()
        user_data['id'] = str(user_data['_id'])
        user_data.pop('_id')
        return User(**user_data)

    def get_by_provider_id(self, provider_id: str) -> User:
        user_data = self.collection.find_one({'provider_id': provider_id})
        if not user_data:
            raise NotExistentUserError()
        user_data['id'] = str(user_data['_id'])
        user_data.pop('_id')
        return User(**user_data)

    def delete(self, user_id: str):
        self.collection.delete_one({'_id': ObjectId(user_id)})
