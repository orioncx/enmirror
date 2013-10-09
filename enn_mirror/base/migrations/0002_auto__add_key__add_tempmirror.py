# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Key'
        db.create_table('base_key', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('inp', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('base', ['Key'])

        # Adding model 'TempMirror'
        db.create_table('base_tempmirror', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history', self.gf('django.db.models.fields.CharField')(max_length=40000)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=90000)),
        ))
        db.send_create_signal('base', ['TempMirror'])


    def backwards(self, orm):
        # Deleting model 'Key'
        db.delete_table('base_key')

        # Deleting model 'TempMirror'
        db.delete_table('base_tempmirror')


    models = {
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
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'game_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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