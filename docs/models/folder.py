from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Folder(models.Model):

	class Meta:
		app_label = 'docs'
		nid_namespace = 'D'
		ordering = ['name']

	name = models.CharField(max_length=256)
	parent = models.ForeignKey('self', null=True, related_name='folders')
	last_modified = models.DateTimeField(editable=False, default=now)
	permissions = models.ManyToManyField('Permission', related_name='folderperm+')
	
	# == Version control ==
	is_archived = models.BooleanField(default=False)
	starring = models.ManyToManyField(User, related_name='starred_folders')

	# == Linkbacks from other models ==
	# folders (OneToManyField to self)
	# files (OneToManyField to File)

	def path(self):
		node = self
		path = [self]
		while node.parent:
			node = node.parent
			path.append(node)
		path.reverse()
		return path

	def nid(self):
		from docs.utils import get_uid
		return get_uid(Folder, self.id)

	def __unicode__(self):
		return self.name
