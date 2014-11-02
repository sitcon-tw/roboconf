from django.contrib.auth.models import User
from users.models import *

def generate_password():
	from os import urandom
	from base64 import urlsafe_b64encode
	# Generate a password with length 12
	return urlsafe_b64encode(urandom(8))[:-1]

GROUP_PRIORITY = [3, 1, 6, 5, 7, 8, 4, 9, 2, 14, 15, 13, 12, 11, 10]	# Sort by team lead -> staff -> consultant
def get_user_sorting_key(user):
	groups = [g.id for g in user.groups.all()]
	identity = ''.join([str(1 - groups.count(i)) for i in GROUP_PRIORITY])	# Sort by identity first
	title = user.profile.title.ljust(5)
	name = user.profile.name()
	return ''.join((identity, title, name))

def sorted_users(users):
	if not users:
		users = User.objects.filter(is_active=True)
	return sorted(users, key=get_user_sorting_key)

def get_group_sorting_key(category):
	try:
		return GROUP_PRIORITY.index(category.id)
	except ValueError:
		return len(GROUP_PRIORITY)

def sorted_categories():
	return { category : sorted(category.groups.all(), key=get_group_sorting_key) for category in GroupCategory.objects.all() }

def is_authorized_user(user):
	return user.groups.filter(id=11).exists()

def is_trusted_user(user):
	return is_authorized_user() and user.has_perm('auth.change_user')
