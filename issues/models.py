from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Issue(models.Model):
	OPEN = 'O'
	CLOSED = 'D'
	STATE_CHOICES = (
			(OPEN, 'Open'),
			(CLOSED, 'Closed')
		)

	title = models.CharField(max_length=128)
	creator = models.ForeignKey(User, editable=false)
	creation_time = models.DateTimeField(editable=false)
	state = models.CharField(max_length=1, choices=STATE_CHOICES, default=OPEN)
	assignee = models.ForeignKey(User, blank=true)
	due_time = models.DateTimeField(blank=true)
	content = models.TextField()

class IssueHistory(models.Model):
	user = models.ForeignKey(User, editable=false)
	timestamp = models.DateTimeField()
	comment = models.TextField()
