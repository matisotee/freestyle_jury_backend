from competition.exceptions import OrganizerCreationError
from competition.models.organizer import Organizer


class CompetitionCreator:

    @staticmethod
    def create_competition(organizer_dict, name, date, is_inscription_open_during_competition):

        if not organizer_dict.get('_id'):
            raise OrganizerCreationError('Missing id')

        try:
            organizer = Organizer.objects.get(_id=organizer_dict['_id'])
        except Organizer.DoesNotExist:
            organizer = Organizer.objects.create(**organizer_dict)

        competition = organizer.create_competition(
            name,
            date,
            is_inscription_open_during_competition
        )

        return competition
