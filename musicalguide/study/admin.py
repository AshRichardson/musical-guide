from django.contrib import admin

from .models import Participant, Note, ComputerNote

class NoteAdmin(admin.ModelAdmin):
	list_filter = ('participant', 'interaction', )

class ComputerNoteAdmin(admin.ModelAdmin):
	list_filter = ('participant', 'interaction', )

admin.site.register(Participant)
admin.site.register(Note, NoteAdmin)
admin.site.register(ComputerNote, ComputerNoteAdmin)