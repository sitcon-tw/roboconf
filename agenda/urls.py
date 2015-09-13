from django.conf.urls import patterns, url
from agenda import views

urlpatterns = patterns('',
        url(r'^$', views.main, name='main'),
    )
