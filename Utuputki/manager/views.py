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

def linklist(request):
    response = render_to_response("manager/list.txt", {
        'playlist': Video.objects.all().order_by('id'),
    }, context_instance=RequestContext(request))
    
    response['Content-Type'] = 'text/csv'
    response['Content-Disposition'] = 'attachment; filename="linklist.csv"'
    return response

def index(request):
    oldies = Video.objects.filter(deleted=True).order_by('-id')[:5]
    playlist = Video.objects.filter(deleted=False).order_by('id')
    
    try:
        current = Video.objects.get(playing=True)
    except Video.DoesNotExist:
        current = None
    
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
        'playlist': playlist,
        'oldies': oldies,
        'addform': addform,
        'current': current,
    }, context_instance=RequestContext(request))
    