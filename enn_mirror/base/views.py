from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from forms import MirrorAdminForm
from models import MirrorObject
import urllib,cookielib
import urllib2
import re


cj = cookielib.LWPCookieJar("c_cookie.txt")
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)


headers = {'User-Agent' : 'Mozilla/5.0 (X11; XUbuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0', }


def _login(model):
    host = "".join(['http://%s/Login.aspx'%model.domain,'?return=%2FDefault.aspx&lang=ru'])
    ddlNetwork = 1
    if model.domain.find("quest.ua")!=-1: #not sure that is that required
        ddlNetwork = 2
    post = urllib.urlencode({'Login' : '%s'%model.login,
                                     'password' : '%s'%model.password,
                                     'ddlNetwork' : ddlNetwork, #not sure that is that required
                                     'btnLogin' : 0})
    conn = urllib2.Request(host, post, headers)
    data=urllib2.urlopen(conn)
    game_page = data.read()
    game_page = game_page.decode("utf8","replace")
    if game_page.find("error")!=-1:
        return 1
    cj.save(filename="enn_mirror/cookies/%s.txt"%model.code)
    return 0


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
    return TemplateResponse(request,template="en_mirror/admin.html",context={"form":form,"message":message})

@csrf_exempt
def view_game(request,code):
    mirror = MirrorObject.objects.get(code=code)
    host = "http://%s/gameengines/encounter/play/%s?%s"%(mirror.domain,mirror.game_id,urllib.urlencode(request.GET))
    cj.load(filename="enn_mirror/cookies/%s.txt"%mirror.code)
    conn = urllib2.Request(host, (urllib.urlencode(request.POST) or None), headers)
    data = urllib2.urlopen(conn)
    game_page = data.read()
    game_page = game_page.decode("utf8","replace").replace("/GameStat.aspx?gid=%s"%mirror.game_id,"http://%s/GameStat.aspx?gid=%s"%(mirror.domain,mirror.game_id)).replace("/gameengines/encounter/play/%s/"%mirror.game_id,"")

#    refresh_links = re.findall("\/gameengines\/encounter\/play\/%s\/\?rnd\=0\,[0-9]+"%mirror.game_id,game_page)
#    for refresh_link in refresh_links:
#        game_page=game_page.replace(refresh_link,"")

    if game_page.find("error")!=-1 or game_page.find("padT20")!=-1:
        _login(mirror)
        return view_game(request,code)
    return HttpResponse(game_page)