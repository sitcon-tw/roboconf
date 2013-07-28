from django.conf import settings

def get_setting(category, value, default=None):
	return settings.NOTIFICATIONS[category].get(value, default)
