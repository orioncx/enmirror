__author__ = 'orion'
from django.contrib import admin
from models import MirrorObject, TempMirror, Key, AutoRefreshMirror, LogRequest


class AutoRefreshMirrorAdmin(admin.ModelAdmin):
    list_display = ['domain', 'login', 'game_id', 'current_level', 'link']


admin.site.register(MirrorObject, AutoRefreshMirrorAdmin)
admin.site.register(TempMirror)
admin.site.register(Key)
admin.site.register(AutoRefreshMirror, AutoRefreshMirrorAdmin)
admin.site.register(LogRequest)
