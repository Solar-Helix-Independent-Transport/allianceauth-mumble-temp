from django.urls import path
from django.conf.urls import url

from . import views


app_name = 'mumbletemps'

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^join/(?P<link_ref>[\w\-]+)/$', views.link, name='join'),
    url(r'^nuke/(?P<link_ref>[\w\-]+)/$', views.nuke, name='nuke'),
]