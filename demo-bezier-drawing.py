import sys
import os
sys.path.insert(0, os.path.relpath('./third_party'))

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
# from gi.repository import Gdk
# import cairo
from editfonts.widgets.editor_box import EditorBox
import editfonts.globals as globals


class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Editor Area")
        # self.set_size_request(globals.EDITOR_BOX_WIDTH,
        #                       globals.EDITOR_BOX_HEIGHT)
        self.set_size_request(globals.EDITOR_AREA['EDITOR']
                              ['EDITOR_BOX_WIDTH'],
                              globals.EDITOR_AREA['EDITOR']
                              ['EDITOR_BOX_HEIGHT'])

        editor_alignment = Gtk.Alignment(xalign=0.5,
                                         yalign=0.5,
                                         xscale=0,
                                         yscale=0)

        editor_area = EditorBox()

        editor_alignment.add(editor_area)
        self.add(editor_alignment)

        self.show_all()

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
