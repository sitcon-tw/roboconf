from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class File(models.Model):

	class Meta:
		app_label = 'docs'
		nid_namespace = 'F'
		ordering = ['name']
		permissions = (
			('archive', 'Archive files and folders'),
		)

	# == File system ==
	name = models.CharField(max_length=256)
	parent = models.ForeignKey('Folder', related_name='files')
	last_modified = models.DateTimeField(editable=False, default=now)
	permissions = models.ManyToManyField('Permission', related_name='fileperm+')
	
	# == Version control ==
	is_archived = models.BooleanField(default=False)
	current_revision = models.ForeignKey('Revision', related_name='currev+', on_delete=models.PROTECT)
	starring = models.ManyToManyField(User, related_name='starred_files')

	# == Linkbacks from other models ==
	# revisions (OneToManyField to Revision)

	def __unicode__(self):
		return self.name
