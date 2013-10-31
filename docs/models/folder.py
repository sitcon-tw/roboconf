from django.db import models
from django.utils.timezone import now

class Folder(models.Model):
	name = models.CharField(max_length=256)
	parent = models.ForeignKey('self', related_name='folders')
	last_modified = models.DateTimeField(editable=False, default=now)
	permissions = models.ManyToManyField('Permission', related_name='perm+')
	
	# == Version control ==
	is_archived = models.BooleanField(default=False)

	# == Linkbacks from other models ==
	# folders (OneToManyField to self)
	# files (OneToManyField to File)
	# watchers (ManyToManyField to User)

	def __unicode__(self):
		return self.name
