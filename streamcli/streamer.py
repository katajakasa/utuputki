# -*- coding: utf-8 -*-

# Attempt to find configuration
try:
    import config
except:
    print "Config module not found! Make sure config.py exists!"
    exit()
    
# Others
import os
import sys
import livestreamer
import json
import httplib
import time
import signal

class NetException(Exception):
    """ Exception for interwebs errors """
    pass

def get_json(path):
    """ Fetches JSON response from API """
    conn = httplib.HTTPConnection(config.UTUPUTKI_API_DOMAIN)
    conn.request("GET", path)
    ret = conn.getresponse()
    if ret.status == 200:
        return json.loads(ret.read())
    else:
        raise NetException('Unable to fetch data from server')

def req_video():
    """ Fetches next video from API """
    return get_json(config.UTUPUTKI_API_PATH + '/next/')

def req_skips(id):
    """ Fetches skipping information from API """
    return get_json(config.UTUPUTKI_API_PATH + '/checkskip/?video_id' + str(id))

# Globals nom
is_playing = False
is_running = True
current_id = -1
current_url = ""
session = livestreamer.Livestreamer()
current_stream = None

def sigint_handler(signal, frame):
    is_running = False

signal.signal(signal.SIGINT, sigint_handler)

# Do stuff.
while is_running:
    if is_playing:
        skips = req_skips(current_id)
        if 'skip' in skips and  skips['skip'] == 1:
            print("Skipping video {0} / '{1}'".format(current_id, current_url))
    else:
        video = req_video()
        if video['state'] == 1:
            current_id = video['id']
            current_url = video['url']
            
            print("Switching to video {0} / '{1}'".format(current_id, current_url))
            
            try:
                streams = session.streams(video['url'])
            except NoPluginError:
                print("Livestreamer is unable to handle video {0} / '{1}'".format(current_id, current_url))
            except PluginError as err:
                print("Livestreamer plugin error: {0}".format(err))
                
            current_stream = streams[config.QUALITY]
            is_playing = True
    
    time.sleep(0.1)

print("SIGINT, quitting ...")
exit(0)