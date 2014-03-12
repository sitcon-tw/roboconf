from django import template

register = template.Library()

@register.filter
def formateach(iterable, format):
	return [format % i for i in iterable]

@register.filter
def escapecsv(iterable):
	return [r'"%s"' % i.replace(r'"', r'""') for i in iterable]
