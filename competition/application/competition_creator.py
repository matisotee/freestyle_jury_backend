from competition.application.exceptions import CompetitionApplicationError
from competition.domain.exceptions import CompetitionPastDateError
from competition.domain.models.organizer import Organizer


class CompetitionCreator:

    @classmethod
    def create_competition(cls, organizer_id, name, date, open_inscription_during_competition):

        organizer = Organizer.objects.get_or_create(organizer_id)

        try:
            competition = organizer.create_competition(
                name,
                date,
                open_inscription_during_competition
            )
        except CompetitionPastDateError:
            raise CompetitionApplicationError('Date: set a current or future date', code='PAST_DATE')

        return cls._map_competition_to_dict(competition)

    @staticmethod
    def _map_competition_to_dict(competition):
        return {
            'name': competition.name,
            'status': competition.status,
            'id': str(competition._id)
        }
