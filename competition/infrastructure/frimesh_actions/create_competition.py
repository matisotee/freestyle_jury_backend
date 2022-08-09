from frimesh import fields, Schema
from frimesh.action import FrimeshAction
from frimesh.exceptions import ActionError

from competition.application.competition_creator import CompetitionCreator
from competition.application.exceptions import CompetitionApplicationError


class CreateCompetitionSchema(Schema):
    name = fields.Str()
    date = fields.DateTime()
    organizer_id = fields.Str()


class CreateCompetitionAction(FrimeshAction):

    schema = CreateCompetitionSchema

    def run(
        self, organizer_id, name, date, **kwargs
    ):
        try:
            response = CompetitionCreator().create_competition(organizer_id, name, date)

            return response
        except CompetitionApplicationError as e:
            raise ActionError(e.message, code=e.code)
