# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Video.playing'
        db.add_column(u'manager_video', 'playing',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Video.playing'
        db.delete_column(u'manager_video', 'playing')


    models = {
        u'manager.skiprequest': {
            'Meta': {'object_name': 'SkipRequest'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['manager.Video']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'})
        },
        u'manager.video': {
            'Meta': {'object_name': 'Video'},
            'deleted': ('django.db.models.fields.IntegerField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'playing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'youtube_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['manager']