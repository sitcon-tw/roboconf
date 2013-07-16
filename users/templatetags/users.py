from django import template
from django.contrib.auth.models import User
import md5

register = template.Library()

@register.filter(is_safe=True)
def get_avatar(value, size=None):
	if size == '#':
		size = 144
	hash_value = md5.new(value.strip().lower()).hexdigest()
	return ('https://secure.gravatar.com/avatar/%s?d=retro' % hash_value) + (('&s=%s' % size) if size else '')

@register.filter(is_safe=True)
def get_username(id):
	try:
		user = User.objects.get(id=id)
		return user.username
	except User.DoesNotExist:
		return id
