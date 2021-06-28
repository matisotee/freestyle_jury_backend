import datetime

from django.utils import timezone
from djongo import models
from pytz import utc

from competition.domain.exceptions import CompetitionPastDateError
from competition.domain.models.competitor import Competitor
from competition.domain.models.phase import Phase
from shared.models.base import BaseModel, BaseManager


class CompetitionManager(BaseManager):

    def create(self, name, date, open_inscription_during_competition):

        competition = self.model(
            name=name, date=date, open_inscription_during_competition=open_inscription_during_competition
        )

        if competition.date < datetime.datetime.now(tz=utc):
            raise CompetitionPastDateError('You tried to set a past date to a new competition')
        competition.status = Competition.STATUS_CREATED
        # Validate model and raise an exception if the data doesn't fit
        competition.clean_fields()
        competition.save(using=self._db)

        return competition


class Competition(BaseModel):
    name = models.CharField(max_length=255,)
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=25,)
    phases = models.ArrayReferenceField(
        to=Phase,
        on_delete=models.CASCADE,
        blank=True
    )
    competitors = models.ArrayReferenceField(
        to=Competitor,
        on_delete=models.CASCADE,
        blank=True
    )
    open_inscription_during_competition = models.BooleanField(default=True)

    STATUS_CREATED = 'created'
    STATUS_STARTED_WITH_INSCRIPTION_OPEN = 'started_with_inscription_open'
    STATUS_STARTED = 'started'
    STATUS_FINISHED = 'finished'
    STATUSES = [
        STATUS_CREATED,
        STATUS_STARTED_WITH_INSCRIPTION_OPEN,
        STATUS_STARTED,
        STATUS_FINISHED
    ]

    objects = CompetitionManager()
