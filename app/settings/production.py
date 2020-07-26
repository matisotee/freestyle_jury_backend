from .base import *
import dj_database_url

ALLOWED_HOSTS = [
    'search-events-evb.herokuapp.com',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'vacations',
        'USER': 'name',
        'PASSWORD': '',
        'PORT': '',
    }
}
DB_FROM_ENV = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(DB_FROM_ENV)

STATIC_ROOT = os.path.join(BASE_DIR, 'static_prod')
# Application definition

INSTALLED_APPS += [  # noqa
    'whitenoise.runserver_nostatic'
]

MIDDLEWARE += [  # noqa
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEBUG = False
