# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from Utuputki.common.responses import JSONResponse
from Utuputki.manager.models import Video,SkipRequest
from django.conf import settings

def index(request):
    if settings.ENABLE_HTML_PLAYER:
        return render_to_response("player/index.html", {}, context_instance=RequestContext(request))
    else:
        raise Http404("Player is disabled.")

def check_skip(request):
    # Make sure the request is ok
    video_id = -1
    try:
        video_id = request.GET['video_id']
    except:
        return JSONResponse({'error': 1});
    
    doskip = False
    skipreqs = SkipRequest.objects.filter(event_id=video_id)
    if len(skipreqs) > 2:
        doskip = True
    
    return JSONResponse({'error': 0, 'skip': doskip});

def find_next(request):
    # For now, set this here
    # TODO: Make more sophisticated JSON API
    try:
        current = Video.objects.get(playing=True)
        current.playing = False
        current.save()
    except Video.DoesNotExist:
        pass
    
    # Get next
    fnext = Video.objects.filter(deleted=False).order_by('id')[0:1]
    if len(fnext) == 0:
        return JSONResponse({'state': 0})
    else:
        murl = fnext[0].youtube_url
        mid = fnext[0].pk
        fnext[0].deleted = True
        fnext[0].playing = True
        fnext[0].save()
        return JSONResponse({'state': 1, 'url': murl, 'id': mid})
