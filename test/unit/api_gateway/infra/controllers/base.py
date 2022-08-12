from unittest.mock import MagicMock

import pytest

from api_gateway.domain.exceptions.user import NotExistentUserError
from api_gateway.infrastructure.controllers.base import get_path_user_id
from api_gateway.infrastructure.controllers.exceptions import HTTPException
from test.utils import generate_object_id

from api_gateway.domain.user import User


def test_get_path_user_id_with_me_in_url():
    authenticated_user = User(
        id=str(generate_object_id()),
        provider_id='1234',
        name='Test',
        last_name='Last',
        email='test@email.com'
    )
    path_user_id = 'me'

    result = get_path_user_id(path_user_id, authenticated_user, MagicMock())

    assert result == authenticated_user.id


def test_get_path_user_id_with_user_id_in_url():
    authenticated_user = User(
        id=str(generate_object_id()),
        provider_id='1234',
        name='Test',
        last_name='Last',
        email='test@email.com'
    )
    path_user_id = str(generate_object_id())

    result = get_path_user_id(path_user_id, authenticated_user, MagicMock())

    assert result == path_user_id


def test_get_path_user_id_fails_with_invalid_user_id_in_url():
    authenticated_user = User(
        id=str(generate_object_id()),
        provider_id='1234',
        name='Test',
        last_name='Last',
        email='test@email.com'
    )
    path_user_id = str(generate_object_id())
    mock_repository = MagicMock()
    mock_repository.get_by_id.side_effect = NotExistentUserError()

    with pytest.raises(HTTPException):
        get_path_user_id(path_user_id, authenticated_user, mock_repository)


