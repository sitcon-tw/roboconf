from django.conf import settings

def get_setting(category, value, default=None):
	return settings.NOTIFICATIONS[category].get(value, default)

def get_realname(user):
	return '%s %s' % (user.last_name, user.first_name)
