# -*- coding: utf-8 -*-

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder, HTML
from Utuputki.manager.models import Video
from django.utils.translation import ugettext_lazy as _

import urlparse
import httplib
import json

class AddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.session_key = kwargs.pop('session_key', None)
        super(AddForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                _('Add a new video to the playlist'),
                'youtube_url',
                ButtonHolder (
                    HTML('<input type="reset" value="C" />'),
                    Submit('submit', _('Add'))
                )
            )
        )
        
    def exists(self, url):
        pitems = Video.objects.filter(deleted=False, key=self.session_key, youtube_url=url)
        if len(pitems) > 0:
            return True
        return False
        
    def get_video_info(self, id):
        host = 'gdata.youtube.com'
        headers = {'Content-Type': 'application/json',}
        c = httplib.HTTPSConnection(host, timeout=15)
        c.request('GET', '/feeds/api/videos/'+id+'?v=2&alt=jsonc', headers=headers)
        res = c.getresponse()
        message = json.loads(res.read())
        return message
        
    def clean_youtube_url(self):
        self.tmp_desc = u''
        
        # Make sure field has content
        if not self.cleaned_data['youtube_url']:
            return self.cleaned_data['youtube_url']
        
        # Clean up url (trim whitespace etc.)
        url = self.cleaned_data['youtube_url'].strip()
        
        # Check if we already have a valid embed url
        if url.find('http://www.youtube.com/v/') == 0 \
                or url.find('https://www.youtube.com/v/') == 0 \
                or url.find('http://youtu.be/') == 0 \
                or url.find('https://youtu.be/') == 0:
            parsed = urlparse.urlparse(url)
            mpath = parsed.path
            if mpath[-1:] == '/':
                mpath = mpath[:-1]
            segs = mpath.rpartition('/')
            video_id = segs[2]
        else:
            parsed = urlparse.urlparse(url)
            qs = urlparse.parse_qs(parsed.query)
            
            # Check if the video id exists in query string
            if 'v' not in qs:
                raise forms.ValidationError(_('Given URL is not a valid Youtube video URL.'))
            
            # Get video ID
            video_id = qs['v'][0]
        
        # Check if url already exists for this IP
        r_url = 'http://www.youtube.com/v/'+video_id+'/'
        if self.exists(r_url):
            raise forms.ValidationError(_('Given video URL is already once in the playlist with this IP.'))
            
        # Get video information; make sure it is available
        video_info = self.get_video_info(video_id)
        if u'data' in video_info:
            # Make sure video is not restricted
            if u'status' in video_info['data']:
                if u'value' in video_info['data']['status']:
                    if video_info['data']['status']['value'] == 'restricted':
                        raise forms.ValidationError(_('Video is restricted, and cannot be loaded.'))
                
            # Make sure video is embeddable
            if u'accessControl' in video_info['data']:    
                if video_info['data']['accessControl']['embed'] != "allowed":
                    raise forms.ValidationError(_('Embedding this video is not allowed, and thus cannot be loaded.'))
            
            # Make sure the video is not too long
            if u'duration' in video_info['data']:
                duration = int(video_info['data']['duration'])
                if duration > 900:
                    raise forms.ValidationError(_('Video is too long. Maximum length for the video is 15 minutes.'))
            
            # Set temp description
            if u'title' in video_info['data']:
                self.tmp_desc = video_info['data']['title']
            else:
                self.tmp_desc = _('Unavailable')
        else:
            raise forms.ValidationError(_('Video does not exist!'))
            
        # All done. Return valid url
        return r_url
        
    class Meta:
        model = Video
        fields = ('youtube_url',)
