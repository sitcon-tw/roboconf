from django.contrib import admin
from submission.models import *

admin.site.register(Score)

class SubmissionAdmin(admin.ModelAdmin):
    actions = ['make_editing', 'make_accepted', 'make_rejected', 'make_reviewing', 'make_pending', 'make_ended']
    list_filter = ('type', 'status')

    def make_editing(self, request, queryset):
        queryset.update(status='E')

    def make_accepted(self, request, queryset):
        queryset.update(status='A')

    def make_rejected(self, request, queryset):
        queryset.update(status='R')

    def make_reviewing(self, request, queryset):
        queryset.update(status='V')

    def make_pending(self, request, queryset):
        queryset.update(status='P')

    def make_ended(self, request, queryset):
        queryset.update(status='Z')

admin.site.register(Submission, SubmissionAdmin)
