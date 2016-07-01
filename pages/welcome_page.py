import os
import shutil
import logging
import subprocess
from gettext import gettext as _

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import Pango

from widgets.custom_box import PageHeading
from widgets.custom_box import ImageButton

from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import TitleEntry
from sugar3.activity.widgets import ShareButton
from sugar3.activity.widgets import DescriptionItem
from sugar3.graphics.objectchooser import ObjectChooser
from sugar3.graphics.objectchooser import FILTER_TYPE_MIME_BY_ACTIVITY
from sugar3.datastore import datastore
from sugar3 import profile
from sugar3.graphics import style
from sugar3.graphics.alert import Alert
from sugar3.graphics.icon import Icon
from sugar3.graphics.palette import Palette

class WelcomePage(Gtk.VBox):
    """
    This Class Creates the "Welcome" Page
    
    """

    def __init__(self, activity):

        super(WelcomePage, self).__init__()
        self.activity = activity

        self._init_ui()

    def update(self, activity):
        #FIX ME: this shouldn't destroy anything
        #just update all the information in the modal

        self.activity = activity

    def _init_ui(self):

        alignment_box = Gtk.Alignment(xalign=0.5,
                      yalign=0.5,
                      xscale=0,
                      yscale=0)

        heading = PageHeading("Welcome to Edit Fonts Activity", fontSize = '40000')
        alignment_box.add(heading)

        self.pack_start(alignment_box, True, True, 0)
        
        #a hbox to store teh buttons 
        button_box = Gtk.HBox()

        #open_ufo_button
        open_ufo_button = ImageButton('open-ufo')
        open_ufo_button.set_tooltip_text('Open a .ufo font file')
        open_ufo_button.connect("clicked", lambda _: self.activity.load_ufo())

        button_box.pack_start(open_ufo_button, False, False, 30)

        #create_ufo_button
        create_ufo_button = ImageButton('create-ufo')
        create_ufo_button.set_tooltip_text('Create a new .ufo font file')
        create_ufo_button.connect("clicked", lambda _: self.activity.create_ufo())

        button_box.pack_start(create_ufo_button, False, False, 30)

        alignment_box = Gtk.Alignment(xalign=0.5,
                      yalign=0.5,
                      xscale=0,
                      yscale=0)
        alignment_box.add(button_box)
        self.pack_start(alignment_box, True, True, 0)

        self.show_all()
