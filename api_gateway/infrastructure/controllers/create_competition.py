from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api_gateway.application.create_competition import CreateCompetitionService
from api_gateway.application.exceptions.competition import CreateCompetitionError
from api_gateway.infrastructure.authentication.django_authentication import DjangoAuthentication
from api_gateway.infrastructure.controllers.base import BaseAPIView, CharField


class CreateCompetitionRequestSerializer(serializers.Serializer):
    name = CharField(max_length=255)
    date = serializers.DateTimeField()
    open_inscription_during_competition = serializers.BooleanField()


class CreateCompetitionResponseSerializer(serializers.Serializer):
    name = CharField(max_length=255)
    status = CharField(max_length=255)


class CreateCompetitionView(BaseAPIView):
    """Create a new competition"""
    authentication_classes = [DjangoAuthentication]
    permission_classes = [IsAuthenticated]
    request_serializer_class = CreateCompetitionRequestSerializer
    response_serializer_class = CreateCompetitionResponseSerializer

    def post(self, request, *args, **kwargs):

        try:
            service = CreateCompetitionService()
            response = service.create_competition(
                **request.data, authenticated_user=request.user.__dict__
            )
            return Response(response)
        except CreateCompetitionError as e:
            raise ValidationError(e.message, code=e.code)
