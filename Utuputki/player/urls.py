# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    'Utuputki.player.views',
    url(r'^$', 'index', name="index"),
    url(r'^next/', 'find_next', name="next"),
)
