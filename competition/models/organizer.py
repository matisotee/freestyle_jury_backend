from django.core.exceptions import ValidationError
from djongo import models

from competition.exceptions import DUPLICATED_UNIQUE_FIELD_STRING
from competition.models.competition import Competition


class OrganizerManager(models.DjongoManager):

    def create(self, _id, name, last_name, aka):
        if self.filter(_id=_id).exists():
            raise ValidationError(
                "{'uid': ['There is another organizer with this id']}"
            )
        organizer = self.model(
            _id=_id, name=name, last_name=last_name, aka=aka,
        )

        # Validate model and raise an exception if the data doesn't fit
        organizer.clean_fields()
        organizer.save(using=self._db)
        return organizer


class Organizer(models.Model):
    _id = models.ObjectIdField(db_column='_id')
    name = models.CharField(max_length=25,)
    last_name = models.CharField(max_length=25)
    aka = models.CharField(max_length=25, blank=True)
    competitions = models.ArrayReferenceField(
        to=Competition,
        blank=True,
        on_delete=models.CASCADE,
    )

    objects = OrganizerManager()

    def create_competition(self, name, date, is_inscription_open_during_competition):
        competition = Competition.objects.create(
            name=name,
            date=date,
            open_inscription_during_competition=is_inscription_open_during_competition,
        )

        self.competitions.add(competition)

        return competition
