from bson import ObjectId
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from djongo import models

from api_gateway.domain.exceptions.user import ExistingUserError
from shared.models.base import BaseModel, BaseManager


class UserManager(BaseManager):

    def create_user(self, provider_id, name, last_name, email=None, phone_number=None, aka=''):
        """Creates and saves a new user"""
        if self.filter(provider_id=provider_id).exists():
            raise ExistingUserError()

        user = self.model(
            provider_id=provider_id,
            name=name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            aka=aka
        )
        user.set_unusable_password()

        # Validate model and raise an exception if the data doesn't fit
        user.clean_fields()
        user.save(using=self._db)

        return user

    def create_superuser(self, provider_id, aka=''):
        """Creates and saves a super user"""
        default_params = {
            'name': 'super',
            'last_name': 'user'
        }
        user = self.create_user(provider_id=provider_id, aka=aka, **default_params)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model"""
    class Meta:
        app_label = 'api_gateway'

    _id = models.ObjectIdField(db_column='_id')
    provider_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=25,)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=25, blank=True)
    aka = models.CharField(max_length=25, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'provider_id'


class PermissionManager(BaseManager):

    def create(self, object_id, object_type, authorized_user_ids):
        permission = Permission(_id=ObjectId(object_id), object_type=object_type)
        authorized_users = User.objects.filter(_id__in=authorized_user_ids)
        for user in authorized_users:
            permission.authorized_users.add(user)
        permission.save()

        return permission


class Permission(BaseModel):
    USER_TYPE = 'USER'
    COMPETITION_TYPE = 'COMPETITION'
    TYPE_CHOICES = (
        (USER_TYPE, 'User'),
        (COMPETITION_TYPE, 'Competition'),
    )
    object_type = models.CharField(max_length=244, choices=TYPE_CHOICES)
    authorized_users = models.ArrayReferenceField(
        to=User,
        on_delete=models.CASCADE,
    )

    objects = PermissionManager()
