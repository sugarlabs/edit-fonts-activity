"""This file contains all the global variables required across the activity."""

# Choose variable names wisely as they will going in the global namespace of
# the activity

import gi  # noqa
from gi.repository import GObject

from editfonts.objects.basefont import BaseFont
# from defcon import Font


class GlobalVar(GObject.GObject):
    """
    This class defines the global settings veriable used
    GObject provides the signal 'notify' on change,
    which is the sole reason to use this class
    """

    def __init__(self):
        super(GlobalVar, self).__init__()

        # handle for the activity class
        self.A = None

        # The Default font that will always be loaded
        self.DEFAULT_FONT_PATH = "./test_fonts/sample.ufo"

        # The Path for the font file
        # set this to be DEFAULT_FONT_PATH in the beginning
        self.FONT_PATH = self.DEFAULT_FONT_PATH

        # The global variable to store the current working font across the
        # entire activity
        self.FONT = BaseFont(self.DEFAULT_FONT_PATH)

        self.GLYPH = self.FONT["dollar"]

        self.ACTIVITY_HANDLE = None
        self.EDITOR_BOX_WIDTH = 500
        self.EDITOR_BOX_HEIGHT = 500
        self.GdkPixbuf = 1

        self.h = self.FONT.info.ascender - self.FONT.info.descender

        self.b = 0 - self.FONT.info.descender

        self.ZONE_R = 20

        # a flag to see if any particular tool is active in the editor area
        self.TOOL_ACTIVE = {'BezierPenTool': False}

        # if the current page has changed the global data or not
        # FONT_EDITED = False

        self.GLYPH_BOX_COLOR = '#6699cc'

    def X(self, x):
        t = float(x) * self.EDITOR_BOX_HEIGHT / self.h
        return t

    def Y(self, y):
        t = float(self.h - y - self.b) * self.EDITOR_BOX_HEIGHT / self.h
        return t

    def invX(self, x):
        return float(x) * self.h / self.EDITOR_BOX_HEIGHT

    def invY(self, y):
        return self.h - float(y) * self.h / self.EDITOR_BOX_HEIGHT - self.b

globals = GlobalVar()
