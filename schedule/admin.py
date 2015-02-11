from django.contrib import admin
from schedule.models import *
from schedule.models import Room
import copy

class ActivityAdmin(admin.ModelAdmin):
    actions = ['copy_activity', 'propagate_all_rooms']

    def copy_activity(self, request, queryset):
        for a in queryset:
            a_copy = copy.copy(a)
            a_copy.pk = None
            a_copy.submission = None
            a_copy.save()

    def propagate_all_rooms(self, request, queryset):
        for a in queryset:
            for r in Room.objects.all():
                if not a.room == r:
                    a_copy = copy.copy(a)
                    a_copy.pk = None
                    a_copy.submission = None
                    a_copy.room = r
                    a_copy.save()

admin.site.register(Activity, ActivityAdmin)
admin.site.register(Timeslot)
admin.site.register(Room)
