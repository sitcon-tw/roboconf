from django import template
import misaka as m

register = template.Library()

@register.filter(is_safe=True)
def markdown(value):
	return m.html(value, 
		extensions=m.EXT_FENCED_CODE | m.EXT_AUTOLINK | m.EXT_STRIKETHROUGH | m.EXT_SPACE_HEADERS,
		render_flags=m.HTML_SKIP_HTML,
	)
