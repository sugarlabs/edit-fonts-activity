# import os
# import shutil
# import logging
# import subprocess
# from gettext import gettext as _

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

# from editfonts.widgets.misc import PageHeading
from editfonts.widgets.misc import ImageButton
from editfonts.widgets.misc import FormatLabel
from editfonts.widgets.editor_box import EditorBox
import editfonts.globals as globals


class WelcomePage(Gtk.VBox):
    """
    This Class Creates the "Welcome" Page
    """

    def __init__(self):
        super(WelcomePage, self).__init__()
        self._init_ui()

    def _init_ui(self):

        # add the editfonts glyph

        editor_alignment = Gtk.Alignment(xalign=0.5,
                                         yalign=0.5,
                                         xscale=0,
                                         yscale=0)

        editor_area = EditorBox('WELCOME', fill=True)
        editor_alignment.add(editor_area)
        self.pack_start(editor_alignment, True, True, 30)

        # make a grid for the buttons
        grid = Gtk.Grid()

        grid.set_row_spacing(globals.BUTTON_BOX_ROW_SPACING)
        grid.set_column_spacing(globals.BUTTON_BOX_COLUMN_SPACING)

        # New Blank Font
        vbox = Gtk.VBox()
        button = ImageButton('blank-font', pixel_size=globals.BUTTON_BOX_SIZE)
        button.set_tooltip_text('Create a new font file')
        button.connect("clicked", lambda _: globals.A.create_font())

        vbox.pack_start(button, False, False, 0)

        label = FormatLabel('New Blank Font', globals.TEXT_STYLE['LABEL'])
        alignment_box = Gtk.Alignment(xalign=0.5,
                                      yalign=0.5,
                                      xscale=0,
                                      yscale=0)
        alignment_box.add(label)
        vbox.pack_start(alignment_box, True, True, 0)

        grid.attach(vbox, 0, 0, 1, 1)

        # Load Font
        vbox = Gtk.VBox()
        button = ImageButton('load-font', pixel_size=globals.BUTTON_BOX_SIZE)

        # FIXME: change the tooltip below to something oriented towards kids
        button.set_tooltip_text('Load a font:\
            a .zip file containing a .ufo file')
        button.connect("clicked", lambda _: globals.A.load())

        vbox.pack_start(button, False, False, 0)

        label = FormatLabel('Load Font', globals.TEXT_STYLE['LABEL'])
        alignment_box = Gtk.Alignment(xalign=0.5,
                                      yalign=0.5,
                                      xscale=0,
                                      yscale=0)
        alignment_box.add(label)
        vbox.pack_start(alignment_box, True, True, 0)

        grid.attach(vbox, 0, 1, 1, 1)

        # New Sample Font
        vbox = Gtk.VBox()
        button = ImageButton('sample-font', pixel_size=globals.BUTTON_BOX_SIZE)
        button.set_tooltip_text('Load the sample font: Geo')
        button.connect("clicked", lambda _: globals.A.load_sample())

        vbox.pack_start(button, False, False, 0)

        label = FormatLabel('New Sample Font', globals.TEXT_STYLE['LABEL'])
        alignment_box = Gtk.Alignment(xalign=0.5,
                                      yalign=0.5,
                                      xscale=0,
                                      yscale=0)
        alignment_box.add(label)
        vbox.pack_start(alignment_box, True, True, 0)

        grid.attach(vbox, 1, 0, 1, 1)

        # Import Font
        vbox = Gtk.VBox()
        button = ImageButton('import-font', pixel_size=globals.BUTTON_BOX_SIZE)

        # FIXME: change the tooltip below to something oriented towards kids
        button.set_tooltip_text('Import a font: only\
            .otf or .ttf files supported')
        button.connect("clicked", lambda _: globals.A.import_font())

        vbox.pack_start(button, False, False, 0)

        label = FormatLabel('Import Font', globals.TEXT_STYLE['LABEL'])
        label.set_alignment(0, 0.5)
        alignment_box = Gtk.Alignment(xalign=0.5,
                                      yalign=0.5,
                                      xscale=0,
                                      yscale=0)
        alignment_box.add(label)
        vbox.pack_start(alignment_box, True, True, 0)

        grid.attach(vbox, 1, 1, 1, 1)

        alignment_box = Gtk.Alignment(xalign=0.5,
                                      yalign=0.5,
                                      xscale=0,
                                      yscale=0)
        alignment_box.add(grid)
        self.pack_start(alignment_box, True, True, 0)

        self.show_all()
