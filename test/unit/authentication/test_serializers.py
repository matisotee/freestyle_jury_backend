from unittest.mock import patch

from authentication.models import User
from authentication.serializers import RegisterUserSerializer


@patch('authentication.serializers.Serializer.validate')
@patch.object(User, 'objects')
def test_validate(mock_objects, mock_validate):

    payload = {
        'name': 'test',
        'last_name': 'user',
        'aka': 'aka',
        'token': 'token'
    }
    mock_validate.return_value = payload
    serializer = RegisterUserSerializer()

    serializer.validate(payload)

    assert mock_validate.called
    mock_objects.create_user_by_token.assert_called_with(
        name='test', last_name='user', token='token', aka='aka'
    )
