from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):
        """Creates and saves a new user"""
        user = self.model(email=email, **kwargs)
        user.set_password(password)

        # Validate model and raise an exception if the data doesn't fit
        user.clean_fields()
        user.email = self.normalize_email(user.email)
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
    name = models.CharField(max_length=25,)
    last_name = models.CharField(max_length=25)
    aka = models.CharField(max_length=25, blank=True)
    is_verified = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
