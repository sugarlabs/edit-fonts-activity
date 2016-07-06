from gi.repository import Gtk, Gdk
import cairo
import pango
import math

from sugar3.graphics.icon import Icon
from sugar3.graphics import style

from defcon import Font, Contour, Glyph, Layer, Anchor, Component, Point, Image
from defcon.objects.base import BaseObject
from fontTools.misc.transform import Identity
from editfonts.objects import settings

import extractor
import fontTools

class BaseFont(Font):

    def __init__(self, *args, **kwargs):
        kwargs["glyphClass"] = BaseGlyph
        super(BaseFont, self).__init__(*args, **kwargs)
        
    @classmethod
    def new_standard_font(cls, data):
        font = cls()

        font.info.familyName = data["familyName"]
        font.info.ascender = data["ascender"]
        font.info.descender = data["descender"]
        font.info.copyright = data["copyright"]
        font.info.trademark = data["trademark"]
        font.info.styleName = data["styleName"]
        
        font.info.capHeight = data["capHeight"]
        font.info.unitsPerEm = data["unitsPerEm"]
        font.info.xHeight = data["xHeight"]
        font.info.year = data["year"]
        font.info.versionMajor = data["versionMajor"]
        font.info.versionMinor = data["versionMinor"]
        
        default_glyph_set = settings.get_default_glyph_set()
        for glyph_name in default_glyph_set:
            font.new_standard_glyph(glyph_name)
        font.dirty = False

        #alert: new font created
        return font

    def new_standard_glyph(self, name, override=False, addUnicode=True,
                         asTemplate=False, markColor=None, width=500):
        if not override:
            if name in self:
                return None
        glyph = self.newGlyph(name)
     
        glyph.width = width
     
        if addUnicode:
            glyph.auto_unicodes()
        glyph.markColor = markColor
        return glyph
    
class BaseGlyph(Glyph):

    def __init__(self, *args, **kwargs):
        super(BaseGlyph, self).__init__(*args, **kwargs)
        
    def auto_unicodes(self):
        
        GL2UV = fontTools.agl.AGL2UV
        hexes = "ABCDEF0123456789"
        name = self.name
        if name in GL2UV:
            uni = GL2UV[name]
        elif (name.startswith("uni") and len(name) == 7 and
              all(c in hexes for c in name[3:])):
            uni = int(name[3:], 16)
        elif (name.startswith("u") and len(name) in (5, 7) and
              all(c in hexes for c in name[1:])):
            uni = int(name[1:], 16)
        else:
            return
        self.unicodes = [uni]
