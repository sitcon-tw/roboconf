from django.db import models

class Room(models.Model):
    shortname = models.CharField(max_length=5, help_text='Short room name')
    fullname = models.CharField(max_length=40, help_text='Full room name')

    def __unicode__(self):
        return self.shortname

class Timeslot(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()

class Activity(models.Model):
    description = models.TextField(default='N/A')
    timeslot = models.ForeignKey(Timeslot)
    room = models.ForeignKey(Room, blank=True, null=True)
    submission = models.OneToOneField('submission.Submission', blank=True, null=True)
