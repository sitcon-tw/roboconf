from django.conf.urls import patterns, url
from docs import views

urlpatterns = patterns('',
		url(r'^$', views.main, name='main'),
		url(r'^new$', views.create, name='create'),
		url(r'^view/(?P<identifier>[0-9A-Za-z_\-]+)$', views.render, name='render'),
		url(r'^(?P<nidb64>[0-9A-Za-z_\-]+)$', views.view, name='view'),
	)
