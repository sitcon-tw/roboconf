from django.conf.urls import patterns, url
from docs import views

urlpatterns = patterns('',
		url(r'^$', views.main, name='main'),
		url(r'^folder/(?P<nidb64>[0-9A-Za-z_\-]+)$', views.folder, name='folder'), 
	)
