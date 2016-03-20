from django.conf.urls import patterns, url
from agenda import views

urlpatterns = [
    url(r'^$', views.main, name='main'),
]
