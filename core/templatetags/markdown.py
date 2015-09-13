from django import template
from django.utils.safestring import mark_safe
from core.formatting import render_inline

register = template.Library()

@register.filter(needs_autoescape=True)
def markdown(value, autoescape=None):
    return mark_safe(render_inline(value, autoescape=autoescape))
