from django import template
from users.utils import get_avatar_url, get_user_name

register = template.Library()

@register.filter(is_safe=True)
def get_avatar(value, size=None):
	if size == '#': size = 144
	return get_avatar_url(value) + (('&s=%s' % size) if size else '')

@register.filter(is_safe=True)
def get_name(value):
	return get_user_name(value)
