from django.conf.urls import patterns, url
from issues import views

urlpatterns = patterns('',
		url(r'^$', views.list, name='list'),
		url(r'^new$', views.create, name='create'),
		url(r'^(?P<issue_id>\d+)$', views.detail, name='detail'),
		url(r'^assigned/(?P<user_id>\d+)$', views.assigned, name='assigned'),
		url(r'^created/(?P<user_id>\d+)$', views.created, name='created'),
		url(r'^starred/(?P<user_id>\d+)$', views.starred, name='starred'),
	)
