from rest_framework import serializers


class CharField(serializers.CharField):

    def run_validation(self, data):
        value = super().run_validation(data)
        if not isinstance(data, str):
            self.fail('invalid')
        return value