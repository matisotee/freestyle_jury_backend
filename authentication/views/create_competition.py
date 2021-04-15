from dependency_injector.wiring import (
    Provide, inject,
)
from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from authentication.application.create_competition import CreateCompetitionService
from authentication.application.exceptions import CallServiceError
from authentication.domain.service_caller import ServiceCaller
from authentication.authenticator import FirebaseAuthentication
from authentication.infrastructure.dependency_injection.containers import Container
from authentication.infrastructure.dependency_injection.decorator import wire


class OrganizerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=25)
    last_name = serializers.CharField(max_length=25)
    aka = serializers.CharField(max_length=25, required=False)
    _id = serializers.CharField(max_length=100)


class CreateCompetitionSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    date = serializers.DateTimeField(write_only=True)
    status = serializers.CharField(max_length=255, read_only=True)
    open_inscription_during_competition = serializers.BooleanField(write_only=True)
    organizer = OrganizerSerializer(write_only=True)

    @wire
    @inject
    def create(
        self,
        validated_data: dict,
        service_caller: ServiceCaller = Provide[Container.service_caller]
    ) -> dict:
        service = CreateCompetitionService(service_caller)
        return service.create_competition(validated_data)


class CreateCompetitionView(APIView):
    """Create a new competition"""
    serializer_class = CreateCompetitionSerializer
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        data['organizer'] = request.user.__dict__

        try:
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except CallServiceError as e:
            raise ValidationError(str(e), code=e.code)
        competition = serializer.data

        return Response(competition, status=status.HTTP_201_CREATED)
