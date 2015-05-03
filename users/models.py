import md5
import os.path
from django.db import models
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.utils.timezone import now

def photo_path(instance, filename):
    _, ext = os.path.splitext(filename)
    hash_value = md5.new(instance.display_name + now().isoformat()).hexdigest()
    return u'photos/{}{}'.format(hash_value, ext)

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    display_name = models.CharField(max_length=16)
    title = models.CharField(max_length=16)
    school = models.CharField(max_length=32, blank=True, help_text='school or company')
    bio = models.TextField(max_length=300, help_text='biography')
    grade = models.CharField(max_length=32, blank=True, help_text='department and grade / position')
    phone = models.CharField(max_length=16, blank=True)
    photo = models.FileField(upload_to=photo_path)
    departure = models.CharField(max_length=10, blank=True, help_text='departure')
    comment = models.TextField(blank=True)

    def __unicode__(self):
        return '%s - %s' % (self.title, self.user.username)

    @property
    def name(self):
        if self.display_name:
            return self.display_name
        elif self.user.first_name and self.user.last_name:
            return '%s %s' % (self.user.last_name, self.user.first_name)
        else:
            return self.user.username

    @property
    def gravatar(self):
        hash_value = md5.new(self.user.email.strip().lower()).hexdigest()
        return ('https://secure.gravatar.com/avatar/%s?d=retro' % hash_value)

    @property
    def avatar(self):
        if not self.photo:
            return self.gravatar
        else:
            return self.photo.url

    def is_authorized(self):
        return self.user.groups.filter(id=settings.STAFF_GROUP_ID).exists()

    def is_trusted(self):
        return self.is_authorized() and self.user.has_perm('auth.change_user')

class GroupCategory(models.Model):
    name = models.CharField(max_length=30)
    is_visible = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group, related_name='categories')

    def __unicode__(self):
        return self.name
