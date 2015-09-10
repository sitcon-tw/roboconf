import md5
import os.path
from django.db import models
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils.timezone import now

def photo_path(instance, filename):
    _, ext = os.path.splitext(filename)
    hash_value = md5.new(instance.display_name.encode('utf8') + now().isoformat()).hexdigest()
    return u'photos/{}{}'.format(hash_value, ext)

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    display_name = models.CharField(max_length=16)
    title = models.CharField(max_length=16)
    school = models.CharField(max_length=32, default='', help_text='school or company')
    grade = models.CharField(max_length=32, default='', help_text='department and grade / position')
    phone = models.CharField(max_length=16, default='')
    photo = models.FileField(upload_to=photo_path)
    bio = models.TextField(max_length=320, default='', help_text='biography')
    residence = models.CharField(max_length=16, default='', help_text='residence')
    shirt_size = models.CharField(max_length=8, default='', help_text='T-shirt size')
    diet = models.CharField(max_length=8, default='')

    comment = models.TextField(default='')

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
        return ('https://secure.gravatar.com/avatar/%s?d=identicon' % hash_value)

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

class RegisterToken(models.Model):
    """
    valid:  flag for current token can use or not
    user:   after registration, the token will link to the user.
            Team leader can trace the usage of tokens.
    group:  User registered by token is belongs to.
    """
    token = models.CharField(max_length=12, default=get_random_string)
    group = models.ForeignKey(GroupCategory)
    valid = models.BooleanField(default=True)
    user = models.ForeignKey(User, default=None, null=True)
