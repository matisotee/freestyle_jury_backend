import datetime
from pytz import utc
from competition.domain.exceptions import CompetitionPastDateError
from bson import ObjectId


class Competition:
    STATUS_CREATED = 'created'
    STATUS_STARTED_WITH_INSCRIPTION_OPEN = 'started_with_inscription_open'
    STATUS_STARTED = 'started'
    STATUS_FINISHED = 'finished'

    def __init__(self, name, date, organizer, status, phases=None, competitors=None, _id=None):
        self._id = _id if type(_id) != str else ObjectId(_id)
        self.name = name
        self.date = date
        self.status = status
        self.phases = phases
        self.competitors = competitors
        self.organizer = organizer if type(organizer) != str else ObjectId(organizer)

    @classmethod
    def create(cls, name, date, organizer_id):
        if date < datetime.datetime.now(tz=utc):
            raise CompetitionPastDateError('You tried to set a past date to a new competition')
        return cls(name, date, organizer_id, cls.STATUS_CREATED)

    def to_dict(self):
        data_dict = {
            'name': self.name,
            'date': self.date,
            'status': self.status,
            'phases': self.phases,
            'organizer': self.organizer,
            'competitors': self.competitors,
        }
        if self._id:
            data_dict['_id'] = self._id
        return data_dict
