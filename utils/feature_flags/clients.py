from django.conf import settings
from optimizely import optimizely

# FEATURE FLAG CLIENT CONTRACT
# class FeatureFlags:
#
#     def is_feature_enabled(self, feature_flag_key, user_dict=None):
#
#     def get_feature_variable(self, feature_flag_key, variable_key, user_dict=None):


class OptimizelyFeatureFlags:

    @classmethod
    def get_client_and_optimizely_parameters(cls, user_dict):
        client = optimizely.Optimizely(sdk_key=settings.OPTIMIZELY_SDK_KEY)
        user_id = ''

        if user_dict:
            user_id = user_dict.pop('id')

        return client, user_id, user_dict

    @classmethod
    def is_feature_enabled(cls, feature_flag_key, user_dict=None):
        client, user_id, user_dict = cls.get_client_and_optimizely_parameters(user_dict)

        return client.is_feature_enabled(
            feature_flag_key, user_id, attributes=user_dict
        )

    @classmethod
    def get_feature_variable(cls, feature_flag_key, variable_key, user_dict=None):
        client, user_id, user_dict = cls.get_client_and_optimizely_parameters(user_dict)

        return client.get_feature_variable(
            feature_flag_key, variable_key, user_id, attributes=user_dict
        )


class FeatureFlagManager:
    """Wrapper to use any Feature flag client"""

    feature_flag_client = OptimizelyFeatureFlags

    @classmethod
    def is_feature_enabled(cls, feature_flag_key, user_dict=None):
        return cls.feature_flag_client.is_feature_enabled(
            feature_flag_key,
            user_dict=user_dict
        )

    @classmethod
    def get_feature_variable(cls, feature_flag_key, variable_key, user_dict=None):
        return cls.feature_flag_client.get_feature_variable(
            feature_flag_key,
            variable_key,
            user_dict=user_dict
        )
