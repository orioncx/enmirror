# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MirrorObject'
        pass


    def backwards(self, orm):
        # Deleting model 'MirrorObject'
        pass


    models = {
        'base.mirrorobject': {
            'Meta': {'object_name': 'MirrorObject'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'game_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['base']