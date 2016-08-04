import math
import logging

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
# from gi.repository import GdkPixbuf
# from gi.repository import GLib
# from gi.repository import Gio
# from gi.repository import GObject

import cairo

# from defcon import Font
# from defcon import Point
# from defcon import Contour

import editfonts.globals as globals


def distance(X, Y):

    t1 = (X.get_x() - Y.get_x())
    t2 = (X.get_y() - Y.get_y())
    return math.sqrt(t1 * t1 + t2 * t2)


def slope(X, Y):

    t1 = (X.get_x() - Y.get_x())
    t2 = (X.get_y() - Y.get_y())
    return float(t2) / t1


class DragPoint(Gtk.EventBox):

    def __init__(self, point=None):

        super(DragPoint, self).__init__()

        self.point = point
        self.set_x(globals.X(self.point.x))
        self.set_y(globals.Y(self.point.y))

        # if the point is bound to any other points
        self.is_bound = False

        self.binding = []

        # radius of the point
        self.r = 5

        self.set_size_request(self.r * 2, self.r * 2)

        WIDTH = self.r * 2
        HEIGHT = self.r * 2

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
        cr = cairo.Context(surface)
        cr.scale(WIDTH, HEIGHT)  # Normalizing the canvas
        cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)

        cr.set_line_width(0.1)
        cr.set_source_rgb(0.7, 0.2, 0.0)
        cr.translate(0.5, 0.5)
        cr.arc(0, 0, 0.3, 0, 2 * math.pi)
        cr.stroke_preserve()

        cr.close_path()
        cr.fill()
        cr.stroke()

        pixbuf = Gdk.pixbuf_get_from_surface(surface, 0, 0, self.r * 2,
                                             self.r * 2)
        transparent = pixbuf.add_alpha(True, 0xff, 0xff, 0xff)
        image = Gtk.Image.new_from_pixbuf(transparent)
        self.add(image)

        self.set_above_child(True)
        self.connect("notify::point", lambda _: logging.debug("Hello"))
        self.connect("motion-notify-event", self._on_motion)

        self.set_events(self.get_events() |
                        Gdk.EventMask.LEAVE_NOTIFY_MASK |
                        Gdk.EventMask.BUTTON_PRESS_MASK |
                        Gdk.EventMask.POINTER_MOTION_MASK |
                        Gdk.EventMask.POINTER_MOTION_HINT_MASK)

        self.show_all()

    def set_type(self, segmentType):

        self.point.segmentType = segmentType

    def bind_to(self, *points):

        self.is_bound = True
        self.binding.append(points[0])
        self.binding.append(points[1])

    def update_connected_points(self, dx, dy):

        if self.point.segmentType is None:
            O = self.binding[0]
            B = self.binding[1]

            r = distance(O, B)
            d = distance(O, self)
            # m = slope(self, O)

            # t = r * r / (m * m + 1)
            # t = math.sqrt(t)

            # B.update(O.get_x() + t, O.get_y() + m*t)
            B.update(O.get_x() + (O.get_x() - self.get_x()) *
                     r / d, O.get_y() + (O.get_y() - self.get_y()) *
                     r / d)

            # print "moving B"

        elif self.point.segmentType == u'curve' and self.point.smooth is True:
            A = self.binding[0]
            B = self.binding[1]

            B.update(B.get_x() + dx, B.get_y() + dy)
            A.update(A.get_x() + dx, A.get_y() + dy)

            # print "moving A and B"

    def _on_point_press(self, widget, event):

        if event.type == Gdk.EventType.BUTTON_PRESS:
            self.drag_state = True
            return True

    def _on_point_release(self, widget, event):

        if event.type == Gdk.EventType.BUTTON_RELEASE:
            self.drag_state = False
            return True

    def get_corner_x(self):

        return self.x - self.r

    def get_corner_y(self):

        return self.y - self.r

    def _on_motion(self, widget, event):

        (window, dx, dy, state) = event.window.get_pointer()

        if state & Gdk.ModifierType.BUTTON1_MASK:

            # update the position of the point
            self.update(self.get_x() + dx - self.r, self.get_y() + dy - self.r)

            # update the position of the points binded with this point
            # print "I'm here"
            # print self.binding
            # print self.point.segmentType
            # print self.point.smooth

            if self.is_bound:
                self.update_connected_points(dx - self.r, dy - self.r)

        return True

    def update(self, x, y):
        self.set_x(x)
        self.set_y(y)

        # print "[" + str(self.x) + "," + str(self.x) + "]"

        self.get_parent().move(self, self.get_corner_x(), self.get_corner_y())

    def get_x(self):

        return self.x

    def get_y(self):

        return self.y

    def set_x(self, x):

        self.x = x

        # validate the move
        # see that the points dont go outside the drawing area
        if self.x > globals.EDITOR_BOX_WIDTH:
            self.x = globals.EDITOR_BOX_WIDTH

        elif self.x < 0:
            self.x = 0

        self.point.x = globals.invX(self.x)

    def set_y(self, y):

        self.y = y

        # validate the move
        # see that the points dont go outside the drawing area
        if self.y > globals.EDITOR_BOX_HEIGHT:
            self.y = globals.EDITOR_BOX_HEIGHT
        elif self.y < 0:
            self.y = 0

        self.point.y = globals.invY(self.y)
