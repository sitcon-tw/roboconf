from django.conf.urls import patterns, url
from schedule import views

urlpatterns = patterns('',
        url(r'^activity/api$', views.activity.api.all, name='api_activity_api_all'),
    )
