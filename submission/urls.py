from django.conf.urls import patterns, url
from submission import views

urlpatterns = patterns('',
        url(r'^$', views.list, name='list'),
        url(r'^new$', views.create, name='create'),
        url(r'^delete$', views.delete, name='delete'),
        url(r'^score/save$', views.score_save, name='score_save'),
        url(r'^score$', views.score, name='score'),
        url(r'^edit/(\d+)$', views.edit, name='edit'),
        url(r'^view/partial/(\d+)$', views.view_partial, name='view_partial'),
        url(r'^view/(\d+)$', views.view, name='view'),
    )
