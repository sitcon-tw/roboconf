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
