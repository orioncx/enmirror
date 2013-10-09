# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MirrorObject.is_sturm'
        db.add_column('base_mirrorobject', 'is_sturm',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'MirrorObject.current_level'
        db.add_column('base_mirrorobject', 'current_level',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'MirrorObject.is_sturm'
        db.delete_column('base_mirrorobject', 'is_sturm')

        # Deleting field 'MirrorObject.current_level'
        db.delete_column('base_mirrorobject', 'current_level')


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