
import gi
gi.require_version('Gtk', '3.0')

from fontTools.pens.basePen import BasePen
from fontTools.misc.transform import Transform

import editfonts.globals as globals


class GtkPen(BasePen):
    """
    This class is a subclass of the BasePen Class from fontTools which
    converts any segment type to simple moveTo, lineTo, curveTo commands
    """

    def __init__(self, cr, pos, id='EDITOR', scale=1.0):
        BasePen.__init__(self, glyphSet={})
        self.cr = cr

        self.id = id

        # the position the glyph is at while drawing it in a string of glyphs
        self.pos = pos

        self.glyph = globals.EDITOR_AREA[self.id]['glyph']
        self.font = self.glyph.font
        # The advance width of the glyph
        self.w = H = self.glyph.width

        # The difference in the ascender and the descender values
        self.h = self.font.info.ascender - self.font.info.descender

        # the distance between the baseline and the descender
        self.b = 0 - self.font.info.descender

        # the scale of the drawing
        self.scale = scale

        H = globals.EDITOR_AREA[self.id]['height']  # noqa
        W = globals.EDITOR_AREA[self.id]['width']  # noqa

        self.transformation = Transform()
        self.transformation = self.transformation\
            .translate(0, self.b - self.h)\
            .scale(1, -1)\
            .scale(H / self.h, H / self.h)

        #    .translate(0, self.h - self.b)\

    # define the transformations for the points here
    def X(self, x):
        """
        t = self.pos + float(x) *\
            globals.EDITOR_AREA[self.id]['height'] / self.h

        H = globals.EDITOR_AREA[self.id]['EDITOR_BOX_HEIGHT']
        W = globals.EDITOR_AREA[self.id]['EDITOR_BOX_WIDTH']

        H_ = 0.8 * H
        W_ = self.w * 0.8 * H / self.h
        # w_prime = W * 1.2 * self.h / H
        t = (W / 2.0 + W_ / 2.0) + float(x) * W_ / self.w
        """

        t, __ = self.transformation.transformPoint((x, 1))
        return t * self.scale

    def Y(self, y):
        """
        t = float(self.h - y - self.b) *\
            globals.EDITOR_AREA[self.id]['height'] / self.h
        t = float(1.1 * self.h - y - self.b) *\
            globals.EDITOR_AREA[self.id]['height'] / 1.2 * self.h
        """

        __, t = self.transformation.transformPoint((1, y))
        return t * self.scale

    def convertToScale(self, X):
        return X * self.scale *\
            globals.EDITOR_AREA[self.id]['height'] / self.h

    def _moveTo(self, p):
        x, y = self.transformation.transformPoint(p)
        self.cr.move_to(x, y)
        # self.cr.move_to(self.X(x), self.Y(y))

    def _lineTo(self, p):
        x, y = self.transformation.transformPoint(p)
        # x, y = p

        self.cr.line_to(x, y)

    def _curveToOne(self, p1, p2, p3):
        x1, y1 = self.transformation.transformPoint(p1)
        x2, y2 = self.transformation.transformPoint(p2)
        x3, y3 = self.transformation.transformPoint(p3)

        self.cr.curve_to(x1, y1, x2, y2,
                         x3, y3)
