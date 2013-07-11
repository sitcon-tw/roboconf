from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	title = models.CharField(max_length=16)
	school = models.CharField(max_length=32, blank=true, help_text='school or company')
	grade = models.CharField(max_length=32, blank=true, help_text='department and grade / position')
	phone = models.CharField(max_length=16, blank=true)
	comment = models.TextField(blank=true)
