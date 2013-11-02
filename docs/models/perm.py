from django.db import models
from django.contrib.auth.models import User, Group

class Permission(models.Model):

	VIEW = '1'
	COMMENT = '2'
	EDIT = '3'

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

	def __key__(self):
		# Returns the sorting key for comparision functions
		# Permissions with lower priority (granularity) goes first
		return '%s%s%s' % (self.scope, self.type, self.effect)

	TYPE_NAMES = {
		VIEW: 'VIEW',
		COMMENT: 'COMMENT',
		EDIT: 'EDIT',
	}

	EFFECT_NAMES = {
		ALLOW: 'ALLOW',
		DENY: 'DENY',
	}

	SCOPE_NAMES = {
		PUBLIC: '*',
		INTERNAL: 'STAFF',
		PROTECTED: 'ADMIN',
		PER_GROUP: 'GROUP',
		PER_USER: 'USER',
	}

	def __unicde__(self):
		return '%s:%s %s%s %s' % (
				__key__(self), 
				EFFECT_NAMES.get(self.effect, '?'),
				SCOPE_NAMES.get(self.scope, '?'),
				(' %s' % self.target) if self.target else '',
				TYPE_NAMES.get(self.type, '?'),
			)
