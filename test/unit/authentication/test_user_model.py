from unittest.mock import patch

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from authentication.firebase_connector import FirebaseConnector
from authentication.models import User, UserManager


@pytest.fixture
def user_parameters():
    return {
        'uid': 'test_uid',
        'name': 'matias',
        'last_name': 'perez',
        'aka': 'sot'
    }


@pytest.fixture
def user_parameters_with_token():
    return {
        'token': 'test_token',
        'name': 'matias',
        'last_name': 'perez',
        'aka': 'sot'
    }


@patch.object(UserManager, 'filter')
@patch.object(User, 'save')
def test_create_user_successful(mock_save, mock_filter, user_parameters):
    """Test creating a new user successfully"""
    mock_filter.return_value.exists.return_value = False

    user = User.objects.create_user(**user_parameters)

    for key, value in user_parameters.items():
        assert getattr(user, key) == value

    assert mock_save.called


@patch.object(UserManager, 'filter')
@patch.object(User, 'save')
def test_create_user_without_name_fails(mock_save, mock_filter, user_parameters):
    """Test creating a new user without name fails"""
    mock_filter.return_value.exists.return_value = False

    user_parameters['name'] = ''

    with pytest.raises(ValidationError):
        User.objects.create_user(**user_parameters)

    assert not mock_save.called


@patch.object(UserManager, 'filter')
@patch.object(User, 'save')
def test_create_existent_user_fails(mock_save, mock_filter, user_parameters):
    """Test creating an existent user fails"""
    mock_filter.return_value.exists.return_value = True

    with pytest.raises(IntegrityError):
        User.objects.create_user(**user_parameters)

    assert not mock_save.called


@patch.object(
    FirebaseConnector,
    'get_user_info_by_firebase_token',
    return_value={'uid': 'test_uid'}
)
@patch.object(UserManager, 'create_user')
def test_create_user_by_token(mock_create, mock_firebase, user_parameters_with_token):
    """Test creating user with token successfully"""

    User.objects.create_user_by_token(**user_parameters_with_token)
    assert mock_firebase.called
    assert mock_create.called
    assert mock_create.call_args[0] == ('test_uid', 'matias', 'perez', 'sot')


@patch.object(UserManager, 'create_user')
@patch.object(User, 'save')
def test_create_new_super_user(mock_save, mock_create_user):
    """Test creating a new super user"""
    mock_create_user.return_value = User(
        uid='test', aka='', name='super', last_name='user'
    )

    user = User.objects.create_superuser('test')

    assert user.is_superuser
    assert user.is_staff
