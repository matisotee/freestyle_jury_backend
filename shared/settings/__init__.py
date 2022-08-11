import os
import importlib
from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = 'Set the {} environment variable'.format(var_name)
        raise ImproperlyConfigured(error_msg)


def get_env_variable_or_none(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        return ''


settings = importlib.import_module(os.environ['DJANGO_SETTINGS_MODULE'])
