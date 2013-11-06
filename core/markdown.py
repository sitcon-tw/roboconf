import markdown as m

inline = m.Markdown(
	extensions=['fenced_code', 'nl2br'],
	safe_mode='escape',
	smart_emphasis=False,	# Prevent problems on Chinese characters
)

docs = m.Markdown(
	extensions=['abbr', 'def_list', 'fenced_code', 'footnotes', 'tables', 'toc', 'nl2br'],
	smart_emphasis=False,	# Prevent problems on Chinese characters
)

def render_inline(text, autoescape=True):
	return inline.convert(text)

def render_document(text):
	return docs.convert(text)
