import pytest
import requests
from bson import ObjectId
from django.conf import settings

from firebase_admin import auth
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate

from authentication.firebase_connector import FirebaseConnector
from authentication.models import User


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
def authenticated_post_request(verified_firebase_user):
    user = User.objects.create_user(verified_firebase_user['uid'], 'Test', 'test', aka='t')
    user._id = str(user._id)

    def create_request(url, payload):
        factory = APIRequestFactory()
        request = factory.post(url, payload, format='json')
        force_authenticate(request, user=user)
        return request
    return create_request


@pytest.fixture
def client():
    return APIClient()


def generate_object_id():
    return str(ObjectId())
