from django.contrib import admin

from competition.models.competition import Competition
from competition.models.organizer import Organizer

admin.site.register(Organizer)
admin.site.register(Competition)
