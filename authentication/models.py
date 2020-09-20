from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models, IntegrityError

from authentication.firebase_connector import FirebaseConnector


class UserManager(BaseUserManager):

    def create_user_by_token(self, token, name, last_name, aka=''):
        payload = FirebaseConnector.get_user_info_by_firebase_token(token)
        return self.create_user(payload['uid'], name, last_name, aka)

    def create_user(self, uid, name, last_name, aka=''):
        """Creates and saves a new user"""
        if self.filter(uid=uid).exists():
            raise IntegrityError

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
    uid = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=25,)
    last_name = models.CharField(max_length=25)
    aka = models.CharField(max_length=25, blank=True)
    password = models.CharField(max_length=25, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'uid'
