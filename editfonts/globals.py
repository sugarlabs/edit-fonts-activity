"""This file contains all the global variables required across the activity."""

# Choose variable names wisely as they will going in the global namespace of
# the activity

import gi  # noqa
from gi.repository import Gdk

from editfonts.objects.basefont import BaseFont
from defcon import Font


# handle for the activity class
A = None

# The Default font that will always be loaded
DEFAULT_FONT_PATH = "./test_fonts/sample.ufo"

# The Path for the font file
# set this to be DEFAULT_FONT_PATH in the beginning
FONT_PATH = DEFAULT_FONT_PATH

# The global variable to store the current working font across the
# entire activity
FONT = BaseFont(DEFAULT_FONT_PATH)

GLYPH = FONT["dollar"]

ACTIVITY_HANDLE = None
EDITOR_BOX_WIDTH = 500
EDITOR_BOX_HEIGHT = 500
GdkPixbuf = 1

h = FONT.info.ascender - FONT.info.descender

b = 0 - FONT.info.descender

ZONE_R = 20

# a flag to see if any particular tool is active in the editor area
TOOL_ACTIVE = {'BezierPenTool': False}

# if the current page has changed the global data or not
# FONT_EDITED = False

def X(x): # noqa
    t = float(x) * EDITOR_BOX_HEIGHT / h
    return t


def Y(y): # noqa
    t = float(h - y - b) * EDITOR_BOX_HEIGHT / h
    return t


def invX(x): # noqa
    return float(x) * h / EDITOR_BOX_HEIGHT


def invY(y): # noqa
    return h - float(y) * h / EDITOR_BOX_HEIGHT - b

# ###########
# Screen Info
# ###########

SCREEN = Gdk.Screen.get_default()
SCREEN_WIDTH = SCREEN.get_width()
print SCREEN_WIDTH
SCREEN_HEIGHT = SCREEN.get_height()
print SCREEN_HEIGHT

# #############
# Widget Styles
# #############

# General
GLYPH_BOX_COLOR = '#6699cc'

# Welcome Page
f = Font('./test_fonts/Geo-Regular.ufo')

WELCOME_GLYPH = f['editfonts']

WELCOME_EDITOR_BG = '#AAAAAA'

WELCOME_EDITOR_BOX_WIDTH = float(SCREEN_WIDTH) * 0.8
WELCOME_EDITOR_BOX_HEIGHT = float(SCREEN_WIDTH) * 0.2

BUTTON_BOX_SIZE = float(SCREEN_WIDTH) * 0.1
BUTTON_BOX_COLUMN_SPACING = float(SCREEN_WIDTH) * 0.1
BUTTON_BOX_ROW_SPACING = float(SCREEN_WIDTH) * 0.01

# Summary Page

# ###########
# Font Styles
# ###########

TEXT_STYLE = {}

# Using this as a font of size 15000 looks like a LABEL
# text style on a 1920 px wide screen
text_size = 20000 / 1920 * SCREEN_WIDTH

TEXT_STYLE["HEADING"] = {'color': 'black',
                         'font': 'Cantarell',
                         'weight': 'bold',
                         'size': text_size * 2}

TEXT_STYLE["PARA"] = {'color': 'black',
                      'font': 'Cantarell',
                      'weight': 'bold',
                      'size': text_size / 2}

TEXT_STYLE["LABEL"] = {'color': 'black',
                       'font': 'Cantarell',
                       'weight': 'medium',
                       'size': text_size}
