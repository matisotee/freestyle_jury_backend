from .base import *
import django_heroku

ALLOWED_HOSTS = [
    'freestyle-jury-api-qa.herokuapp.com',
    'localhost',
    '127.0.0.1',
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_TMP = os.path.join(BASE_DIR, 'static')

os.makedirs(STATIC_TMP, exist_ok=True)
os.makedirs(STATIC_ROOT, exist_ok=True)
# Application definition

INSTALLED_APPS += [  # noqa
    'whitenoise.runserver_nostatic'
]

MIDDLEWARE += [  # noqa
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEBUG = True
django_heroku.settings(locals())
