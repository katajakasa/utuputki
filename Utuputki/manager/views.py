# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from Utuputki.common.responses import JSONResponse

from Utuputki.manager.models import Video,SkipRequest
from Utuputki.manager.forms import AddForm

def request_skip(request):
    ip = request.META['REMOTE_ADDR']
    try:
        current = Video.objects.get(playing=True)
    except Video.DoesNotExist:
        return JSONResponse({'error': 1})
    
    try:
        SkipRequest.objects.get(ip=ip,event=current)
    except SkipRequest.DoesNotExist:
        req = SkipRequest()
        req.ip = ip
        req.event = current
        req.save()
        return JSONResponse({'error': 0})
    
    return JSONResponse({'error': 2})

def get_data(request):
    outlist = {
        'current': None,
        'playlist': [],
        'old': [],
        'skips': 0,
        'error': 0,
    }
    
    try:
        current = Video.objects.get(playing=True)
        outlist['current'] = {
            'id': current.id,
            'ip': current.ip,
            'description': current.description,
            'youtube_url': current.youtube_url
        }
        skipreqs = SkipRequest.objects.filter(event=current)
        outlist['skips'] = len(skipreqs)
    except Video.DoesNotExist:
        outlist['current'] = None
    
    # Old videos
    for v in Video.objects.filter(deleted=True).order_by('-id')[:5]:
        o = {
            'id': v.id,
            'description': v.description,
            'youtube_url': v.youtube_url,
            'ip': v.ip,
        }
        outlist['old'].append(o)
    
    # Old videos
    for v in Video.objects.filter(deleted=False).order_by('id'):
        o = {
            'id': v.id,
            'description': v.description,
            'youtube_url': v.youtube_url,
            'ip': v.ip,
        }
        outlist['playlist'].append(o)

    return JSONResponse(outlist)

def linklist(request):
    response = render_to_response("manager/list.txt", {
        'playlist': Video.objects.all().order_by('id'),
    }, context_instance=RequestContext(request))
    
    response['Content-Type'] = 'text/csv'
    response['Content-Disposition'] = 'attachment; filename="linklist.csv"'
    return response

def index(request):
    ip = request.META['REMOTE_ADDR']
    if request.method == "POST":
        addform = AddForm(request.POST, ip=ip)
        if addform.is_valid():
            d = addform.save(commit=False)
            d.ip = ip
            d.description = addform.tmp_desc
            d.save()
            return HttpResponseRedirect(reverse('manager:index'))
    else:
        addform = AddForm(ip=ip)
    
    return render_to_response("manager/index.html", {
        'addform': addform,
    }, context_instance=RequestContext(request))
    