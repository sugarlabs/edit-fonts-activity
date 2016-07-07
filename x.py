"""
This file contains all the global variables required across the activity

"""
#Choose variable names wisely as they will going in the global namespace of the activity

from editfonts.objects.basefont import BaseFont



#The Default font that will always be loaded
DEFAULT_FONT_PATH = "./test_fonts/sample.ufo"

#The Path for the font file
#set this to be DEFAULT_FONT_PATH in the beginning
FONT_PATH = DEFAULT_FONT_PATH

#The global variable to store the current working font across the entire activity
FONT = BaseFont(DEFAULT_FONT_PATH)

try:
	GLYPH_NAME = FONT.keys()[0] 
except Exception, e:
	GLYPH_NAME = 'A' 

ACTIVITY_HANDLE = None