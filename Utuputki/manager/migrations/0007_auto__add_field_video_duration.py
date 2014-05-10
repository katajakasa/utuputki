# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Video.duration'
        db.add_column(u'manager_video', 'duration',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Video.duration'
        db.delete_column(u'manager_video', 'duration')


    models = {
        u'manager.skiprequest': {
            'Meta': {'object_name': 'SkipRequest'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['manager.Video']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'manager.video': {
            'Meta': {'object_name': 'Video'},
            'deleted': ('django.db.models.fields.IntegerField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'playing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'youtube_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['manager']