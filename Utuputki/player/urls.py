# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'Utuputki.player.views',
    url(r'^$', 'index', name="index"),
    url(r'^next/', 'find_next', name="next"),
    url(r'^checkskip/', 'check_skip', name="checkskip"),
)
