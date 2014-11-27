from django.db import models
from django.conf import settings
from users.models import User

def file_path(instance, filename):
    return u'{}submission_files/{} - {}'.format(
            settings.MEDIA_ROOT,
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
    SUBMISSION_TYPES = (
            (SHORT, 'Short talk'),
            (LONG, 'Talk'),
            (LIGHTNING, 'Lightning talk'),
        )

    ACCEPTED = 'A'
    REJECTED = 'R'
    PENDING = 'P'
    REVIEWING = 'V'
    STATUS = (
            (ACCEPTED, 'Accepted'),
            (REJECTED, 'Rejected'),
            (PENDING, 'Pending'),
            (REVIEWING, 'Reviewing'),
        )

    user = models.ForeignKey(User, editable=False, related_name='submissions')
    title = models.CharField(max_length=40, unique=True)
    type = models.CharField(max_length=1, choices=SUBMISSION_TYPES, default=SHORT)
    nickname = models.CharField(max_length=100, help_text='nickname')
    bio = models.TextField(max_length=300, help_text='biography')
    avatar = models.CharField(max_length=1000, blank=True, help_text='link to custom avatar image')
    abstract = models.TextField(max_length=500)
    details = models.TextField(blank=True)
    status = models.CharField(max_length=1, choices=STATUS, default=PENDING)
    comment = models.TextField(blank=True, help_text='Review comment')
    departure = models.CharField(max_length=1000, help_text='departure')
    photo = models.FileField(upload_to='photos')

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
