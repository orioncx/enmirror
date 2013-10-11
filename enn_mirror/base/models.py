import re
import urllib
import urllib2
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import signals
import os
import cookielib
import random

# Create your models here.
from django import forms

# cj = cookielib.LWPCookieJar("c_cookie.txt")
# cj = cookielib.MozillaCookieJar("c_cookie.txt")
import time,datetime
import threading
from enn_mirror.base.page_replace import get_auto_refresh_code


LOCKS = {}

headers = {'User-Agent': 'Mozilla/6.0 (X11; XUbuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0',
           "Connection": "keep-alive"}



class MirrorObjectAbstract(models.Model):
    domain = models.CharField(max_length=20, help_text="demo.en.cx")
    code = models.CharField(max_length=10, unique=True, help_text="1 to 10 latin chars or digits")
    login = models.CharField(max_length=30, help_text="you login in encounter")
    password = models.CharField(max_length=30, help_text="you password in encounter")
    game_id = models.IntegerField(help_text="example: 41502 (for http://gomel.en.cx/GameDetails.aspx?gid=41502)")

    is_sturm = models.BooleanField(default=False)
    current_level = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True


class MirrorObject(MirrorObjectAbstract):
    def __unicode__(self):
        current_site = Site.objects.get_current()

        return "game link: http://%s/GameDetails.aspx?gid=%s  mirror link: http://%s/play/%s/" % (
            self.domain, self.game_id, current_site.domain, self.code)


class AutoRefreshMirror(MirrorObjectAbstract):
    current_page = models.TextField(max_length=999999, blank=True)
    last_update = models.DateTimeField(default=datetime.datetime.now())
    delet = models.BooleanField(default=False)

    def __unicode__(self):
        current_site = Site.objects.get_current()

        return "game link: http://%s/GameDetails.aspx?gid=%s  mirror link: http://%s/auto_play/%s/" % (
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


def _server_refresh(mirror):
    host = "http://%s/gameengines/encounter/play/%s/?rnd=%s" % (mirror.domain, mirror.game_id, random.random())
    cj = cookielib.MozillaCookieJar(filename="enn_mirror/cookies/%s.txt" % mirror.code)
    cj.load(ignore_discard=True, ignore_expires=True)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    headers.update({"Referer": "http://%s/gameengines/encounter/play/%s/" % (mirror.domain, mirror.game_id),
                    "Host": "%s" % mirror.domain, })
    conn = urllib2.Request(host, None, headers)
    data = opener.open(conn)
    cj.save(ignore_discard=True, ignore_expires=True)
    game_page = data.read()
    game_page = game_page.decode("utf8", "replace")
    if max(game_page.find("error"), game_page.find("padT20"), game_page.find("loginRu")) != -1:
        _login(mirror)
        print "relogin"
        return 1
    if not mirror.is_sturm:
        try:
            mirror.current_level = re.search("\?level=\d+", game_page).group()[7:]
            mirror.save()
        except:
            mirror.is_sturm = True
    lust_script_pos = game_page.rfind("</script>")+45

    game_page = game_page.replace("/GameStat.aspx?gid=%s" % mirror.game_id,
                                  "http://%s/GameStat.aspx?gid=%s" % (
                                      mirror.domain, mirror.game_id)) \
        .replace(
        "/gameengines/encounter/play/%s/" % mirror.game_id, "") \
        .replace("/LevelStat.aspx", "http://%s/LevelStat.aspx" % mirror.domain) \
        .replace("/GameDetails.aspx?gid=", "http://%s/GameDetails.aspx?gid=" % mirror.domain) \
        .replace("/guestbook/messages.aspx?topic=", "http://%s/guestbook/messages.aspx?topic=" % mirror.domain)
    if not mirror.is_sturm:
        game_page = "%s"%get_auto_refresh_code(mirror.code, mirror.current_level) \
            .join([game_page[:lust_script_pos], game_page[lust_script_pos:]])
    mirror.current_page = game_page
    mirror.save()
    return 0

def server_refresh(instance):
    while True:
        time.sleep(1)
        try:
            LOCKS[instance.code].acquire()
            mirror = AutoRefreshMirror.objects.get(pk=instance.pk)
            _server_refresh(mirror)
            print "refreshed-->%s"%datetime.datetime.now()
            LOCKS[instance.code].release()
        except: # deleted
            print "breaked"
            return 0


def login_mirror(sender, instance, created, raw, using, **kwargs):
    if created:
        _login(instance)
    # t1 = threading.Thread(target=server_refresh, args=(instance,))
    # t1.start()


def login_mirror_and_refresh_start(sender, instance, created, raw, using, **kwargs):
    if created:
        _login(instance)
        lock = threading.Lock()
        LOCKS[instance.code] = lock
        t1 = threading.Thread(target=server_refresh, args=(instance,))
        t1.start()


def login_mirror_and_refresh_stop(sender, instance, using, **kwargs):
    if instance.code in LOCKS:
        LOCKS[instance.code].acquire()


def login_mirror_and_refresh_delete(sender, instance, using, **kwargs):
    if instance.code in LOCKS:
        LOCKS[instance.code].release()
        del LOCKS[instance.code]


def delete_cookie(sender, instance, using, **kwargs):
    try:
        os.remove("enn_mirror/cookies/%s.txt" % instance.code)
    except:
        pass

signals.post_save.connect(login_mirror, sender=MirrorObject)
signals.post_save.connect(login_mirror_and_refresh_start, sender=AutoRefreshMirror)
signals.pre_delete.connect(delete_cookie, sender=MirrorObject)
signals.pre_delete.connect(login_mirror_and_refresh_stop, sender=AutoRefreshMirror)
signals.post_delete.connect(login_mirror_and_refresh_delete, sender=AutoRefreshMirror)