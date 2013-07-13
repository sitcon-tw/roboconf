from django.conf.urls import patterns, url
from issues import views

urlpatterns = patterns('',
		url(r'^$', views.list, name='list'),
		url(r'^new$', views.create, name='create'),
		url(r'^(?P<id>\d+)$', views.detail, name='detail')
	)
