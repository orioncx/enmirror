import cookielib
import re
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
import simplejson
from enn_mirror.base.models import _login, headers
from forms import MirrorAdminForm
from models import MirrorObject, TempMirror, Key
import urllib
import urllib2
import time

from page_replace import get_auto_refresh_code



# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))


@csrf_exempt
def admin(request):
    c_code = request.POST.get("code")
    if c_code:
        MirrorObject.objects.filter(code=c_code).delete()
    form = MirrorAdminForm(request.POST or None)
    message = ""
    if form.is_valid():
        mirror = form.save()
        if not _login(mirror):
            message = "Successfully created."
        else:
            message = "Create fail. Please check domain availability, game id and login\pass"
    return TemplateResponse(request, template="en_mirror/admin.html", context={"form":form,"message":message})


@csrf_exempt
def view_game(request, code):
    mirror = get_object_or_404(MirrorObject, code=code)
    host = "http://%s/gameengines/encounter/play/%s/?%s" % (mirror.domain, mirror.game_id, urllib.urlencode(request.GET))
    cj = cookielib.MozillaCookieJar(filename="enn_mirror/cookies/%s.txt" % mirror.code)
    cj.load(ignore_discard=True, ignore_expires=True)

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    post_arr = request.POST.items()
    post_dict = {}
    for i in post_arr:
        post_dict.update({i[0]: i[1].encode('utf8')})

    # post_dict.update({'Login': '%s' % mirror.login,
    #                   'password': '%s' % mirror.password,
    #                   'btnLogin': 0})

    headers.update({"Referer": "http://%s/gameengines/encounter/play/%s/" % (mirror.domain, mirror.game_id),
                    "Host": "%s" % mirror.domain, })
    conn = urllib2.Request(host, (urllib.urlencode(post_dict) or None), headers)

    data = opener.open(conn)
    cj.save(ignore_discard=True, ignore_expires=True)
    game_page = data.read()
    game_page = game_page.decode("utf8", "replace")
    if game_page.find("error") != -1 or game_page.find("padT20") != -1:
        _login(mirror)
        return view_game(request, code)

    if not mirror.is_sturm:
        mirror.current_level = re.search("\?level=\d+", game_page).group()[7:]
        mirror.save()

    lust_script_pos = game_page.rfind("</script>")+45

    game_page = game_page.replace("/GameStat.aspx?gid=%s" % mirror.game_id,
                                  "http://%s/GameStat.aspx?gid=%s" % (
                                      mirror.domain, mirror.game_id)) \
        .replace(
        "/gameengines/encounter/play/%s/" % mirror.game_id, "") \
        .replace("/LevelStat.aspx", "http://%s/LevelStat.aspx" % mirror.domain)\
        .replace("/GameDetails.aspx?gid=", "http://%s/GameDetails.aspx?gid=" % mirror.domain)\
        .replace("/guestbook/messages.aspx?topic=", "http://%s/guestbook/messages.aspx?topic=" % mirror.domain)
    if not mirror.is_sturm:
        game_page = "%s"%get_auto_refresh_code(code, mirror.current_level)\
        .join([game_page[:lust_script_pos], game_page[lust_script_pos:]])
    # game_page = "<-->".join([game_page[:lust_script_pos], game_page[lust_script_pos:]])

    response = HttpResponse(game_page)
    return response


@csrf_exempt
def dyn_mirror(request):
    r_dict = {}
    mirr = TempMirror.objects.all()[0]
    mirr.content = request.POST.get("content", " ")
    mirr.history = request.POST.get("history", " ")
    mirr.save()
    r_dict = {}
    if Key.objects.filter(sent=False).count():
        keys = Key.objects.filter(sent=False)
        keys_arr = [key.value for key in keys]
        r_dict["key_arr"] = keys_arr
        keys.update(sent=True)
    json = simplejson.dumps(r_dict, ensure_ascii=False)
    response = HttpResponse(json, mimetype="application/json")
    XS_SHARING_ALLOWED_ORIGINS = "chrome-extension://ookhjnjamhmchjfofoojpdmgimpehhei"
    XS_SHARING_ALLOWED_METHODS = ['POST', 'GET', 'OPTIONS', 'PUT', 'DELETE']
    response['Access-Control-Allow-Origin'] = XS_SHARING_ALLOWED_ORIGINS
    response['Access-Control-Allow-Methods'] = ",".join(XS_SHARING_ALLOWED_METHODS)
    response[
        'Access-Control-Allow-Headers'] = "Content-Type, Depth, User-Agent, X-File-Size, X-Requested-With, If-Modified-Since, X-File-Name, Cache-Control"
    return response


def mirror(request):
    mirr = TempMirror.objects.all()[0]

    return TemplateResponse(request, template="en_mirror/mirror.html",
                            context={"content": urllib.unquote(mirr.content.encode('ascii')).decode("utf8"), "history": urllib.unquote(mirr.history.encode('ascii')).decode("utf8")})

@csrf_exempt
def gen_new_key(request):
    key = Key()
    key.value = request.POST.get("answer", None)
    if key.value:
        key.save()
    return HttpResponse("Ok")


def auto_up(request, code, level_id):
    timeout = 60 * 3
    while timeout:
        mirror = get_object_or_404(MirrorObject, code=code)
        if str(level_id) == str(mirror.current_level):
            time.sleep(1)
            timeout -= 1
        else:
            return HttpResponse(mirror.current_level)

    return HttpResponse(level_id)