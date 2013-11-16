from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class File(models.Model):

	nid_namespace = 'F'

	class Meta:
		app_label = 'docs'
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

	def nid(self):
		from docs.utils import get_uid
		return get_uid(File, self.id)

	def __unicode__(self):
		return self.name
