from django.contrib import admin
from docs.models import *

admin.site.register(Permalink)
admin.site.register(File)
admin.site.register(Folder)
admin.site.register(BlobText)
admin.site.register(Permission)
admin.site.register(Revision)
