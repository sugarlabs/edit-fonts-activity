from defcon import Font
# from defcon import Glyph

from editfonts.objects import settings

import fontTools


class BaseFont(Font):

    def __init__(self, *args, **kwargs):
        super(BaseFont, self).__init__(*args, **kwargs)

    @classmethod
    def new_standard_font(cls, data=None):
        font = cls()

        if data is not None:
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

        else:
            font.info.familyName = "Untitled Font"
            font.info.ascender = 800
            font.info.descender = -200
            font.info.copyright = ""
            font.info.trademark = ""
            font.info.styleName = "Regular"

            font.info.capHeight = 800
            font.info.unitsPerEm = 1000
            font.info.xHeight = 500
            font.info.year = 2016
            font.info.versionMajor = 1
            font.info.versionMinor = 0

        default_glyph_set = settings.get_default_glyph_set()
        for glyph_name in default_glyph_set:
            font.new_standard_glyph(glyph_name)
        font.dirty = False

        # alert: new font created
        return font

    def new_standard_glyph(self, name, override=False, addUnicode=True,
                           asTemplate=False, markColor=None, width=500):
        if not override:
            if name in self:
                return None
        glyph = self.newGlyph(name)

        glyph.width = width

        if addUnicode:

            GL2UV = fontTools.agl.AGL2UV
            hexes = "ABCDEF0123456789"
            name = glyph.name
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
            glyph.unicodes = [uni]

        glyph.markColor = markColor
        return glyph

"""
def new_standard_font(cls, data=None):
    '''
    Create a New Font with the user inputed data
    or with default data
    '''
    font = Font()

    if data is not None:
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

    else:
        font.info.familyName = "Untitled Font"
        font.info.ascender = 800
        font.info.descender = -200
        font.info.copyright = ""
        font.info.trademark = ""
        font.info.styleName = "Regular"

        font.info.capHeight = 800
        font.info.unitsPerEm = 1000
        font.info.xHeight = 500
        font.info.year = 2016
        font.info.versionMajor = 1
        font.info.versionMinor = 0

    default_glyph_set = settings.get_default_glyph_set()
    for glyph_name in default_glyph_set:
        font.new_standard_glyph(glyph_name)
    font.dirty = False

    return font

def new_standard_glyph(self, name, override=False, addUnicode=True,
                       asTemplate=False, markColor=None, width=500):
    if name in globals.FONT:
        return None
    glyph = self.newGlyph(name)

    glyph.width = width

    if addUnicode:

        GL2UV = fontTools.agl.AGL2UV
        hexes = "ABCDEF0123456789"
        name = glyph.name
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
        glyph.unicodes = [uni]

    glyph.markColor = markColor
    return glyph
"""
