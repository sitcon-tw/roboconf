from django.conf.urls import patterns, url
from notifications import views

urlpatterns = patterns('',
        url(r'^$', views.list, name='list'),
        url(r'^new$', views.create, name='create'),
    )
