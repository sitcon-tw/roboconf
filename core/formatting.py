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

INLINE_TAGS = (
    'a', 'abbr', 'acronym',
    'b', 'blockquote', 'br',
    'code',
	'del',
    'em',
	'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr',
    'i', 'img', 'ins',
    'li',
    'ol',
	'p', 'pre',
    'strong',
	'table', 'td', 'tbody', 'th', 'thead', 'tr',
    'ul',
)

INLINE_ATTRIBUTES = {
	'*': ['class'],
	'a': ['href', 'title'],
	'img': ['src', 'alt', 'width', 'height'],
}

def render_inline(text, autoescape=True):
	text = inline.convert(text)
	if autoescape:
		text = bleach.clean(text, tags=INLINE_TAGS, attributes=INLINE_ATTRIBUTES)
	return text

def render_document(text):
	docs.reset()
	return docs.convert(text)
