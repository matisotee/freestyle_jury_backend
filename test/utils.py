import datetime
import pytz

from fastapi.testclient import TestClient
from firebase_admin import auth
import pytest
import requests
from bson import ObjectId

from api_gateway.domain.user import User
from api_gateway.infrastructure.authentication.fast_api_authentication import authenticate_with_token
from api_gateway.infrastructure.authentication.firebase_auth_provider import FirebaseAuthProvider
from api_gateway.infrastructure.repositories.user_repository import MongoUserRepository
from frimesh.client import FrimeshClient
from main import app
from shared.frimesh_services_map import services_map
from shared.settings import settings


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
        self.email = json_response['email']

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


@pytest.fixture
def authorization_header(firebase_user):
    user = User(provider_id=firebase_user.uid, name='Test', last_name='test', aka='t', email='test@test.com')
    repository = MongoUserRepository()
    user = repository.create(user)
    yield {"Authorization": f"Bearer {firebase_user.token}"}
    repository.delete(user.id)


async def mock_authenticate_with_token():
    return User(
        _id=generate_object_id(), provider_id='1234', name='test', last_name='test',
        email='test@test.com', phone_number='1234567', aka='tes'
    )


@pytest.fixture
def mock_authenticated_client():
    app.dependency_overrides[authenticate_with_token] = mock_authenticate_with_token
    yield TestClient(app)
    app.dependency_overrides = {}


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def frimesh_client():
    return FrimeshClient(services_map)


def generate_object_id():
    return str(ObjectId())


@pytest.fixture
def now_date():
    date_now = datetime.datetime.now(tz=datetime.timezone.utc).astimezone(
        pytz.timezone('America/Argentina/Buenos_Aires')
    )
    date_now_plus_an_hour = date_now + datetime.timedelta(hours=1)
    return date_now_plus_an_hour.isoformat()
