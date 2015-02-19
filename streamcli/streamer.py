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
import gi
import livestreamer
import json
import httplib
import time
import signal
from player import LivestreamerPlayer
from gi.repository import GObject as gobject, Gst as gst

class NetException(Exception):
    """ Exception for interwebs errors """
    pass

# Globals nom
is_playing = False

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

def sigint_handler(signal, frame):
    is_running = False

# Do stuff.
def main():
    # Init
    gi.require_version("Gst", "1.0")
    gobject.threads_init()
    gst.init(None)
    
    # Vars
    is_running = True
    current_id = -1
    current_url = ""
    session = livestreamer.Livestreamer()
    current_stream = None
    player = LivestreamerPlayer()
    
    # Just run until CTRL+C
    while is_running:
        is_playing = (player and player.is_playing)
        if is_playing:
            skips = req_skips(current_id)
            if 'skip' in skips and  skips['skip'] == 1:
                print("Skipping video {0} / '{1}'".format(current_id, current_url))
                if player:
                    player.stop()
        else:
            video = req_video()
            if 'state' in video and video['state'] == 1:
                current_id = video['id']
                current_url = video['url']
                
                print("Switching to video {0} / '{1}'".format(current_id, current_url))
                
                try:
                    streams = session.streams(video['url'])
                except NoPluginError:
                    print("Livestreamer is unable to handle video {0} / '{1}'".format(current_id, current_url))
                except PluginError as err:
                    print("Livestreamer plugin error: {0}".format(err))
                
                # Make sure there are streams available
                if not streams:
                    print("Livestreamer found no streams {0} / '{1}'".format(current_id, current_url))
                
                # Pick the stream we want
                current_stream = streams[config.QUALITY]
                if not current_stream:
                    print("There was no stream of quality '{0}' available on {1} / {2}".format(config.QUALITY, current_id, current_url))
                
                player.play(current_stream)
        
        time.sleep(0.1)
    
if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint_handler)
    main()
    print("Quitting ...")
    exit(0)
