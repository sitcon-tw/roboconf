from django.conf.urls import patterns, include, url
from sitconstaff.shortcuts import redirect_static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sitconstaff.views.home', name='home'),
    # url(r'^sitconstaff/', include('sitconstaff.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', 'core.views.index', name='index'),
    url(r'^favicon.ico$', redirect_static('img/SITCON.ico'), name='favicon'),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^issues/', include('issues.urls', namespace='issues')),
    url(r'^backend/', include(admin.site.urls)),
)
