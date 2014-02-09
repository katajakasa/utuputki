# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'Utuputki.manager.views',
    url(r'^$', 'index', name="index"),
    url(r'^linklist/', 'linklist', name="linklist"),
    url(r'^reqskip/', 'request_skip', name="reqskip"),
)
