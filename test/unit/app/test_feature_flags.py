from unittest.mock import patch, MagicMock

from app.feature_flags import OptimizelyFeatureFlags, FeatureFlagManager


# OptimizelyFeatureFlagsTest

@patch('app.feature_flags.optimizely')
def test_get_client_and_optimizely_parameters_without_user(mock_optimizely):
    mock_optimizely.Optimizely.return_value = 'client'

    result = OptimizelyFeatureFlags.get_client_and_optimizely_parameters(None)

    assert result == ('client', '', None)


@patch('app.feature_flags.optimizely')
def test_get_client_and_optimizely_parameters_with_user(mock_optimizely):
    mock_optimizely.Optimizely.return_value = 'client'

    result = OptimizelyFeatureFlags.get_client_and_optimizely_parameters(
        {'id': '1234', 'data': 'test_data'}
    )

    assert result == ('client', '1234', {'data': 'test_data'})


@patch.object(OptimizelyFeatureFlags, 'get_client_and_optimizely_parameters')
def test_is_feature_enabled(mock_get_client_and_params):
    mock_get_client_and_params.return_value = (MagicMock(), MagicMock(), MagicMock())
    client = mock_get_client_and_params.return_value[0]

    OptimizelyFeatureFlags.is_feature_enabled('test')

    assert client.is_feature_enabled.called


@patch.object(OptimizelyFeatureFlags, 'get_client_and_optimizely_parameters')
def test_get_feature_variable(mock_get_client_and_params):
    mock_get_client_and_params.return_value = (MagicMock(), MagicMock(), MagicMock())
    client = mock_get_client_and_params.return_value[0]

    OptimizelyFeatureFlags.get_feature_variable('test', 'test')

    assert client.get_feature_variable.called


# FeatureFlagManagerTest

def test_manager_is_feature_enabled():
    FeatureFlagManager.feature_flag_client = MagicMock()

    FeatureFlagManager.is_feature_enabled('test')

    assert FeatureFlagManager.feature_flag_client.is_feature_enabled.called


def test_manager_get_feature_variable():
    FeatureFlagManager.feature_flag_client = MagicMock()

    FeatureFlagManager.get_feature_variable('test', 'test')

    assert FeatureFlagManager.feature_flag_client.get_feature_variable.called
