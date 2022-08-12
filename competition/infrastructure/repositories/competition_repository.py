from pymongo import MongoClient
from bson import ObjectId

from competition.domain.competition import Competition
from shared.settings import settings

from competition.domain.repositories import CompetitionRepository


class MongoCompetitionRepository(CompetitionRepository):

    def __init__(self):
        self.client = MongoClient(settings.MONGO_URL)
        self.db = self.client.competition
        self.collection = self.db.competition

    def create(self, competition: Competition):
        competition_data = competition.dict()
        competition_data.pop('id')
        competition_data['organizer'] = ObjectId(competition_data['organizer'])
        competition.id = str(self.collection.insert_one(competition_data).inserted_id)
        return competition
