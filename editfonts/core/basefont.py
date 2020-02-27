import logging
from defcon import Font
# from defcon import Glyph

from editfonts.core import settings
import fontTools


class BaseFont(Font):
    """The Subclass of :class:`Font` class."""

    def __init__(self, *args, **kwargs):
        super(BaseFont, self).__init__(*args, **kwargs)

    @classmethod
    def new_default_font(cls):  # noqa
        """
        Return a font object that has the *Default Values* preset for
        certain *Attributes*.

        The *Attributes* and their *Default Values* are set within
        this function definition.
        """
        font = cls()

        font.info.familyName = "Untitled Font"
        font.info.ascender = 800
        font.info.descender = -200
        font.info.copyright = ""

        # FIXME: Set the default trademark
        font.info.trademark = ""
        font.info.styleName = "Regular"

        font.info.capHeight = 800
        font.info.unitsPerEm = 1000
        font.info.xHeight = 500

        import datetime
        font.info.year = datetime.datetime.now().year
        font.info.versionMajor = 1
        font.info.versionMinor = 0

        font.dirty = False

        # alert: new font created
        return font

    def set_font_data(self, data):  # noqa
        """
        Set the Font attributes to the data specified as key
        arguments to this function.

        ## Usage

        ```python
        data = {'familyName':'Amazo',
                'ascender':800,
                'descender':-200
               }

        font  = BaseFont()
        font.set_font_data(data)
        ```
        """
        if data is not None:
            for attr, val in enumerate(data):
                if data[attr] is not None and hasattr(self.info, attr):
                    setattr(self.info, attr, val)

    def add_glyph(self, glyph_list):
        """
        Add the Glyph Names mentioned in the glyph_list to the font.

        Don't Override all the Glyphs that are already present in the Font
        """
        for glyph_name in glyph_list:
            self.new_standard_glyph(glyph_name)

    def remove_glyph(self, glyph_list):
        """Remove the Glyph Names mentioned in the glyph_list from the font."""
        for glyph_name in glyph_list:
            del self[glyph_name]

    def set_default_glyph_set(self):  # noqa
        """
        Add the default Glyph List specified in :func:`settings.get_default_glyph_set`  # noqa
        """
        default_glyph_set = settings.get_default_glyph_set()
        self.add_glyph(default_glyph_set)
        self.dirty = False

    def sort_glyph_list(self):
        """
        Sort the Glyph List according to
        [fontTools.ttLib.standardGlyphOrder](https://github.com/behdad/fonttools/blob/master/Lib/fontTools/ttLib/standardGlyphOrder.py)  # noqa
        """
        from fontTools.ttLib.standardGlyphOrder import standardGlyphOrder
        # FIXME: Complete this, Fixes #91
        for glyph_name in standardGlyphOrder:
            pass

    def new_standard_glyph(self, name, override=False, addUnicode=True,  # noqa
                           asTemplate=False, markColor=None, width=500):
        """
        Add a new *Standard Glyph* to the Font.

        **Standard Glyph** is a Glyph from AGLFN(Adobe Glyph List For New Fonts)

        from module [fontTools.agl](https://github.com/behdad/fonttools/blob/master/Lib/fontTools/agl.py)

        AGLFN (Adobe Glyph List For New Fonts) provides a list of base glyph
        names that are recommended for new fonts, which are compatible with
        the AGL (Adobe Glyph List) Specification, and which should be used
        as described in Section 6 of that document. AGLFN comprises the set
        of glyph names from AGL that map via the AGL Specification rules to
        the semantically correct UV (Unicode Value). For example, "Asmall"
        is omitted because AGL maps this glyph name to the PUA (Private Use
        Area) value U+F761, rather than to the UV that maps from the glyph
        name "A." Also omitted is "ffi," because AGL maps this to the
        Alphabetic Presentation Forms value U+FB03, rather than decomposing
        it into the following sequence of three UVs: U+0066, U+0066, and
        U+0069. The name "arrowvertex" has been omitted because this glyph
        now has a real UV, and AGL is now incorrect in mapping it to the PUA
        value U+F8E6. If you do not find an appropriate name for your glyph
        in this list, then please refer to Section 6 of the AGL
        Specification.

        Format: three semicolon-delimited fields:
          (1) Standard UV or CUS UV--four uppercase hexadecimal digits
          (2) Glyph name--upper/lowercase letters and digits
          (3) Character names: Unicode character names for standard UVs, and
              descriptive names for CUS UVs--uppercase letters, hyphen, and
              space

        The records are sorted by glyph name in increasing ASCII order,
        entries with the same glyph name are sorted in decreasing priority
        order, the UVs and Unicode character names are provided for
        convenience, lines starting with "#" are comments, and blank lines
        should be ignored.

        Ported from [Trufont](https://github.com/trufont/trufont/blob/master/Lib/trufont/objects/defcon.py)  # noqa
        """
        if not override:
            if name in self:
                return None
        glyph = self.newGlyph(name)

        glyph.width = width

        if addUnicode:

            GL2UV = fontTools.agl.AGL2UV  # noqa
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

    def save_zip(self, ufo_path, zip_path):  # noqa
        """
        Save the font to the ``zip_path`` attribute as zip file containing a UFO font file.  # noqa

        ``ufo_path`` is the path where the UFO font file is saved
        This is used as the source for the zip file made

        **Output**: Returns the state of statement *The zip file was successfully created*
        """
        if zip_path is not None:
            # zip the folder
            import zipfile
            import os

            # create an empty zip file in the data folder
            try:
                zipf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)

                for root, dirs, files in os.walk(ufo_path):
                    for file in files:
                        relroot = os.path.relpath(root, ufo_path)
                        zipf.write(os.path.join(root, file),
                                   os.path.join(relroot, file))
                zipf.close()

            except Exception:
                return False

            else:
                return True

    @classmethod
    def import_from_binary(cls, path):
        """Import the font from a .otf/.ttf file."""
        # FIXME: Check wether the current font is saved
        import extractor
        try:
            font = cls()
            extractor.extractUFO(path, font)
        except Exception:
            logging.error("Unable to Import the chosen file")
            return None
        else:
            return font

    def export_binary(self, path):
        """Export the font as a .otf file."""
        # converting the font to a OTF
        # The current implementation fails if optimizeCff is set to True
        # FIXME: Find a better solution for exporting the font
        # probably use fontmake to validate the data being saved
        from ufo2ft import compileOTF
        otf = compileOTF(self, optimizeCff=False)

        # save the otf
        otf.save(path)
