from django import template

register = template.Library()

@register.filter
def formateach(iterable, format):
    return [format % i for i in iterable]

@register.filter
def escapecsv(iterable):
    return [r'"%s"' % unicode(i).replace(r'"', r'""') for i in iterable]

@register.filter
def escapevcard(str):
    chars_to_replace = (
        (',', '\\,'),
        (';', '\\;'),
        ('\n', '\\n'),
    )
    for src, dest in chars_to_replace:
        str = str.replace(src, dest)
    return str
