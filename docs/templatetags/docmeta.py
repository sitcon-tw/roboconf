from django import template
from docs.utils import *

register = template.Library()

@register.filter(is_safe=True)
def nid(value):
	return generate_nid(value)
