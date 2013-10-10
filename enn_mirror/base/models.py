import re
import urllib
import urllib2
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import signals
import os
import cookielib

# Create your models here.
from django import forms

# cj = cookielib.LWPCookieJar("c_cookie.txt")
# cj = cookielib.MozillaCookieJar("c_cookie.txt")
headers = {'User-Agent': 'Mozilla/6.0 (X11; XUbuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0',
           "Connection": "keep-alive"}


class MirrorObject(models.Model):
    domain = models.CharField(max_length=20, help_text="demo.en.cx")
    code = models.CharField(max_length=10, unique=True, help_text="1 to 10 latin chars or digits")
    login = models.CharField(max_length=30, help_text="you login in encounter")
    password = models.CharField(max_length=30, help_text="you password in encounter")
    game_id = models.IntegerField(help_text="example: 41502 (for http://gomel.en.cx/GameDetails.aspx?gid=41502)")

    is_sturm = models.BooleanField(default=False)
    current_level = models.IntegerField(null=True,blank=True)

    def __unicode__(self):
        current_site = Site.objects.get_current()

        return "game link: http://%s/GameDetails.aspx?gid=%s  mirror link: http://%s/play/%s/" % (
        self.domain, self.game_id, current_site.domain, self.code)


class TempMirror(models.Model):
    history = models.CharField(max_length=40000)
    content = models.CharField(max_length=90000)


class Key(models.Model):
    value = models.CharField(max_length=1000)
    sent = models.BooleanField(default=False)
    inp = models.BooleanField(default=False)


def _login(model):
    cj = cookielib.MozillaCookieJar("c_cookie.txt")
    host = "".join(['http://%s/Login.aspx' % model.domain, '?return=%2FDefault.aspx&lang=ru'])
    ddlNetwork = 1
    if model.domain.find("quest.ua") != -1: #not sure that is that required
        ddlNetwork = 2
    post = urllib.urlencode({'Login': '%s' % model.login,
                             'password': '%s' % model.password,
                             'ddlNetwork': ddlNetwork, #not sure that is that required
                             'btnLogin': 0})

    conn = urllib2.Request(host, post, headers)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    # urllib2.install_opener(opener)
    data = opener.open(conn)
    cj.save(filename="enn_mirror/cookies/%s.txt" % model.code)

    game_page = data.read()

    game_page = game_page.decode("utf8", "replace")
    if game_page.find("error") != -1:
        return 1
    cj.save(filename="enn_mirror/cookies/%s.txt" % model.code, ignore_discard=True, ignore_expires=True)
    return 0


def login_mirror(sender, instance, created, raw, using, **kwargs):
    if created:
        _login(instance)



def delete_cookie(sender, instance, using, **kwargs):
    try:
        os.remove("enn_mirror/cookies/%s.txt" % instance.code)
    except:
        pass

signals.post_save.connect(login_mirror, sender=MirrorObject)
signals.pre_delete.connect(delete_cookie, sender=MirrorObject)