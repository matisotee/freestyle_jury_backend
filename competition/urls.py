from django.urls import path

from competition.controllers.create_competition import CreateCompetitionView

app_name = 'competition'

urlpatterns = [
    path('', CreateCompetitionView.as_view(), name='create_competition'),
]
