from django.db import models
from django.utils.timezone import now

class File(models.Model):

	class Meta:
		permissions = (
			('archive', 'Archive files and folders'),
		)

	# == File system ==
	name = models.CharField(max_length=256)
	parent = models.ForeignKey('Folder', related_name='files')
	last_modified = models.DateTimeField(editable=False, default=now)
	permissions = models.ManyToManyField('Permission', related_name='perm+')
	
	# == Version control ==
	is_archived = models.BooleanField(default=False)
	current_revision = models.ForeignKey('Revision', related_name='currev+', on_delete=models.PROTECT)

	# == Linkbacks from other models ==
	# revisions (OneToManyField to Revision)
	# watchers (ManyToManyField to User)

	def __unicode__(self):
		return self.name
