from models import Permission
from django.contrib.auth.models import User, Group

def get_perms(user, fileobj):
	perms = {
		Permission.VIEW: None,
		Permission.COMMENT: None,
		Permission.EDIT: None,
	}

	acl = sorted(fileobj.permissions.all(), key=Permission.__key__)
	node = fileobj.parent

	# Propagate through file nodes
	while None in perms.values():
		# Fill with parent permissions when ran out
		if not len(acl):
			if not node: break
			acl = sorted(node.permissions.all(), key=Permission.__key__)
			node = node.parent

		# Retrieve entry with highest granularity
		perm = acl.pop()

		# First, check if rights has been set
		if perms[perm.type] is not None:
			continue

		# Then, check if the permission is on right scope
		if perm.scope == Permission.INTERNAL:
			if not user.is_authenticated(): continue
		elif perm.scope == Permission.PROTECTED:
			if not user.is_staff: continue
		elif perm.scope == Permission.PER_GROUP:
			if not user.groups.filter(id=perm.target).exists(): continue
		elif perm.scope == Permission.PER_USER:
			if user.id != perm.target: continue

		# Validated permission applicability.
		# Let's fill in the rights

		if perm.effect == Permission.ALLOW:
			perms[perm.type] = True
			# Cascading apply permissions
			if perm.type == Permission.EDIT:
				perms[Permission.VIEW] = True
				perms[Permission.COMMENT] = True
			elif perm.type == Permission.COMMENT:
				perms[Permission.VIEW] = True
		elif perm.effect == Permission.DENY:
			perms[perm.type] = False
			# Do not cascade apply denial since user might be granted lower rights

	# Any rights hasn't been granted is set to False
	for k in perms:
		if perms[k] is None: perms[k] = False

	# Return a dict consists of permission mapping
	return perms
