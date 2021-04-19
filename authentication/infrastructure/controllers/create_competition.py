from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from authentication.application.create_competition import CreateCompetitionService
from authentication.application.exceptions import CallServiceError
from authentication.authenticator import FirebaseAuthentication


class CreateCompetitionSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    date = serializers.DateTimeField(write_only=True)
    status = serializers.CharField(max_length=255, read_only=True)
    open_inscription_during_competition = serializers.BooleanField(write_only=True)

    def create(self, validated_data: dict):
        service = CreateCompetitionService()
        return service.create_competition(validated_data)


class CreateCompetitionView(APIView):
    """Create a new competition"""
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        try:
            serializer = CreateCompetitionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(authenticated_user=request.user.__dict__)
        except CallServiceError as e:
            raise ValidationError(e.message, code=e.code)
        competition = serializer.data

        return Response(competition, status=status.HTTP_201_CREATED)
