import pytest
import requests
from django.conf import settings

from firebase_admin import auth
from rest_framework.test import APIClient

from authentication.firebase_connector import FirebaseConnector


def initialize_firebase():
    if not FirebaseConnector.is_initialized:
        FirebaseConnector.initialize_credentials()


@pytest.fixture
def verified_firebase_login_info():
    initialize_firebase()
    password = '12345678'
    firebase_user = auth.create_user(
        email='test@test.com',
        email_verified=True,
        password=password
    )

    yield {
        'email': firebase_user.email,
        'password': password,
        'uid': firebase_user.uid
    }

    auth.delete_user(firebase_user.uid)


@pytest.fixture
def verified_firebase_user(verified_firebase_login_info):
    email = verified_firebase_login_info['email']
    password = verified_firebase_login_info['password']
    response = requests.post(
        'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword',
        params={'key': settings.FIREBASE_API_KEY},
        data={'email': email, 'password': password, 'returnSecureToken': True}
    )
    json_response = response.json()

    return {
        'uid': verified_firebase_login_info['uid'],
        'token': json_response['idToken']
    }


@pytest.fixture
def client():
    return APIClient()
