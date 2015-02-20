# -*- coding: utf-8 -*-

import sys
import gi

from gi.repository import Gtk as gtk, GdkX11, GstVideo

class VideoWindow(object):
    def __init__(self):
        self.open = True

        # Gtk window
        self.window = gtk.Window()
        self.window.connect('destroy', self.on_window_destroy)
        self.window.set_title("Utuputki")
        self.window.fullscreen()

        # Drawing area
        self.area = gtk.DrawingArea()
        self.window.add(self.area)

        self.window.show_all()

    def run(self):
        gtk.main()

    def get_xid(self):
        return self.area.get_property('window').get_xid()

    def is_open(self):
        return self.open

    def on_window_destroy(self, nx):
        gtk.main_quit()
        self.open = False

