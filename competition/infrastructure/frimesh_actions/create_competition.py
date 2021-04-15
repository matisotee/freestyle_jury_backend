from datetime import datetime

from frimesh.action import FrimeshAction
from frimesh.exceptions import ActionError

from competition.exceptions import CompetitionPastDateError
from competition.services.competition_creator import CompetitionCreator


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
        except CompetitionPastDateError:
            raise ActionError('Date: set a current or future date', code='PAST_DATE')
