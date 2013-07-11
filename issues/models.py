from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Label(models.Model):
	name = models.CharField(max_length=32)
	color = models.CharField(max_length=6)

class Issue(models.Model):
	title = models.CharField(max_length=128)
	creator = models.ForeignKey(User, editable=False, on_delete=models.SET_NULL)
	creation_time = models.DateTimeField(editable=False)
	is_open = models.BooleanField(default=True)
	assignee = models.ForeignKey(User, blank=True)
	due_time = models.DateTimeField(blank=True)
	labels = models.ManyToManyField(Label)
	content = models.TextField()

class IssueHistory(models.Model):
	COMMENT = '.'
	ASSIGN = 'A'
	CHANGE_STATE = 'S'
	MODE_CHOICES = (
			(COMMENT, 'Commented'),
			(ASSIGN, 'Assigned to'),
			(CHANGE_STATE, 'Changed state')
		)

	issue = models.ForeignKey(Issue, editable=False, related_name='histories')
	user = models.ForeignKey(User, editable=False)
	timestamp = models.DateTimeField(editable=False)
	mode = models.CharField(max_length=1, editable=False, choices=MODE_CHOICES, default=COMMENT)
	affected_value = models.TextField()
	comment = models.TextField()
