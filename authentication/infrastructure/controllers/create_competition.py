from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from authentication.application.create_competition import CreateCompetitionService
from authentication.application.exceptions import CallServiceError
from authentication.authenticator import FirebaseAuthentication


class CreateCompetitionRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    date = serializers.DateTimeField()
    open_inscription_during_competition = serializers.BooleanField()


class CreateCompetitionResponseSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    status = serializers.CharField(max_length=255)


class CreateCompetitionView(APIView):
    """Create a new competition"""
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        try:
            serializer = CreateCompetitionRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # with validate_request_and_response:
            service = CreateCompetitionService()
            response = service.create_competition(
                **request.data, authenticated_user=request.user.__dict__
            )

            serializer = CreateCompetitionResponseSerializer(data=response)
            serializer.is_valid(raise_exception=True)
        except CallServiceError as e:
            raise ValidationError(e.message, code=e.code)

        return Response(response, status=status.HTTP_201_CREATED)
