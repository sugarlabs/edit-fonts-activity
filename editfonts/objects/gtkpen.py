
import gi
gi.require_version('Gtk', '3.0')

from fontTools.pens.basePen import BasePen
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

        # The advance width of the glyph
        self.w = globals.GLYPH.width

        # The difference in the ascender and the descender values
        self.h = globals.FONT.info.ascender - globals.FONT.info.descender

        # the distance between the baseline and the descender
        self.b = 0 - globals.FONT.info.descender

        # the scale of the drawing
        self.scale = scale

    # define the transformations for the points here
    def X(self, x):
        t = self.pos + float(x) *\
            globals.EDITOR_AREA[self.id]['height'] / self.h

        """
        H = globals.EDITOR_AREA[self.id]['EDITOR_BOX_HEIGHT']
        W = globals.EDITOR_AREA[self.id]['EDITOR_BOX_WIDTH']

        H_ = 0.8 * H
        W_ = self.w * 0.8 * H / self.h
        # w_prime = W * 1.2 * self.h / H
        t = (W / 2.0 + W_ / 2.0) + float(x) * W_ / self.w
        """
        return t * self.scale

    def Y(self, y):
        t = float(self.h - y - self.b) *\
            globals.EDITOR_AREA[self.id]['height'] / self.h
        """
        t = float(1.1 * self.h - y - self.b) *\
            globals.EDITOR_AREA[self.id]['height'] / 1.2 * self.h
        """
        return t * self.scale

    def convertToScale(self, X):
        return X * self.scale *\
            globals.EDITOR_AREA[self.id]['height'] / self.h

    def _moveTo(self, p):
        x, y = p
        self.cr.move_to(self.X(x), self.Y(y))
        # print "move ->" + str(x) + "," + str(y)

    def _lineTo(self, p):
        x, y = p
        self.cr.line_to(self.X(x), self.Y(y))
        # print "line ->" + str(x) + "," + str(y)

    def _curveToOne(self, p1, p2, p3):
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        self.cr.curve_to(self.X(x1), self.Y(y1), self.X(x2), self.Y(y2),
                         self.X(x3), self.Y(y3))
        # print "curve ->" + str(x1) + "," + str(y1) + "|" + str(x2) +
        #       "," + str(y2) + "|" + str(x3) + "," + str(y3)
