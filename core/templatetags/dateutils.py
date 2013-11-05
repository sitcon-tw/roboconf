from django import template
from django.utils.timezone import now, localtime

register = template.Library()

@register.filter(is_safe=True)
def smartdate(date):
	delta = now() - date
	local = localtime(now())
	localdate = localtime(date)
	if delta.days < 1 and local.hour >= delta.hours:
		return '%d:%d' % (localdate.hour, localdate.minute)
	if local.year >= localdate.year:
		return u'%d\u6708%d\u65e5' % (localtime.year, localdate.month)
	return localdate.strftime('%x')
