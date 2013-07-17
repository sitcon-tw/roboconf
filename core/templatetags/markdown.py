from django import template
from django.utils.safestring import mark_safe
import misaka as m

register = template.Library()

@register.filter(needs_autoescape=True)
def markdown(value, autoescape=None):
	return mark_safe(m.html(value, 
		extensions=m.EXT_FENCED_CODE | m.EXT_AUTOLINK | m.EXT_STRIKETHROUGH | m.EXT_SPACE_HEADERS,
		render_flags=(m.HTML_ESCAPE if autoescape else None),
	))
