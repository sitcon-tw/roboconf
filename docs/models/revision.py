from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Revision(models.Model):

	class Meta:
		app_label = 'docs'

	LOCAL = '.'

	TYPE_CHOICES = (
			(LOCAL, 'Local revision'),
		)

	file = models.ForeignKey('File', related_name='revisions')
	type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=LOCAL)
	user = models.ForeignKey(User, editable=False, related_name='doc_revisions')
	timestamp = models.DateTimeField(editable=False, default=now)
	base_revision = models.OneToOneField('self', related_name='derived_revision')
	comment = models.TextField()
	text = models.ForeignKey('BlobText', related_name='revisions')

	# == Linkbacks from other models ==
	# derived_revision (OneToManyField to self)

	def __unicode__(self):
		return '[%s] %s: %s' % (self.timestamp.isoformat(), self.user, self.comment)
