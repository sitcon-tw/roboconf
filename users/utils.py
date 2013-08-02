from users.models import *

def get_user_name(user):
	try:
		display_name = user.profile.display_name
		if display_name: return display_name
	except UserProfile.DoesNotExist:
		pass
	return user.username

def validate_email(email):
	# TODO: Use regular expression?
	i = email.find('@')
	return i and (i == email.rfind('@')) and (i < email.rfind('.')) and (email.find(' ') < 0)
