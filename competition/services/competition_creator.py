from competition.exceptions import OrganizerCreationError
from competition.models.organizer import Organizer


class CompetitionCreator:

    @classmethod
    def create_competition(cls, organizer_dict, name, date, open_inscription_during_competition):

        if not organizer_dict.get('_id'):
            raise OrganizerCreationError('Missing id')

        try:
            organizer = Organizer.objects.get(_id=organizer_dict['_id'])
        except Organizer.DoesNotExist:
            organizer = Organizer.objects.create(**organizer_dict)

        competition = organizer.create_competition(
            name,
            date,
            open_inscription_during_competition
        )

        return cls._map_competition_to_dict(competition)

    @staticmethod
    def _map_competition_to_dict(competition):
        return {
            'name': competition.name,
            'status': competition.status
        }
