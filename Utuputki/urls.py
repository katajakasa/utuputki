# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings

# Use admin panel, if debug mode is on
if settings.DEBUG:
    admin.autodiscover()

# URLS
urlpatterns = patterns('',
    url(r'^player/', include('Utuputki.player.urls', namespace="player")),
    url(r'^$', include('Utuputki.manager.urls', namespace="manager")),
)

# Add admin panel link if debug mode is on
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^admin/', include(admin.site.urls)),
    )

# Serve media files through static.serve when running in debug mode
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )