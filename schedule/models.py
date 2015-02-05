from django.db import models
from submission.models import Submission, Room

class Timeslot(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()

class Activity(models.Model):
    description = models.TextField(default='N/A')
    timeslot = models.ForeignKey(Timeslot)
    room = models.ForeignKey(Room, blank=True, null=True)
    submission = models.OneToOneField(Submission, blank=True, null=True)
