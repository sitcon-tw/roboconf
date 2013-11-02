from models import Permission

def is_in_scope(user, perm):
	if perm.scope == Permission.INTERNAL:
		return user.is_authenticated()
	elif perm.scope == Permission.PROTECTED:
		return user.is_staff
	elif perm.scope == Permission.PER_GROUP:
		return user.groups.filter(id=perm.target).exists()
	elif perm.scope == Permission.PER_USER:
		return user.id == perm.target
	# Permission.PUBLIC
	return True

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

		perm = acl.pop()		# Retrieve entry with highest granularity

		if perms[perm.type] is not None: continue	# First, check if rights has been set
		if not is_in_scope(user, perm): continue	# Then, check if the permission is on right scope

		# Validated permission applicability. Let's fill in the rights
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

def has_perm(user, fileobj, perm_type):
	# Define priority
	priority = dict(enumerate((Permission.VIEW, Permission.COMMENT, Permission.EDIT)))
	perm_priority = priority.get(perm_type, -1)

	# Propagate through file nodes
	acl = sorted(fileobj.permissions.all(), key=Permission.__key__)
	node = fileobj.parent

	while node:
		while len(acl):
			perm = acl.pop()
			if not is_in_scope(user, perm): continue

			if perm.effect == Permission.ALLOW:
				if perm_priority <= priority.get(perm.type, -1):
					return True
			elif perm.effect == Permission.DENY:
				if perm_priority >= priority.get(perm.type, -1):
					return False

		acl = sorted(node.permissions.all(), key=Permission.__key__)
		node = node.parent

	# Not granted in any permission
	return False
