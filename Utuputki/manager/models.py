# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin

class Video(models.Model):
    description = models.TextField(u'Kuvaus', help_text=u'Videon kuvaus.', blank=True)
    youtube_url = models.URLField(u'Youtube URL', help_text=u"Linkki teoksen Youtube-versioon.")
    ip = models.IPAddressField(u'Sender IP', blank=True, null=True)
    deleted = models.IntegerField(u'Deleted', default=False)
    playing = models.BooleanField(u'Playing', default=False)

    def __unicode__(self):
        return self.description

class SkipRequest(models.Model):
    event = models.ForeignKey(Video, verbose_name=u'Video')
    ip = models.IPAddressField(u'Sender IP')
    
    def __unicode__(self):
        return self.event.description

try:
    admin.site.register(Video)
    admin.site.register(SkipRequest)
except:
    pass
