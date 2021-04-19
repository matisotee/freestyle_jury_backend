from bson import ObjectId
from bson.errors import InvalidId

from djongo import models


class IdValidationError(Exception):

    def __init__(self, *args):
        super().__init__(*args)


class BaseManager(models.DjongoManager):

    def get(self, *args, **kwargs):
        if kwargs.get('_id'):
            str_id = str(kwargs['_id'])
            try:
                kwargs['_id'] = ObjectId(str_id)
            except InvalidId:
                raise IdValidationError(f'`{str_id}` is not a valid ObjectID')
        return super().get(*args, **kwargs)

    def filter(self, *args, **kwargs):
        if kwargs.get('_id'):
            str_id = str(kwargs['_id'])
            try:
                kwargs['_id'] = ObjectId(str_id)
            except InvalidId:
                raise IdValidationError(f'`{str_id}` is not a valid ObjectID')
        return super().filter(*args, **kwargs)


class BaseModel(models.Model):

    class Meta:
        abstract = True

    _id = models.ObjectIdField(db_column='_id')

    def save(self, *args, **kwargs):
        if self._id:
            str_id = str(self._id)
            try:
                self._id = ObjectId(str_id)
            except InvalidId:
                raise IdValidationError(f'`{str_id}` is not a valid ObjectID')
        return super().save(*args, **kwargs)
