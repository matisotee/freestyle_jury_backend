from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_meets_djongo.fields import ObjectIdField

from competition.exceptions import CompetitionPastDateError
from competition.services.competition_creator import CompetitionCreator

from authentication.authenticator import FirebaseAuthentication


class OrganizerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=25)
    last_name = serializers.CharField(max_length=25)
    aka = serializers.CharField(max_length=25, required=False)
    _id = ObjectIdField()


class CreateCompetitionSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    date = serializers.DateTimeField(write_only=True)
    status = serializers.CharField(max_length=255, read_only=True)
    open_inscription_during_competition = serializers.BooleanField(write_only=True)
    organizer = OrganizerSerializer(write_only=True)

    def create(self, validated_data):
        user_dict = validated_data.get('organizer')
        name = validated_data.get('name')
        date = validated_data.get('date')
        is_inscription_open_during_competition = validated_data.get(
            'open_inscription_during_competition'
        )
        return CompetitionCreator.create_competition(
            user_dict,
            name,
            date,
            is_inscription_open_during_competition
        )


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
        except CompetitionPastDateError:
            raise ValidationError('Date: set a current or future date', code='PAST_DATE')
        competition = serializer.data

        return Response(competition, status=status.HTTP_201_CREATED)
