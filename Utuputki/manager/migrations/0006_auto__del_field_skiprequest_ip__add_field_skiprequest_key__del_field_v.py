# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'SkipRequest.ip'
        db.delete_column(u'manager_skiprequest', 'ip')

        # Adding field 'SkipRequest.key'
        db.add_column(u'manager_skiprequest', 'key',
                      self.gf('django.db.models.fields.CharField')(default=u'', max_length=64),
                      keep_default=False)

        # Deleting field 'Video.ip'
        db.delete_column(u'manager_video', 'ip')

        # Adding field 'Video.key'
        db.add_column(u'manager_video', 'key',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'SkipRequest.ip'
        db.add_column(u'manager_skiprequest', 'ip',
                      self.gf('django.db.models.fields.IPAddressField')(default=u'', max_length=15),
                      keep_default=False)

        # Deleting field 'SkipRequest.key'
        db.delete_column(u'manager_skiprequest', 'key')

        # Adding field 'Video.ip'
        db.add_column(u'manager_video', 'ip',
                      self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Video.key'
        db.delete_column(u'manager_video', 'key')


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'playing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'youtube_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['manager']