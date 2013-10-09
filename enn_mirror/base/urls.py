__author__ = 'root'
from views import view_game, dyn_mirror, gen_new_key, mirror, auto_up
from django.conf.urls import patterns,  url

urlpatterns = patterns('',

    url(r'^play/(?P<code>[a-z0-9_]{3,10})/$', view_game,name="view_game"),
    url(r'^auto_up/(?P<code>[a-z0-9_]{3,10})/(?P<level_id>[a-z0-9_]{1,3})/$', auto_up,name="auto_up"),
    url(r'^mirror_data/$', dyn_mirror, name="mirror_data"),
    url(r'^mirror/$', mirror, name="mirror"),
    url(r'^gen_new_key/$', gen_new_key, name="gen_new_key"),
)