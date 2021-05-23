from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from djongo import models

from api_gateway.domain.exceptions.user import ExistingUserError


class UserManager(BaseUserManager):

    def create_user(self, uid, name, last_name, aka=''):
        """Creates and saves a new user"""
        if self.filter(uid=uid).exists():
            raise ExistingUserError()

        user = self.model(uid=uid, name=name, last_name=last_name, aka=aka)

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
    uid = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=25,)
    last_name = models.CharField(max_length=25)
    aka = models.CharField(max_length=25, blank=True)
    password = models.CharField(max_length=25, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'uid'
