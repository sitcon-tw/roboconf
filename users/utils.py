from users.models import *
from base64 import urlsafe_b64encode
from os import urandom

def get_user_name(user):
	try:
		display_name = user.profile.display_name
		if display_name: return display_name
	except UserProfile.DoesNotExist:
		pass

	if user.first_name and user.last_name:
		return '%s %s' % (user.last_name, user.first_name)
		
	return user.username

def validate_email(email):
	# TODO: Use regular expression?
	i = email.find('@')
	return i and (i == email.rfind('@')) and (i < email.rfind('.')) and (email.find(' ') < 0)

def generate_password():
	# Generate a password with length 12
	return urlsafe_b64encode(urandom(8))[:-1]

GROUP_PRIORITY = [3, 1, 6, 5, 8, 2, 11]	# Sort by group type, team lead -> staff -> consultant
def get_user_sorting_key(user):
	groups = [g.id for g in user.groups.all()]
	identity = ''.join([str(1 - groups.count(i)) for i in GROUP_PRIORITY])	# Sort by identity first
	title = user.profile.title.ljust(5)
	name = get_user_name(user)
	return ''.join((identity, title, name))
