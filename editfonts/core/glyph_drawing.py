import logging
import gi
gi.require_version('Gtk', '3.0')

from fontTools.pens.basePen import BasePen
# from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform
# from fontTools.pens.basePen import AbstractPen

import editfonts.globals as globals


class EditGlyphBox(object):

    """
    class: `GlyphDrawing` represents a single glyph on a drawing area.

    **Parts of a GlyphDrawing**

    ========================
    Name
    ========================
    GlyphDrawing.drag_points
    GlyphDrawing.support_lines
    GlyphDrawing.glyph_outine
    GlyphDrawing.sidebearing
    ========================

    **Inputs requires by a GlyphDrawing**

    ========================
    Name
    ========================
    GlyphDrawing.cr
    GlyphDrawing.glyph
    GlyphDrawing.origin
    GlyphDrawing.height
    GlyphDrawing.width
    GlyphDrawing.margin
    GlyphDrawing.style
    GlyphDrawing.glyph_color
    ========================

    **Modes of a GlyphDrawing Object**

    GlyphDrawing.mode.<modeName> is a Boolean type variable
    which represents its active and inactive state

    ========================
    Name
    ========================
    GlyphDrawing.mode.edit
    GlyphDrawing.mode.fill
    GlyphDrawing.mode.sidebearing
    ========================

    Note: Both of the above modes can be active at the same time.
    This won't cause problems as every mode deals with a separate
    part of the glyph drawing.

    **Procedure for drawing the Glyph**

    Draw the Glyph Outline

    if GlyphDrawing.mode.edit is True
    then Draw the support lines and the drag points

    if GlyphDrawing.mode.fill is True
    then Fill the glyph

    if GlyphDrawing.mode.sidebearing is True
    then Draw the side bearing editing interface

    # TODO: Add Tool Interaction

    Tools to be added:

    PenTool
    Slice/Cutter Tool
    Select Tool
    """

    def __init__(self,
                 cr,
                 pos,
                 id='EDITOR',
                 scale=1.0):
        BasePen.__init__(self, glyphSet={})
        self.cr = cr

        self.id = id

        # the position the glyph is at while drawing it in a string of glyphs
        self._origin = pos

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
        logging.debug("move ->{ %s , %s}" %
                      str(x), str(y))

    def _lineTo(self, p):
        # print p
        x, y = self.transformation.transformPoint(p)
        # x, y = p

        self.cr.line_to(x, y)
        # self.cr.line_to(self.X(x), self.Y(y))
        # print "line ->" + str(x) + "," + str(y)
        logging.debug("line ->{ %s , %s}" %
                      str(x), str(y))

    def _curveToOne(self, p1, p2, p3):
        x1, y1 = self.transformation.transformPoint(p1)
        x2, y2 = self.transformation.transformPoint(p2)
        x3, y3 = self.transformation.transformPoint(p3)

        self.cr.curve_to(x1, y1, x2, y2,
                         x3, y3)

        # self.cr.curve_to(self.X(x1), self.Y(y1), self.X(x2), self.Y(y2),
        #                  self.X(x3), self.Y(y3))
        logging.debug("curve ->{ %s , %s},{ %s , %s},{ %s , %s}" %
                      str(x1), str(y1), str(x2), str(y2), str(x3), str(y3))
