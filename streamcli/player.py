# -*- coding: utf-8 -*-

import sys
import gi

from gi.repository import GObject as gobject, Gst as gst
from livestreamer import Livestreamer, StreamError

class LivestreamerPlayer(object):
    def __init__(self):
        self.fd = None
        self.mainloop = gobject.MainLoop()
        self.playing = False

        # This creates a playbin pipeline and using the appsrc source
        # we can feed it our stream data
        self.pipeline = gst.ElementFactory.make("playbin", None)
        self.pipeline.set_property("uri", "appsrc://")

        # When the playbin creates the appsrc source it will call
        # this callback and allow us to configure it
        self.pipeline.connect("source-setup", self.on_source_setup)

        # Creates a bus and set callbacks to receive errors
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message::eos", self.on_eos)
        self.bus.connect("message::error", self.on_error)

    def stop(self):
        # Stop playback and exit mainloop
        self.pipeline.set_state(gst.State.NULL)
        self.mainloop.quit()
        self.playing = False

        # Close the stream
        if self.fd:
            self.fd.close()

    def play(self, stream):
        # Attempt to open the stream
        try:
            self.fd = stream.open()
        except StreamError as err:
            print("Failed to open stream: {0}".format(err))
            return False

        # Start playback
        self.pipeline.set_state(gst.State.PLAYING)
        self.mainloop.run()
        self.playing = True
        return True

    def on_source_setup(self, element, source):
        source.connect("need-data", self.on_source_need_data)

    def on_source_need_data(self, source, length):
        # Attempt to read data from the stream
        try:
            data = self.fd.read(length)
        except IOError as err:
            print("Failed to read data from stream: {0}".format(err))

        # If data is empty it's the end of stream
        if not data:
            source.emit("end-of-stream")
            return

        # Convert the Python bytes into a GStreamer Buffer
        # and then push it to the appsrc
        buf = gst.Buffer.new_wrapped(data)
        source.emit("push-buffer", buf)

    def on_eos(self, bus, msg):
        self.stop()

    def on_error(self, bus, msg):
        error = msg.parse_error()[1]
        print("Caught error {0}".format(error))
        self.stop()

    def is_playing(self):
        return self.playing
