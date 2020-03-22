"""This file contains all the global variables required across the activity."""

# Choose variable names wisely as they will going in the global namespace of
# the activity

import weakref
from gi.repository import Gdk
from gi.repository import Gio

from editfonts.core.basefont import BaseFont
# from defcon import Font

from sugar3.graphics.xocolor import XoColor

# handle for the activity class
SELF = None

# The Sample font that will always be loaded
SAMPLE_FONT_PATH = './test_fonts/Geo-Regular.ufo'
SAMPLE_FONT = BaseFont(SAMPLE_FONT_PATH)
SAMPLE_FONT_REF = weakref.ref(SAMPLE_FONT)
# The Path for the font file
# set this to be SAMPLE_FONT_PATH in the beginning
FONT_PATH = SAMPLE_FONT_PATH

# The global variable to store the current working font across the
# entire activity

FONT = BaseFont(SAMPLE_FONT_PATH)
FONT_REF = weakref.ref(FONT)

if FONT_REF() is not None:
    GLYPH = FONT_REF()["A"]
    h = FONT_REF().info.ascender - FONT_REF().info.descender
    b = 0 - FONT_REF().info.descender

GdkPixbuf = 1


ZONE_R = 20

# a flag to see if any particular tool is active in the editor area
TOOL_ACTIVE = {'BezierPenTool': False}

# if the current page has changed the global data or not
# FONT_EDITED = False

# ########################
# Transformation Functions
# ########################


def X(x, id):  # noqa
    t = float(x) * GLYPH_BOX[id]['height'] / h
    return t


def Y(y, id):  # noqa
    t = float(h - y - b) * GLYPH_BOX[id]['height'] / h
    return t


def invX(x, id):  # noqa
    return float(x) * h / GLYPH_BOX[id]['height']


def invY(y, id):  # noqa
    return h - float(y) * h / GLYPH_BOX[id]['height'] - b

# #########
# User Info
# #########

settings = Gio.Settings('org.sugarlabs.color');
color =\
    XoColor(settings.get_string('color'))
USER_COLOR = color.to_string().split(',')

# ###########
# Screen Info
# ###########

SCREEN = Gdk.Screen.get_default()
SCREEN_WIDTH = SCREEN.get_width()
SCREEN_HEIGHT = SCREEN.get_height()

# ######################
# Widget Styles/Settings
# ######################

# General

GLYPH_BOX_COLOR = '#FFFFFF'
GLYPH_BOX = {}
ACTIVITY_BG = '#AAAAAA'

# Character Map

GRID_BOX_SIZE = float(SCREEN_WIDTH) * 0.07
GRID_ROW_SPACING = float(SCREEN_WIDTH) * 0.007
GRID_COLUMN_SPACING = GRID_ROW_SPACING

# Welcome Page

WELCOME_GLYPH = SAMPLE_FONT['editfonts']

# Welcome Page

"""
Trying to fix #86

if SAMPLE_FONT_REF() is not None:
    WELCOME_GLYPH = SAMPLE_FONT_REF()['P']
else:
    SAMPLE_FONT = weakref.ref(BaseFont(SAMPLE_FONT_PATH))
    WELCOME_GLYPH = SAMPLE_FONT_REF()['P']
"""

GLYPH_BOX['WELCOME'] = {'width': float(SCREEN_WIDTH) * 0.80,
                        'height': float(SCREEN_WIDTH) * 0.26,
                        'bg-color': '#AAAAAA',
                        'glyph': WELCOME_GLYPH}

BUTTON_BOX_SIZE = float(SCREEN_WIDTH) * 0.1
BUTTON_BOX_COLUMN_SPACING = float(SCREEN_WIDTH) * 0.1
BUTTON_BOX_ROW_SPACING = float(SCREEN_WIDTH) * 0.01

# Summary Page

# Editor Page

GLYPH_BOX['EDITOR'] = {'glyph': GLYPH,
                       'width': float(SCREEN_WIDTH) * 0.80,
                       'height': float(SCREEN_HEIGHT) * 0.80,
                       'bg-color': '#FFFFFF'}

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

"""
# ##
# GlyphBox Manager
# ##

# A list for storing the identifiers
GlyphBoxManager = []


def add_glyph_box(glyph_box):
    Add the Glyph Box to the GlyphBoxManager.

    The function returns the identifier for the GlyphBox so that each GlyphBox
    has an unique identifier

    if glyph_box.identifier is None:
        from defcon.tools.identifiers import makeRandomIdentifier
        identifier = makeRandomIdentifier(existing=GlyphBoxManager)
    else:
        if identifier in GlyphBoxManager.keys():
            return -1
    GlyphBoxManager[identifier] =
    return len(GlyphBoxManager) - 1

"""
