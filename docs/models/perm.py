from django.db import models
from django.contrib.auth.models import User, Group

class Permission(models.Model):

	VIEW = 'V'
	COMMENT = 'M'
	EDIT = 'E'

	ALLOW = 'A'
	DENY = 'D'

	PUBLIC = '0'
	INTERNAL = '1'
	PROTECTED = '2'
	PER_GROUP = 'G'
	PER_USER = 'U'

	TYPE_CHOICES = (
			(VIEW, 'View document'), 
			(COMMENT, 'Comment on document'), 
			(EDIT, 'Edit document'),
		)

	EFFECT_CHOICES = (
			(ALLOW, 'Allow'),
			(DENY, 'Deny'),
		)

	SCOPE_CHOICES = (
			(PUBLIC, 'Public'),
			(INTERNAL, 'Staff'),
			(PROTECTED, 'Administrators'),
			(PER_GROUP, 'Specify group'),
			(PER_USER, 'Specify user'),
		)

	type = models.CharField(max_length=1, choices=TYPE_CHOICES)
	effect = models.CharField(max_length=1, choices=EFFECT_CHOICES)
	scope = models.CharField(max_length=1, choices=SCOPE_CHOICES)
	target = models.IntegerField(blank=True, null=True)

	def target_user(self):
		if not self.scope == PER_USER:
			return None
		return User.objects.get(id=self.target)

	def target_group(self):
		if not self.scope == PER_GROUP:
			return None
		return Group.objects.get(id=self.target)
