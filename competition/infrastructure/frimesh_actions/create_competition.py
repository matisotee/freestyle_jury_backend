from datetime import datetime

from frimesh.action import FrimeshAction
from frimesh.exceptions import ActionError

from competition.application.competition_creator import CompetitionCreator
from competition.application.exceptions import CompetitionApplicationError


class CreateCompetitionAction(FrimeshAction):

    schema = {
        'name': str,
        'date': datetime,
        'open_inscription_during_competition': bool,
        'organizer': {
            'name': str,
            'last_name': str,
            'aka': str,
            '_id': str
        }
    }

    def run(
        self, organizer, name, date, open_inscription_during_competition, **kwargs
    ):
        try:
            response = CompetitionCreator.create_competition(
                organizer,
                name,
                date,
                open_inscription_during_competition
            )

            return response
        except CompetitionApplicationError as e:
            raise ActionError(e.message, code=e.code)
