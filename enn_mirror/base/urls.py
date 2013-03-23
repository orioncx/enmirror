__author__ = 'root'
from views import  admin,view_game
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    url(r'^admin/$',admin,name="admin"),
    url(r'^play/(?P<code>[a-z0-9_]{3,10})/$', view_game,name="view_game"),
    url(r'^admin/', include(admin.site.urls)),
)