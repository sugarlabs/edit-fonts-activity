# import os
# import shutil
# import logging
# import subprocess
# from gettext import gettext as _

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

from editfonts.widgets.custom_box import PageHeading
from editfonts.widgets.custom_box import ImageButton
import editfonts.globals as globals


class WelcomePage(Gtk.VBox):
    """
    This Class Creates the "Welcome" Page

    """

    def __init__(self):
        super(WelcomePage, self).__init__()
        self._init_ui()

    def _init_ui(self):

        alignment_box = Gtk.Alignment(xalign=0.5,
                                      yalign=0.5,
                                      xscale=0,
                                      yscale=0)

        heading = PageHeading("Welcome to Edit Fonts Activity",
                              fontSize='40000')
        alignment_box.add(heading)

        self.pack_start(alignment_box, True, True, 0)

        # a hbox to store teh buttons
        button_box = Gtk.HBox()

        # open_button
        open_button = ImageButton('open-ufo')
        open_button.set_tooltip_text('Open a .ufo font file')
        open_button.connect("clicked", lambda _: globals.A.load_ufo())

        button_box.pack_start(open_button, False, False, 30)

        # create_button
        create_button = ImageButton('create-ufo')
        create_button.set_tooltip_text('Create a new .ufo font file')

        create_button.connect("clicked", lambda _: globals.A.create_font())

        button_box.pack_start(create_button, False, False, 30)

        alignment_box = Gtk.Alignment(xalign=0.5,
                                      yalign=0.5,
                                      xscale=0,
                                      yscale=0)
        alignment_box.add(button_box)
        self.pack_start(alignment_box, True, True, 0)

        self.show_all()
