from django.conf.urls import patterns, include, url
from core.shortcuts import redirect_static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'roboconf.views.home', name='home'),
    # url(r'^roboconf/', include('roboconf.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', 'core.views.index', name='index'),
    url(r'^favicon.ico$', redirect_static('img/SITCON.ico'), name='favicon'),
    url(r'^users$', 'users.views.default'),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^docs/', include('docs.urls', namespace='docs')),
    url(r'^issues/', include('issues.urls', namespace='issues')),
    url(r'^agenda/', include('agenda.urls', namespace='agenda')),
    url(r'^notifications/', include('notifications.urls', namespace='notifications')),
    url(r'^api/', include('api.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),# not used since we don't need authentication to access API
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^400$', 'django.views.defaults.bad_request'),
    url(r'^403$', 'django.views.defaults.permission_denied'),
    url(r'^404$', 'django.views.defaults.page_not_found'),
    url(r'^500$', 'django.views.defaults.server_error'),

    # Uncomment the next line to enable the admin:
    url(r'^backend/', include(admin.site.urls)),
)
