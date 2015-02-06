from django.db import models
from core.settings.base import TIME_ZONE
import pytz

class Room(models.Model):
    shortname = models.CharField(max_length=5, help_text='Short room name')
    fullname = models.CharField(max_length=40, help_text='Full room name')

    def __unicode__(self):
        return self.shortname

class Timeslot(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __unicode__(self):
        return self.start.astimezone(pytz.timezone(TIME_ZONE)).strftime('%x %X') + " duration: " + str(self.end-self.start)

class Activity(models.Model):
    description = models.TextField(default='N/A')
    timeslot = models.ForeignKey(Timeslot)
    room = models.ForeignKey(Room, blank=True, null=True)
    submission = models.OneToOneField('submission.Submission', blank=True, null=True)

    def __unicode__(self):
        retstr = self.timeslot.start.astimezone(pytz.timezone(TIME_ZONE)).strftime('%X') + " "
        retstr += self.submission.title if self.submission else self.description
        retstr += " @ " + self.room.fullname
        return retstr
