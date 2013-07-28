import misaka as m

def get_markdown(text, autoescape=True):
	return m.html(value, 
		extensions=m.EXT_FENCED_CODE | m.EXT_AUTOLINK | m.EXT_STRIKETHROUGH | m.EXT_SPACE_HEADERS,
		render_flags=(m.HTML_ESCAPE if autoescape else None),
	)
