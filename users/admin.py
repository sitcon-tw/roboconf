from django.contrib import admin
from users.models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.register(UserProfile)
admin.site.register(GroupCategory)
admin.site.register(RegisterToken)
admin.site.register(language)
admin.site.register(abilities)

class MyUserAdmin(UserAdmin):
    actions = ['disable', 'enable']

    def disable(self, request, queryset):
        queryset.update(is_active=False)

    def enable(self, request, queryset):
        queryset.update(is_active=True)

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
