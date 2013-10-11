# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AutoRefreshMirror'
        db.create_table('base_autorefreshmirror', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
            ('login', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('game_id', self.gf('django.db.models.fields.IntegerField')()),
            ('is_sturm', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('current_level', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('current_page', self.gf('django.db.models.fields.TextField')(max_length=999999)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 10, 11, 0, 0))),
        ))
        db.send_create_signal('base', ['AutoRefreshMirror'])


    def backwards(self, orm):
        # Deleting model 'AutoRefreshMirror'
        db.delete_table('base_autorefreshmirror')


    models = {
        'base.autorefreshmirror': {
            'Meta': {'object_name': 'AutoRefreshMirror'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'current_level': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'current_page': ('django.db.models.fields.TextField', [], {'max_length': '999999'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'game_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_sturm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 11, 0, 0)'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'base.key': {
            'Meta': {'object_name': 'Key'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inp': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        'base.mirrorobject': {
            'Meta': {'object_name': 'MirrorObject'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'current_level': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'game_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_sturm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'base.tempmirror': {
            'Meta': {'object_name': 'TempMirror'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '90000'}),
            'history': ('django.db.models.fields.CharField', [], {'max_length': '40000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['base']