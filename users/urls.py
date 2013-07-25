from django.conf.urls import patterns, url
from users import views

urlpatterns = patterns('',
		url(r'^$', views.list, name='list'),
		url(r'^login$', views.login, name='login'),
		url(r'^logout$', views.logout, name='logout'),
		url(r'^(?P<id>\d+)$', views.profile, name='profile'),
	)
