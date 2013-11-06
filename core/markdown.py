import misaka as m

BASE_EXTENSIONS = m.EXT_FENCED_CODE | m.EXT_AUTOLINK | m.EXT_STRIKETHROUGH | m.EXT_SPACE_HEADERS

def render_inline(text, autoescape=True):
	return m.html(text, 
		extensions=BASE_EXTENSIONS,
		render_flags=(m.HTML_ESCAPE if autoescape else None) | m.HTML_HARD_WRAP,
	)

def render_document(text):
	return m.html(text,
		extensions=m.EXT_TABLES | BASE_EXTENSIONS,
		render_flags=None,
	)
