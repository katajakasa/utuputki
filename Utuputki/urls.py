# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

# URLS
urlpatterns = patterns('',
    url(r'^player/', include('Utuputki.player.urls', namespace="player")),
    url(r'^manager/', include('Utuputki.manager.urls', namespace="manager")),
    url(r'^$', include('Utuputki.manager.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)

# Add admin panel link if debug mode is on
# Serve media files through static.serve when running in debug mode
if settings.ENABLE_ADMIN:
    admin.autodiscover()
    urlpatterns += patterns('',
        url(r'^admin/', include(admin.site.urls)),
    )

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )