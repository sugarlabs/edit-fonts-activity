# import math
import cairo

# import gi
# gi.require_version('Gtk', '3.0')
# from gi.repository import Gtk, Gdk, GdkPixbuf, GLib, Gio, GObject

# from defcon import Font, Point, Contour

# from fontTools.pens.basePen import BasePen


class BaseSegment:

    def __init__(self, pointList):

        self.points = pointList[:]

    def draw(self, cr):

        cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)

        # setting the line style to solid

        cr.set_line_width(4)
        cr.set_source_rgb(0.1, 0.1, 0.1)

        # Drawing the Bezier Curve
        cr.move_to(self.points[0].x, self.points[0].y)
        cr.curve_to(self.points[1].x, self.points[1].y, self.points[2].x,
                    self.points[2].y, self.points[3].x, self.points[3].y)

        cr.stroke_preserve()
        cr.stroke()

        # Drawing the support lines

        # setting the line style to dashed
        cr.set_line_width(1)
        cr.set_source_rgb(0.3, 0.3, 0.3)

        cr.move_to(self.points[0].x, self.points[0].y)
        cr.line_to(self.points[1].x, self.points[1].y)
        cr.move_to(self.points[2].x, self.points[2].y)
        cr.line_to(self.points[3].x, self.points[3].y)

        cr.stroke_preserve()
        cr.stroke()

        # cr.close_path ()
        # cr.fill ()
        return False
