__author__ = 'root'
from views import view_game, dyn_mirror, gen_new_key, mirror, auto_up, fast_view_game, get_antimirror_img
from django.conf.urls import patterns,  url

urlpatterns = patterns('',

    url(r'^play/(?P<code>[a-z0-9_]{3,10})/$', view_game,name="view_game"),
    url(r'^auto_play/(?P<code>[a-z0-9_]{3,10})/$', fast_view_game,name="fast_view_game"),
    url(r'^auto_up/(?P<code>[a-z0-9_]{3,10})/(?P<level_id>[a-z0-9_]{1,3})/$', auto_up,name="auto_up"),
    url(r'^mirror_data/$', dyn_mirror, name="mirror_data"),
    url(r'^mirror_2389759/$', mirror, name="mirror"),
    url(r'^gen_new_key/$', gen_new_key, name="gen_new_key"),
    url(r'^img/(?P<code>[0-9])/xxxZXcd123123.jpeg$', get_antimirror_img, name="get_antimirror_img"),
)