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
from window import VideoWindow

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
        glib.threads_init()
        gobject.threads_init()
        gst.init(None)

        # Vars
        self.is_running = True
        self.current_id = -1
        self.current_url = ""
        self.current_stream = None
        self.session = Livestreamer()
        self.player = None

    def run(self):
        # Graphics stuff. Start last!
        glib.timeout_add(500, self.run_checks)
        self.window = VideoWindow()
        self.window.run()

    def run_checks(self):
        if not self.is_running:
            return False

        self.test_skip()
        self.test_next()
        return True

    def test_skip(self):
        # Check for skips
        if self.current_id != -1 and self.player:
            skips = req_skips(self.current_id)
            if 'skip' in skips and skips['skip']:
                print("Skipping video {0} / '{1}'".format(self.current_id, self.current_url))
                self.player.stop()

    def test_next(self):
        if not self.player or not self.player.is_playing():
            video = req_video()
            if 'state' in video and video['state'] == 1:
                self.current_id = video['id']
                self.current_url = video['url']

                print("Switching to video {0} / '{1}'".format(self.current_id, self.current_url))

                try:
                    streams = self.session.streams(self.current_url)
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
                self.player = LivestreamerPlayer(self.window)
                if not self.player.play(self.current_stream):
                    print("Failed to start playback.")
                else:
                    print("Playback started.")

    def close(self):
        self.is_running = False
        if self.player:
            self.player.stop()

if __name__ == "__main__":
    streamer = Streamer()

    def sigint_handler(signal, frame):
        streamer.close()
    signal.signal(signal.SIGINT, sigint_handler)
    
    streamer.run()

    print("Quitting ...")
    exit(0)
