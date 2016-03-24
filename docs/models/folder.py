from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Folder(models.Model):

    nid_namespace = 'D'

    class Meta:
        app_label = 'docs'
        ordering = ['name']

    name = models.CharField(max_length=256)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='folders')
    last_modified = models.DateTimeField(editable=False, default=now)
    permissions = models.ManyToManyField('Permission', related_name='folderperm+')

    # == Version control ==
    is_archived = models.BooleanField(default=False)
    starring = models.ManyToManyField(User, null=True, blank=True, related_name='starred_folders')

    # == Linkbacks from other models ==
    # folders (OneToManyField to self)
    # files (OneToManyField to File)

    def __str__(self):
        return self.name
