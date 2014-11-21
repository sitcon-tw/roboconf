from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.

class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name='profile')
	display_name = models.CharField(max_length=16)
	title = models.CharField(max_length=16)
	school = models.CharField(max_length=32, blank=True, help_text='school or company')
	grade = models.CharField(max_length=32, blank=True, help_text='department and grade / position')
	phone = models.CharField(max_length=16, blank=True)
	comment = models.TextField(blank=True)

	def __unicode__(self):
		return '%s - %s' % (self.title, self.user.username)

	def name(self):
		if self.display_name:
			return self.display_name
		elif self.user.first_name and self.user.last_name:
			return '%s %s' % (self.user.last_name, self.user.first_name)
		else:
			return self.user.username

	def avatar(self):
		import md5
		hash_value = md5.new(self.user.email.strip().lower()).hexdigest()
		return ('https://secure.gravatar.com/avatar/%s?d=retro' % hash_value)

class GroupCategory(models.Model):
	name = models.CharField(max_length=30)
	is_visible = models.BooleanField(default=True)
	groups = models.ManyToManyField(Group, related_name='categories')

	def __unicode__(self):
		return self.name
