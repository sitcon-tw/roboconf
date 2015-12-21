from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import User
from schedule.models import Room

def file_path(instance, filename):
    return u'submission_files/{} - {}'.format(
            instance.submission.title,
            filename)

# Paper submission
class Submission(models.Model):
    class Meta:
        permissions = (
            ('review', 'Review submissions'),
        )
    SHORT = 'S'
    LONG = 'L'
    LIGHTNING = 'N'
    KEYNOTE = 'K'
    SUBMISSION_TYPES = (
            (SHORT, 'Short talk'),
            (LONG, 'Talk'),
            (LIGHTNING, 'Lightning talk'),
            (KEYNOTE, 'Keynote'),
        )

    ACCEPTED = 'A'
    REJECTED = 'R'
    PENDING = 'P'
    REVIEWING = 'V'
    EDITING = 'E'
    ENDED = 'Z'
    STATUS = (
            (ACCEPTED, 'Accepted'),
            (REJECTED, 'Rejected'),
            (PENDING, 'Pending'),
            (REVIEWING, 'Reviewing'),
            (EDITING, 'Editing'),
            (ENDED, 'Ended'),
        )

    user = models.ForeignKey(User, related_name='submissions')
    title = models.CharField(max_length=40, unique=True)
    type = models.CharField(max_length=1, choices=SUBMISSION_TYPES, default=SHORT)
    abstract = models.TextField(max_length=500)
    details = models.TextField(blank=True)
    status = models.CharField(max_length=1, choices=STATUS, default=PENDING)
    comment = models.TextField(blank=True, help_text='Review comment')
    slides = models.TextField(blank=True, help_text='links to slides')

    def __unicode__(self):
        return self.title

class SubmissionFile(models.Model):
    submission = models.ForeignKey(Submission, related_name='files')
    file = models.FileField(upload_to=file_path)

    def __unicode__(self):
        return self.file.name

    def url(self):
        return self.file.url

    def name(self):
        return self.file.name.rpartition('/')[2]

class Score(models.Model):
    submission  = models.ForeignKey(Submission, related_name='scores')
    user        = models.ForeignKey(User)
    audience    = models.PositiveIntegerField(validators=[MaxValueValidator(100),MinValueValidator(0)])
    cool        = models.PositiveIntegerField(validators=[MaxValueValidator(100),MinValueValidator(0)])
    expression  = models.PositiveIntegerField(validators=[MaxValueValidator(100),MinValueValidator(0)])
    difficulty  = models.PositiveIntegerField(validators=[MaxValueValidator(100),MinValueValidator(0)])

    class Meta:
        unique_together = ('submission', 'user')
        permissions = (
                ('view_total_score', 'View total score'),
                )

    def __unicode__(self):
        return self.submission.title+" ["+str(self.audience)+" "+str(self.cool)+" "+\
                str(self.expression)+" "+str(self.difficulty)+"] by "+self.user.profile.display_name
