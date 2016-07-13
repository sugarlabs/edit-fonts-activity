"""
This file contains all the global variables required across the activity

"""
# Choose variable names wisely as they will going in the global namespace of
# the activity

# from editfonts.objects.basefont import BaseFont
from defcon import Font

# The Default font that will always be loaded
DEFAULT_FONT_PATH = "./test_fonts/sample.ufo"

# The Path for the font file
# set this to be DEFAULT_FONT_PATH in the beginning
FONT_PATH = DEFAULT_FONT_PATH

# The global variable to store the current working font across the entire
# activity
FONT = Font(DEFAULT_FONT_PATH)

GLYPH = FONT["Q"]

try:
    GLYPH_NAME = FONT.keys()[0]
except Exception, e:
    GLYPH_NAME = 'A'

ACTIVITY_HANDLE = None
EDITOR_BOX_WIDTH = 500
EDITOR_BOX_HEIGHT = 500
GdkPixbuf = 1

h = FONT.info.ascender - FONT.info.descender

b = 0 - FONT.info.descender


def X(x):
    t = float(x) * EDITOR_BOX_HEIGHT / h
    return t


def Y(y):
    t = float(h - y - b) * EDITOR_BOX_HEIGHT / h
    return t


def invX(x):
    return float(x) * h / EDITOR_BOX_HEIGHT


def invY(y):
    return h - float(y) * h / EDITOR_BOX_HEIGHT - b
