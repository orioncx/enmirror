# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LogRequest'
        db.create_table(u'base_logrequest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('num', self.gf('django.db.models.fields.IntegerField')()),
            ('user_agent', self.gf('django.db.models.fields.CharField')(max_length=2555, null=True, blank=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 2, 28, 0, 0))),
            ('user_ip', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'base', ['LogRequest'])


    def backwards(self, orm):
        # Deleting model 'LogRequest'
        db.delete_table(u'base_logrequest')


    models = {
        u'base.autorefreshmirror': {
            'Meta': {'object_name': 'AutoRefreshMirror'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'current_level': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'current_page': ('django.db.models.fields.TextField', [], {'max_length': '999999', 'blank': 'True'}),
            'delet': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'game_id': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_sturm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 2, 28, 0, 0)'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'base.key': {
            'Meta': {'object_name': 'Key'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inp': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        u'base.logrequest': {
            'Meta': {'object_name': 'LogRequest'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 2, 28, 0, 0)'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '2555', 'null': 'True', 'blank': 'True'}),
            'user_ip': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'base.mirrorobject': {
            'Meta': {'object_name': 'MirrorObject'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'current_level': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'game_id': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_sturm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'base.tempmirror': {
            'Meta': {'object_name': 'TempMirror'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '90000'}),
            'history': ('django.db.models.fields.CharField', [], {'max_length': '40000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['base']