from django.conf.urls import patterns, url
from issues import views

urlpatterns = patterns('',
		url(r'^$', views.ListView.as_view(), name='list'),
		url(r'^new$', views.create, name='create'),
		url(r'^(?P<id>\d+)$', views.DetailView.as_view(), name='detail')
	)
