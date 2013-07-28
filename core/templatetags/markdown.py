from django import template
from django.utils.safestring import mark_safe
from core.markdown import get_markdown

register = template.Library()

@register.filter(needs_autoescape=True)
def markdown(value, autoescape=None):
	return mark_safe(get_markdown(value, autoescape=autoescape))
