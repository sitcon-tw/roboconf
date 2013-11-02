from models import Permission

PRIORITY = (
		Permission.VIEW, 
		Permission.COMMENT, 
		Permission.EDIT,
	)
PRIORITY_COUNT = len(PRIORITY)
PRIORITY_MAPPING = dict(zip(PRIORITY, range(PRIORITY_COUNT)))

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
	perms = dict(zip(PRIORITY, [None] * PRIORITY_COUNT))

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
			priority = PRIORITY_MAPPING.get(perm.type, 0)
			for p in PRIORITY[:priority]:	# Cascading apply permissions
				perms[p] = True

		elif perm.effect == Permission.DENY:
			perms[perm.type] = False
			priority = PRIORITY_MAPPING.get(perm.type, PRIORITY_COUNT)
			for p in PRIORITY[priority+1:]:	# Cascading apply permissions
				perms[p] = False

	# Return a list consists of available permissions
	return [p for p in perms if perms[p]]

def has_perm(user, fileobj, perm_type):
	# Define priority
	perm_priority = PRIORITY_MAPPING.get(perm_type, -1)

	# Propagate through file nodes
	acl = sorted(fileobj.permissions.all(), key=Permission.__key__)
	node = fileobj.parent

	while node:
		while len(acl):
			perm = acl.pop()
			if not is_in_scope(user, perm): continue

			if perm.effect == Permission.ALLOW:
				if perm_priority <= PRIORITY_MAPPING.get(perm.type, -1):
					return True
			elif perm.effect == Permission.DENY:
				if perm_priority >= PRIORITY_MAPPING.get(perm.type, PRIORITY_COUNT):
					return False

		acl = sorted(node.permissions.all(), key=Permission.__key__)
		node = node.parent

	# Not granted in any permission
	return False
