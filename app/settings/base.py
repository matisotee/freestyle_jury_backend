"""
Django settings for search_events project.
Generated by 'django-admin startproject' using Django 3.0.5.
For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from datetime import timedelta

from app.settings import get_env_variable, get_env_variable_or_none
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)
)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_variable('SECRET_KEY')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    'freestyle_jury',
    'authentication',
    'competition'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'NON_FIELD_ERRORS_KEY': 'error',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'authentication.authenticator.FirebaseAuthentication',
    )
}

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DB_USERNAME = get_env_variable_or_none('MONGO_USERNAME')
DB_PASSWORD = get_env_variable_or_none('MONGO_PASSWORD')
DB_NAME = get_env_variable_or_none('MONGO_DATABASE_NAME')

DATABASES = {
   'default': {
       'ENGINE': 'djongo',
       'NAME': DB_NAME,
       'CLIENT': {
            'host': 'mongodb+srv://{}:{}@cluster0.zhs7q.mongodb.net/{}?retryWrites=true&w=majority'.format(
                DB_USERNAME,
                DB_PASSWORD,
                DB_NAME
            ),
            'username': DB_USERNAME,
            'password': DB_PASSWORD,
       },
   }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

AUTH_USER_MODEL = 'authentication.User'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1000000),
}

# Firebase credentials
FIREBASE_AUTH = {
    "SERVICE_ACCOUNT_KEY_FILE": {
        "type": get_env_variable_or_none('FIREBASE_TYPE'),
        "project_id": get_env_variable_or_none('FIREBASE_PROJECT_ID'),
        "private_key_id": get_env_variable_or_none('FIREBASE_PRIVATE_KEY_ID'),
        "private_key": get_env_variable_or_none('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
        "client_email": get_env_variable_or_none('FIREBASE_CLIENT_EMAIL'),
        "client_id": get_env_variable_or_none('FIREBASE_CLIENT_ID'),
        "auth_uri": get_env_variable_or_none('FIREBASE_AUTH_URI'),
        "token_uri": get_env_variable_or_none('FIREBASE_TOKEN_URI'),
        "auth_provider_x509_cert_url": get_env_variable_or_none('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
        "client_x509_cert_url": get_env_variable_or_none('FIREBASE_CLIENT_X509_CERT_URL')
    },
    "EMAIL_VERIFICATION": True
}
FIREBASE_API_KEY = get_env_variable_or_none('FIREBASE_API_KEY')

# Optimizely credential
OPTIMIZELY_SDK_KEY = get_env_variable_or_none('OPTIMIZELY_SDK_KEY')

# SWAGGER
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Auth token eg [Bearer] (JWT) ]': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

