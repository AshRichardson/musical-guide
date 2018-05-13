from django.contrib import admin

from .models import Participant, Note

admin.site.register(Participant)
admin.site.register(Note)
# admin.site.register(PostQuestionnaire)