# -*- coding: utf-8 -*-

# Attempt to find configuration
try:
    import config
except:
    print "Config module not found! Make sure config.py exists!"
    exit()

# Own
from player import LivestreamerPlayer
from query import req_video, req_skips, NetException

# Others
import os
import sys
import gi
import time
import signal
from livestreamer import Livestreamer, NoPluginError, PluginError
from gi.repository import GObject as gobject, Gst as gst, GLib as glib

# Do stuff.
class Streamer(object):
    def __init__(self):
        # Init stuff
        gi.require_version("Gst", "1.0")
        gobject.threads_init()
        glib.threads_init()
        gst.init(None)

        # Vars
        self.is_running = True
        self.current_id = -1
        self.current_url = ""
        self.current_stream = None
        self.session = Livestreamer()
        self.player = LivestreamerPlayer()

        # Start skip watch
        glib.timeout_add(500, self.test_skip)
  
    def test_skip(self):
        if not is_running:
            return False

        # Check for skips
        if self.current_id != -1:
            skips = req_skips(self.current_id)
            if 'skip' in skips and skips['skip']:
                print("Skipping video {0} / '{1}'".format(self.current_id, self.current_url))
                self.player.stop()
        return True

    def main(self):
        # Just run until CTRL+C
        while self.is_running:
            time.sleep(0.2)
            video = req_video()
            if 'state' in video and video['state'] == 1:
                self.current_id = video['id']
                self.current_url = video['url']

                print("Switching to video {0} / '{1}'".format(self.current_id, self.current_url))

                try:
                    streams = self.session.streams(video['url'])
                except NoPluginError:
                    print("Livestreamer is unable to handle video {0} / '{1}'".format(self.current_id, self.current_url))
                except PluginError as err:
                    print("Livestreamer plugin error: {0}".format(err))

                # Make sure there are streams available
                if not streams:
                    print("Livestreamer found no streams {0} / '{1}'".format(self.current_id, self.current_url))

                # Pick the stream we want
                self.current_stream = streams[config.QUALITY]
                if not self.current_stream:
                    print("There was no stream of quality '{0}' available on {1} / {2}".format(config.QUALITY, self.current_id, self.current_url))

                # Play!
                if not self.player.play(self.current_stream):
                    print("Failed to start playback.")

    def close(self):
        self.is_running = False
        self.player.stop()

if __name__ == "__main__":
    streamer = Streamer()

    def sigint_handler(signal, frame):
        streamer.close()
    signal.signal(signal.SIGINT, sigint_handler)
    
    streamer.main()

    print("Quitting ...")
    exit(0)
