from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api_gateway.application.create_competition import CreateCompetitionService
from api_gateway.infrastructure.authentication.django_authentication import DjangoAuthentication
from api_gateway.infrastructure.utils import custom_serializers
from api_gateway.infrastructure.utils.api_views import validate_request_and_response


class CreateCompetitionRequestSerializer(serializers.Serializer):
    name = custom_serializers.CharField(max_length=255)
    date = serializers.DateTimeField()
    open_inscription_during_competition = serializers.BooleanField()


class CreateCompetitionResponseSerializer(serializers.Serializer):
    name = custom_serializers.CharField(max_length=255)
    status = custom_serializers.CharField(max_length=255)


class CreateCompetitionView(APIView):
    """Create a new competition"""
    authentication_classes = [DjangoAuthentication]
    permission_classes = [IsAuthenticated]
    request_serializer_class = CreateCompetitionRequestSerializer
    response_serializer_class = CreateCompetitionResponseSerializer

    @validate_request_and_response
    def post(self, request, *args, **kwargs):

        service = CreateCompetitionService()
        return service.create_competition(
            **request.data, authenticated_user=request.user.__dict__
        )
