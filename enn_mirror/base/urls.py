__author__ = 'root'
from views import view_game, dyn_mirror, gen_new_key, mirror
from django.conf.urls import patterns,  url

urlpatterns = patterns('',

    url(r'^play/(?P<code>[a-z0-9_]{3,10})/$', view_game,name="view_game"),
    url(r'^mirror_data/$', dyn_mirror, name="mirror_data"),
    url(r'^mirror/$', mirror, name="mirror"),
    url(r'^gen_new_key/$', gen_new_key, name="gen_new_key"),
)