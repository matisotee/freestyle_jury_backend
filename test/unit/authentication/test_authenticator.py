from unittest.mock import patch
from rest_framework.exceptions import AuthenticationFailed
import pytest

from authentication.authenticator import FirebaseAuthentication
from authentication.firebase_connector import FirebaseConnector
from authentication.models import User


@pytest.fixture
def authenticator():
    return FirebaseAuthentication()


@patch.object(
    FirebaseAuthentication, 'get_user_by_uid', return_value='mock_user'
)
@patch.object(
    FirebaseConnector,
    'authenticate_in_firebase',
    return_value={'uid': 'mock_uid'}
)
@patch.object(
    FirebaseAuthentication, 'get_token', return_value='token'
)
def test_authenticate_successfully(mock_get_token, mock_firebase, mock_get_user, authenticator):
    result = authenticator.authenticate('request')

    assert result == ('mock_user', {'uid': 'mock_uid'})
    assert mock_get_token.called
    assert mock_firebase.called
    assert mock_get_user.called


@patch.object(FirebaseAuthentication, 'get_token', return_value=None)
def test_authenticate_without_token(mock_get_token, authenticator):
    result = authenticator.authenticate('request')

    assert result is None


@patch(
    'authentication.authenticator.get_authorization_header',
    return_value='Bearer token'.encode()
)
def test_get_token_successfully(mock_get_token, authenticator):

    result = authenticator.get_token('request')

    assert result == b'token'


@patch(
    'authentication.authenticator.get_authorization_header',
    return_value=''
)
def test_get_token_without_authentication_header(mock_get_token, authenticator):
    result = authenticator.get_token('request')

    assert result is None


@patch(
    'authentication.authenticator.get_authorization_header',
    return_value='Bearer'.encode()
)
def test_get_token_without_token(mock_get_token, authenticator):

    with pytest.raises(AuthenticationFailed):
        authenticator.get_token('request')


@patch(
    'authentication.authenticator.get_authorization_header',
    return_value='Bearer token space'.encode()
)
def test_get_token_with_spaced_token(mock_get_token, authenticator):
    with pytest.raises(AuthenticationFailed):
        authenticator.get_token('request')


@patch.object(User, 'objects')
def test_get_user_by_uid_successfully(mock_objects, authenticator):
    user = User(uid='uid', name='test', last_name='user')
    mock_objects.get.return_value = user

    result = authenticator.get_user_by_uid('uid')

    assert result == user
    assert isinstance(result._id, str)


@patch.object(User, 'objects')
def test_get_user_by_uid_with_non_existent_user(mock_objects, authenticator):
    mock_objects.get.side_effect = User.DoesNotExist

    with pytest.raises(AuthenticationFailed):
        authenticator.get_user_by_uid('uid')


def test_authenticate_header(authenticator):

    result = authenticator.authenticate_header('request')

    expected = '{} realm="{}"'.format(
        authenticator.auth_header_prefix, authenticator.www_authenticate_realm
    )

    assert result == expected
