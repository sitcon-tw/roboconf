from django.db import models
from users.models import User

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
    title = models.CharField(max_length=40)
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
    slide = models.FileField(upload_to='slides')
