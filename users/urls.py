from django.conf.urls import patterns, url
from users import views

urlpatterns = patterns('',
		url(r'^$', views.list, name='list'),
		url(r'^login$', views.login, name='login'),
		url(r'^logout$', views.logout, name='logout'),
		url(r'^new$', views.create, name='create'),
		url(r'^password/change$', views.change_password, name='change_password'),
		url(r'^password/reset$', views.reset_password, name='reset_password'),
		url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z\-]+)$', views.reset_password_confirm, name='reset_password_confirm'),
		url(r'^(?P<id>\d+)$', views.profile, name='profile'),
		url(r'^(?P<id>\d+)/edit$', views.edit, name='edit'),
		url(r'^contacts$', views.contacts, name='contacts'),
		url(r'^api$', views.api, name='api'),
	)
