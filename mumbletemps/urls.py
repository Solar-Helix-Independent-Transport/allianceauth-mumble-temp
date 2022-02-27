from django.urls import path, re_path

from . import views


app_name = 'mumbletemps'

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^join/(?P<link_ref>[\w\-]+)/$', views.link, name='join'),
    re_path(r'^nuke/(?P<link_ref>[\w\-]+)/$', views.nuke, name='nuke'),
]