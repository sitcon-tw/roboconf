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

def iter_perms(fileobj):
	acl, node = [], fileobj
	while node:
		acl = sorted(node.permissions.all(), key=Permission.__key__)
		for i in acl: yield i
		node = node.parent

def get_perms(user, fileobj):
	max_perm = len(PRIORITY)-1
	cur_perm = -1

	# Propagate through file nodes
	for perm in iter_perms(fileobj):
		priority = PRIORITY_MAPPING.get(perm.type)
		if priority is None: continue
		if not is_in_scope(user, perm): continue

		if perm.effect == Permission.ALLOW:
			cur_perm = min(max(priority, cur_perm), max_perm)	# Grant highest permission underneath max (denied) perms
		elif perm.effect == Permission.DENY:
			max_perm = min(priority, max_perm)-1 				# Restrict max permission

	return PRIORITY[:cur_perm+1]

def has_perm(user, fileobj, perm_type):
	perm_priority = PRIORITY_MAPPING.get(perm_type)
	if perm_priority is None: return False		# Support builtin permissions only

	# Propagate through file nodes
	for perm in iter_perms(fileobj):
		if not is_in_scope(user, perm): continue

		if perm.effect == Permission.ALLOW:
			if perm_priority <= PRIORITY_MAPPING.get(perm.type, -1):
				return True
		elif perm.effect == Permission.DENY:
			if perm_priority >= PRIORITY_MAPPING.get(perm.type, PRIORITY_COUNT):
				return False

	return False
