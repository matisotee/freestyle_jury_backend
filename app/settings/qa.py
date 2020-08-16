from .base import *
import dj_database_url
import django_heroku

ALLOWED_HOSTS = [
    'freestyle-jury-api-qa.herokuapp.com',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'freestyle_jury',
        'USER': 'name',
        'PASSWORD': '',
        'PORT': '',
    }
}
DB_FROM_ENV = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(DB_FROM_ENV)

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

DEBUG = False
django_heroku.settings(locals())

FRONTEND_DOMAIN = 'freestyle-jury-qa.herokuapp.com'
