import datetime

from django.core.exceptions import ValidationError
from django.utils import timezone
from djongo import models
from pytz import utc

from competition.models.competitor import Competitor
from competition.models.phase import Phase


class CompetitionManager(models.DjongoManager):

    def create(self, *args, **kwargs):
        if kwargs.get('phases') or kwargs.get('competitors'):
            raise ValidationError(
                'Cannot create a new competition with competitors or phases'
            )

        competition = self.model(**kwargs)

        if competition.date < datetime.datetime.now(tz=utc):
            raise ValidationError('Date: set a current or future date', code='PAST_DATE')

        competition.status = Competition.STATUS_CREATED
        # Validate model and raise an exception if the data doesn't fit
        competition.clean_fields()
        competition.save(using=self._db)

        return competition


class Competition(models.Model):
    _id = models.ObjectIdField(db_column='_id')
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
