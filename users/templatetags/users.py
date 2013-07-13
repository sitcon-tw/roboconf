from django import template
import md5

register = template.Library()

@register.filter(is_safe=True)
def get_avatar(value):
	hash_value = md5.new(value.strip().lower()).hexdigest()
	return 'https://secure.gravatar.com/avatar/%s?s=144&d=retro' % hash_value
