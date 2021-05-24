from .base import *  # noqa

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'freestyle_jury',
        'CLIENT': {
            'host': 'mongodb://mongodb/freestyle_jury',
        },
    }
}

DEBUG = True
