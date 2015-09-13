from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Revision(models.Model):

    class Meta:
        app_label = 'docs'

    LOCAL = '.'
    EXTERNAL = '+'

    TYPE_CHOICES = (
            (LOCAL, 'Local revision'),
            (EXTERNAL, 'External linked file'),
        )

    file = models.ForeignKey('File', null=True, related_name='revisions')
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=LOCAL)
    user = models.ForeignKey(User, null=True, editable=False, related_name='doc_revisions')
    timestamp = models.DateTimeField(editable=False, default=now)
    base_revision = models.OneToOneField('self', null=True, related_name='derived_revision')
    comment = models.TextField()
    text = models.ForeignKey('BlobText', related_name='revisions')

    # == Linkbacks from other models ==
    # derived_revision (OneToManyField to self)

    def __unicode__(self):
        return '[%s] %s: %s' % (self.timestamp.isoformat(), self.user, self.comment)
