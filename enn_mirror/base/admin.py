__author__ = 'orion'
from django.contrib import admin
from models import MirrorObject, TempMirror, Key, AutoRefreshMirror

admin.site.register(MirrorObject)
admin.site.register(TempMirror)
admin.site.register(Key)
admin.site.register(AutoRefreshMirror)


