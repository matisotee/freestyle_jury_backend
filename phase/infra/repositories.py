from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
from typing import List

from phase.domain.exceptions import NotExistentCompetitionError
from phase.domain.phase import Competition, Phase
from phase.domain.repositories import CompetitionRepository, PhaseRepository
from shared.settings import settings


class MongoCompetitionRepository(CompetitionRepository):

    def __init__(self):
        self.client = MongoClient(settings.MONGO_URL)
        self.db = self.client.phase
        self.collection = self.db.competition

    def create(self, competition: Competition) -> Competition:
        competition_data = competition.dict()
        if competition_data['id']:
            competition_data['_id'] = ObjectId(competition_data['id'])
        competition_data.pop('id')
        competition.id = str(self.collection.insert_one(competition_data).inserted_id)
        return competition

    def get_by_id(self, competition_id: str) -> Competition:
        try:
            mongo_id = ObjectId(competition_id)
        except InvalidId:
            raise NotExistentCompetitionError()

        competition_data = self.collection.find_one({'_id': mongo_id})
        if not competition_data:
            raise NotExistentCompetitionError()
        competition_data['id'] = str(competition_data['_id'])
        competition_data.pop('_id')
        return Competition(**competition_data)


class MongoPhaseRepository(PhaseRepository):

    def __init__(self):
        self.client = MongoClient(settings.MONGO_URL)
        self.db = self.client.phase
        self.collection = self.db.phase

    def create(self, phase: Phase) -> Phase:
        phase_data = phase.dict()
        if phase_data['id']:
            phase_data['_id'] = ObjectId(phase_data['id'])
        phase_data.pop('id')
        phase.id = str(self.collection.insert_one(phase_data).inserted_id)
        return phase

    def get(self, query: dict) -> List[Phase]:
        phase_list = []
        phases = self.collection.find(query)
        for phase in phases:
            phase['id'] = str(phase['_id'])
            phase.pop('_id')
            phase_list.append(Phase(**phase))
        return phase_list
