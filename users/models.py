import md5
import os.path
from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils.timezone import now


def photo_path(instance, filename):
    _, ext = os.path.splitext(filename)
    hash_value = md5.new(instance.display_name.encode('utf8') + now().isoformat()).hexdigest()
    return u'photos/{}{}'.format(hash_value, ext)

class abilities(models.Model):
    english = models.BooleanField(default=False)
    japanese = models.BooleanField(default=False)
    taiwanese = models.BooleanField(default=False)
    cantonese = models.BooleanField(default=False)

class language(models.Model):
    english = models.BooleanField(default=False)
    japanese = models.BooleanField(default=False)
    taiwanese = models.BooleanField(default=False)
    cantonese = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    display_name = models.CharField(max_length=16)
    title = models.CharField(max_length=16)
    school = models.CharField(max_length=32, default='', help_text='school or company', blank=True)
    grade = models.CharField(max_length=32, default='', help_text='department and grade / position', blank=True)
    phone = models.CharField(max_length=16, default='', blank=True)
    photo = models.FileField(upload_to=photo_path)
    bio = models.TextField(max_length=320, default='', help_text='biography', blank=True)

    residence = models.CharField(max_length=16, default='', help_text='residence', blank=True)
    shirt_size = models.CharField(max_length=8, default='', help_text='T-shirt size', blank=True)
    diet = models.CharField(max_length=8, default='', blank=True)
    transportation = models.CharField(max_length=64, default='', help_text='way to transport', blank=True)
    transportation_fee = models.CharField(max_length=64, default='', help_text='transportation fee', blank=True)
    accom = models.IntegerFieldField(choices=((0, 'Not needed'), (1, 'Either'), (2, 'Needed')), help_text='need for accommodation', null=True, blank=True, default=None)
    roommate = models.ForeignKey(User, help_text='requested roommate', default=None, null=True, blank=True, related_name='+')
    cel_dinner = models.BooleanField(help_text='need for celebratory dinner', blank=True)
    language = models.ForeignKey(language, help_text='language abilities', related_name='+', blank=True, default=None, null=True)
    abilities = models.ForeignKey(abilities, help_text='other abilities', related_name='+', blank=True, default=None, null=True)
    prev_worker = models.BooleanField(blank=True, help_text='if is previously a SITCON worker', default=None, null=True)

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

	def has_submission(self):
		return True if self.user.submissions.count() > 0 else False

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

signals.post_save.connect(create_user_profile, sender=User)

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
    title = models.CharField(max_length=255, default="")
    token = models.CharField(max_length=12, default=get_random_string)
    groups = models.ManyToManyField(Group, related_name='tokens')
    valid = models.BooleanField(default=True)
    user = models.ForeignKey(User, default=None, null=True, blank=True)
