# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from Utuputki.common.responses import JSONResponse
from Utuputki.manager.models import Video

def index(request):
    return render_to_response("player/index.html", {}, context_instance=RequestContext(request))

def find_next(request):
    fnext = Video.objects.filter(deleted=False).order_by('id')[0:1]
    if len(fnext) == 0:
        return JSONResponse({'state': 0})
    else:
        murl = fnext[0].youtube_url
        fnext[0].deleted = True
        fnext[0].save()
        return JSONResponse({'state': 1, 'url': murl})