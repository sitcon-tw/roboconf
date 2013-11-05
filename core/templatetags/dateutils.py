from django import template
from django.utils.timezone import now, localtime

register = template.Library()

@register.filter(is_safe=True)
def smartdate(date):
	delta = now() - date
	local = localtime(now())
	localdate = localtime(date)
	if delta.seconds < 60:
		return u'\u4e0d\u4e45\u524d'
	if delta.days < 1 and localdate.day >= local.day:
		return '%d:%d' % (localdate.hour, localdate.minute)
	if local.year >= localdate.year:
		return u'%d\u6708%d\u65e5' % (localtime.year, localdate.month)
	return localdate.strftime('%x')
