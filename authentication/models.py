from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from freestyle_jury.utils import model_utils


class UserManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):
        """Creates and saves a new user"""
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        model_utils.check_missing_required_fields(user, self.model)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a super user"""
        default_params = {
            'name': 'super',
            'last_name': 'user'
        }
        user = self.create_user(email, password, **default_params)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    aka = models.CharField(max_length=25, unique=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    MANDATORY_FIELDS = ['email', 'password', 'name', 'last_name']

