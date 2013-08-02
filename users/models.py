from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name='profile')
	display_name = models.CharField(max_length=16)
	title = models.CharField(max_length=16, null=True)
	school = models.CharField(max_length=32, null=True, blank=True, help_text='school or company')
	grade = models.CharField(max_length=32, null=True, blank=True, help_text='department and grade / position')
	phone = models.CharField(max_length=16, null=True, blank=True)
	comment = models.TextField(null=True, blank=True)

	def __unicode__(self):
		return self.title
