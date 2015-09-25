from django.contrib import admin
from users.models import *

admin.site.register(UserProfile)
admin.site.register(GroupCategory)
admin.site.register(RegisterToken)
admin.site.register(language)
admin.site.register(abilities)

