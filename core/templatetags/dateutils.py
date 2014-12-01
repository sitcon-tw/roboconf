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
		return '%d:%02d' % (localdate.hour, localdate.minute)
	if localdate.year >= local.year:
		return u'%d\u6708%d\u65e5' % (localdate.month, localdate.day)
	return localdate.strftime('%x')
