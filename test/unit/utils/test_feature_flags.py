from unittest.mock import patch, MagicMock

from django.test import TestCase

from utils.feature_flags.clients import OptimizelyFeatureFlags, FeatureFlagManager


class OptimizelyFeatureFlagsTest(TestCase):

    @patch('utils.feature_flags.clients.optimizely')
    def test_get_client_and_optimizely_parameters_without_user(self, mock_optimizely):
        mock_optimizely.Optimizely.return_value = 'client'

        result = OptimizelyFeatureFlags.get_client_and_optimizely_parameters(None)

        self.assertEqual(result, ('client', '', None))

    @patch('utils.feature_flags.clients.optimizely')
    def test_get_client_and_optimizely_parameters_with_user(self, mock_optimizely):
        mock_optimizely.Optimizely.return_value = 'client'

        result = OptimizelyFeatureFlags.get_client_and_optimizely_parameters(
            {'id': '1234', 'data': 'test_data'}
        )

        self.assertEqual(result, ('client', '1234', {'data': 'test_data'}))

    @patch.object(OptimizelyFeatureFlags, 'get_client_and_optimizely_parameters')
    def test_is_feature_enabled(self, mock_get_client_and_params):
        mock_get_client_and_params.return_value = (MagicMock(), MagicMock(), MagicMock())
        client = mock_get_client_and_params.return_value[0]

        OptimizelyFeatureFlags.is_feature_enabled('test')

        self.assertTrue(client.is_feature_enabled.called)

    @patch.object(OptimizelyFeatureFlags, 'get_client_and_optimizely_parameters')
    def test_get_feature_variable(self, mock_get_client_and_params):
        mock_get_client_and_params.return_value = (MagicMock(), MagicMock(), MagicMock())
        client = mock_get_client_and_params.return_value[0]

        OptimizelyFeatureFlags.get_feature_variable('test', 'test')

        self.assertTrue(client.get_feature_variable.called)


class FeatureFlagManagerTest(TestCase):

    def test_is_feature_enabled(self):
        FeatureFlagManager.feature_flag_client = MagicMock()

        FeatureFlagManager.is_feature_enabled('test')

        self.assertTrue(
            FeatureFlagManager.feature_flag_client.is_feature_enabled.called
        )

    def test_get_feature_variable(self):
        FeatureFlagManager.feature_flag_client = MagicMock()

        FeatureFlagManager.get_feature_variable('test', 'test')

        self.assertTrue(
            FeatureFlagManager.feature_flag_client.get_feature_variable.called
        )
