from competition.exceptions import OrganizerCreationError
from competition.models.organizer import Organizer


class CompetitionCreator:

    @staticmethod
    def create_competition(user_dict, name, date, is_inscription_open_during_competition):

        if not user_dict.get('uid'):
            raise OrganizerCreationError('Missing uid')

        try:
            organizer = Organizer.objects.get(uid=user_dict['uid'])
        except Organizer.DoesNotExist:
            organizer = Organizer.objects.create(**user_dict)

        competition = organizer.create_competition(
            name,
            date,
            is_inscription_open_during_competition
        )

        return competition
