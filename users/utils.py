from django.core.exceptions import ObjectDoesNotExist

def get_user_name(user):
	try:
		display_name = user.profile.display_name
		if display_name: return display_name
	except ObjectDoesNotExist:
		pass
	return user.username
