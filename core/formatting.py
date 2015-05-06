import bleach
import markdown as m

inline = m.Markdown(
	extensions=[
		'markdown.extensions.fenced_code',
		'markdown.extensions.nl2br',
		'markdown.extensions.tables',
		'mdx_del_ins',
		'mdx_linkify.mdx_linkify',
		'users.mentions',
	],
)

docs = m.Markdown(
	extensions=[
		'markdown.extensions.abbr',
		'markdown.extensions.def_list',
		'markdown.extensions.fenced_code',
		'markdown.extensions.footnotes',
		'markdown.extensions.tables',
		'markdown.extensions.toc',
		'markdown.extensions.nl2br',
		'mdx_del_ins',
		'mdx_linkify.mdx_linkify',
		'users.mentions',
	],
)

def render_inline(text, autoescape=True):
	if autoescape:
		text = bleach.clean(text)
	return inline.convert(text)

def render_document(text):
	docs.reset()
	return docs.convert(text)
