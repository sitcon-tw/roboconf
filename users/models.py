# -*- coding: utf-8 -*-
import os.path
from hashlib import md5
from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils.timezone import now


def photo_path(instance, filename):
    _, ext = os.path.splitext(filename)
    hash_value = md5.new(instance.display_name.encode('utf8') + now().isoformat()).hexdigest()
    return 'photos/{}{}'.format(hash_value, ext)


class abilities(models.Model):
    medical = models.BooleanField(default=False, verbose_name='醫療')
    legal = models.BooleanField(default=False, verbose_name='法律')
    pr = models.BooleanField(default=False, verbose_name='公關')
    other = models.CharField(max_length=64, default='', help_text='other special abilities', blank=True)

class language(models.Model):
    english = models.BooleanField(default=False, verbose_name='英語')
    japanese = models.BooleanField(default=False, verbose_name='日語')
    taiwanese = models.BooleanField(default=False, verbose_name='台語')
    cantonese = models.BooleanField(default=False, verbose_name='粵語')
    other = models.CharField(max_length=64, default='', help_text='other language abilities', blank=True)

class UserProfile(models.Model):
    class Meta:
        permissions = (
                ('view_profile_detail', 'View profile detail'),#TODO fixture
            )

    user = models.OneToOneField(User, related_name='profile')
    photo = models.FileField(upload_to=photo_path, blank=True)

    display_name = models.CharField(max_length=16, blank=True)
    title = models.CharField(max_length=16)
    school = models.CharField(max_length=32, default='', help_text='school or company', blank=True)
    grade = models.CharField(max_length=32, default='', help_text='department and grade / position', blank=True)
    gender = models.IntegerField(choices=((1, 'Male'), (2, 'Female'), (9, 'Other')), help_text='', blank=True, null=True)
    personal_id = models.CharField(max_length=16, blank=True, default='')
    twenty = models.BooleanField(help_text='if age >= 20', default=True)
    phone = models.CharField(max_length=16, default='', blank=True)
    residence = models.CharField(max_length=16, default='', help_text='residence', blank=True)
    shirt_size = models.CharField(max_length=8, default='', help_text='T-shirt size', blank=True)
    diet = models.CharField(max_length=8, default='', blank=True)
    transportation_aid = models.BooleanField(help_text='if need transportation fee aid', default=False)
    transportation_hr = models.BooleanField(help_text='if transportation time >= 1hr', default=False)
    transportation = models.CharField(max_length=64, default='', help_text='transportation method', blank=True)
    transportation_fee = models.CharField(max_length=64, default='', help_text='transportation fee', blank=True)
    accom = models.IntegerField(choices=((0, 'Not needed'), (1, 'Either'), (2, 'Needed')), help_text='need for accommodation', default=0)
    roommate = models.ForeignKey(User, help_text='requested roommate', default=None, null=True, blank=True, related_name='+')
    certificate = models.NullBooleanField(help_text='need for certificate', blank=True, null=True)
    cel_dinner = models.NullBooleanField(help_text='need for celebratory dinner', blank=True, null=True)
    prev_worker = models.BooleanField(help_text='if is previously a SITCON worker', default=False)
    language = models.OneToOneField(language, help_text='language abilities', related_name='+', blank=True, default=None, null=True)
    abilities = models.OneToOneField(abilities, help_text='other abilities', related_name='+', blank=True, default=None, null=True)
    bio = models.TextField(max_length=320, default='', help_text='biography', blank=True)
    comment = models.TextField(default='', blank=True)

    def __str__(self):
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
        hash_value = md5(self.user.email.strip().lower().encode()).hexdigest()
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

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

signals.post_save.connect(create_user_profile, sender=User)

class GroupCategory(models.Model):
    name = models.CharField(max_length=30)
    is_visible = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group, related_name='categories')

    def __str__(self):
        return self.name


class RegisterToken(models.Model):
    """
    valid:  flag for current token can use or not
    user:   after registration, the token will link to the user.
            Team leader can trace the usage of tokens.
    group:  User registered by token is belongs to.
    """
    title = models.CharField(max_length=255, default="")
    token = models.CharField(max_length=12, default=get_random_string)
    groups = models.ManyToManyField(Group, related_name='tokens')
    valid = models.BooleanField(default=True)
    user = models.ForeignKey(User, default=None, null=True, blank=True)

    def __str__(self):
        return '%s - %s' % (self.title, self.token)
