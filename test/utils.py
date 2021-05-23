import pytest
import requests
from bson import ObjectId
from django.conf import settings

from firebase_admin import auth
from rest_framework.test import APIClient

from app.frimesh_services_map import services_map
from authentication.infrastructure.authentication.firebase_auth_provider import FirebaseAuthProvider

from authentication.models import User
from frimesh.client import FrimeshClient


def initialize_firebase():
    if not FirebaseAuthProvider.is_initialized:
        FirebaseAuthProvider.initialize_credentials()


def verified_firebase_login_info():
    initialize_firebase()
    password = '12345678'
    firebase_user = auth.create_user(
        email='test@test.com',
        email_verified=True,
        password=password
    )

    return {
        'email': firebase_user.email,
        'password': password,
        'uid': firebase_user.uid
    }


class FirebaseUser:
    instance = None

    def __init__(self, *args, **kwargs):
        login_info = verified_firebase_login_info()
        email = login_info['email']
        password = login_info['password']
        response = requests.post(
            'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword',
            params={'key': settings.FIREBASE_API_KEY},
            data={'email': email, 'password': password, 'returnSecureToken': True}
        )
        json_response = response.json()

        self.uid = login_info['uid']
        self.token = json_response['idToken']

    @classmethod
    def get_instance(cls):
        if not cls.instance:
            cls.instance = FirebaseUser()
        return cls.instance


@pytest.fixture(scope='session', autouse=True)
def firebase_user():
    # Will be executed before the first test
    user = FirebaseUser.get_instance()
    yield user
    # Will be executed after the last test
    auth.delete_user(user.uid)


class AuthenticatedAPIClient(APIClient):

    instance = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        firebase_user = FirebaseUser.get_instance()
        user = User.objects.create_user(firebase_user.uid, 'Test', 'test', aka='t')
        user._id = str(user._id)
        self.force_authenticate(user=user)

    @classmethod
    def get_instance(cls):
        if not cls.instance:
            cls.instance = AuthenticatedAPIClient()
        return cls.instance


@pytest.fixture
def authenticated_client():
    return AuthenticatedAPIClient.get_instance()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def frimesh_client():
    return FrimeshClient(services_map)


def generate_object_id():
    return str(ObjectId())
