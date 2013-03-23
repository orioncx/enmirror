__author__ = 'root'
from views import  admin,view_game
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^admin/$',admin,name="admin"),
    url(r'^play/(?P<code>[a-z0-9_]{3,10})/$', view_game,name="view_game"),
)