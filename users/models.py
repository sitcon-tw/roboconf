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
		return self.title

class GroupCategory(models.Model):
	name = models.CharField(max_length=30)
	is_visible = models.BooleanField(default=True)
	groups = models.ManyToManyField(Group, related_name='categories')

	def __unicode__(self):
		return self.name
