from djongo import models

from competition.domain.models.competition import Competition
from shared.models.base import BaseModel, BaseManager


class OrganizerManager(BaseManager):

    def get_or_create(self, organizer_id):
        try:
            organizer = self.get(_id=organizer_id)
        except Organizer.DoesNotExist:
            organizer = self.model(_id=organizer_id)
            # Validate model and raise an exception if the data doesn't fit
            organizer.full_clean()
            organizer.save()
        return organizer


class Organizer(BaseModel):
    competitions = models.ArrayReferenceField(
        to=Competition,
        blank=True,
        on_delete=models.CASCADE,
    )

    objects = OrganizerManager()

    def create_competition(self, name, date, open_inscription_during_competition):
        competition = Competition.objects.create(
            name=name,
            date=date,
            open_inscription_during_competition=open_inscription_during_competition,
        )

        self.competitions.add(competition)

        return competition
