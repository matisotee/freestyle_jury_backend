from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from djongo import models

from api_gateway.domain.exceptions.user import ExistingUserError


class UserManager(BaseUserManager):

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

        # Validate model and raise an exception if the data doesn't fit
        user.clean_fields()
        user.save(using=self._db)

        return user

    def create_superuser(self, uid, aka=''):
        """Creates and saves a super user"""
        default_params = {
            'name': 'super',
            'last_name': 'user'
        }
        user = self.create_user(uid=uid, aka=aka, **default_params)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model"""
    _id = models.ObjectIdField(db_column='_id')
    provider_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=25,)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=25, blank=True)
    aka = models.CharField(max_length=25, blank=True)
    password = models.CharField(max_length=25, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'provider_id'
