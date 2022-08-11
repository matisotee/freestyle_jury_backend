from pymongo import MongoClient
from shared.settings import settings

from competition.domain.repositories import CompetitionRepository


class MongoCompetitionRepository(CompetitionRepository):

    def __init__(self):
        self.client = MongoClient(settings.MONGO_URL)
        self.db = self.client.competition
        self.collection = self.db.competition

    def create(self, competition):
        competition._id = self.collection.insert_one(competition.to_dict()).inserted_id
        return competition
