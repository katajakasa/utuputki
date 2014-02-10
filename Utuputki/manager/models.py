# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class Video(models.Model):
    description = models.TextField(_('Description'), help_text=_('Description text for the video'), blank=True)
    youtube_url = models.URLField(_('Youtube URL'), help_text=_("URL to a youtube video"))
    ip = models.IPAddressField(_('Sender IP'), blank=True, null=True)
    deleted = models.IntegerField(_('Deleted'), default=False)
    playing = models.BooleanField(_('Playing'), default=False)

    def __unicode__(self):
        return self.description
    
    class Meta:
        verbose_name=_("Video")
        verbose_name_plural=_("Videos")

class SkipRequest(models.Model):
    event = models.ForeignKey(Video, verbose_name=_('Video'))
    ip = models.IPAddressField(_('Sender IP'))
    
    def __unicode__(self):
        return self.event.description

    class Meta:
        verbose_name=_("Skip request")
        verbose_name_plural=_("Skip requests")

try:
    admin.site.register(Video)
    admin.site.register(SkipRequest)
except:
    pass
