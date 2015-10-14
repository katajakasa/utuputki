# -*- coding: utf-8 -*-

from gi.repository import GObject as gobject, Gst as gst, Gtk as gtk, GdkX11, GstVideo 
from livestreamer import Livestreamer, StreamError
import platform


class LivestreamerPlayer(object):
    def __init__(self, window):
        self.fd = None
        self.playing = False
        self.window = window

        # The play binary pipeline
        self.pipeline = gst.ElementFactory.make("playbin", None)
        self.pipeline.set_property("uri", "appsrc://")
        self.pipeline.connect("source-setup", self.on_source_setup)

        # Sink
        if platform.system() == "Windows":
            self.sink = gst.ElementFactory.make('d3dvideosink', 'sink')
        else:
            self.sink = gst.ElementFactory.make('xvimagesink', 'sink')
            self.sink.set_property('force-aspect-ratio', True)

        self.pipeline.set_property('video-sink', self.sink)

        # Creates a bus and set callbacks to receive errors
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message::eos", self.on_eos)
        self.bus.connect("message::error", self.on_error)

        # Find the correct window handle and set it as base drawing area for the video sink
        if platform.system() == "Windows":
            self.sink.set_window_handle(self.window.get_hwnd())
        else:
            self.sink.set_window_handle(self.window.get_xid())

    def stop(self):
        # Stop playback and exit mainloop
        self.pipeline.set_state(gst.State.NULL)

        # Close the stream
        if self.fd:
            self.fd.close()

        self.playing = False

    def play(self, stream):
        # Attempt to open the stream
        try:
            self.fd = stream.open()
        except StreamError as err:
            print("Failed to open stream: {0}".format(err))
            return False

        # Start playback
        self.pipeline.set_state(gst.State.PLAYING)
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
            self.stop()
            return

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
        print("End of stream!")

    def on_error(self, bus, msg):
        error = msg.parse_error()[1]
        print("Caught error {0}".format(error))
        self.stop()

    def is_playing(self):
        return self.playing

