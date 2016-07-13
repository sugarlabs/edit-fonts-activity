import math

# from gi.repository import Gtk
from gi.repository import Gdk

from defcon import Contour
from defcon import Point
import editfonts.globals as globals

ZONE_R = 10


def distance(x1, y1, x2, y2):
    t1 = (x1 - x2)
    t2 = (y1 - y2)
    return math.sqrt(t1 * t1 + t2 * t2)


class BezierPenTool(object):

    def __init__(self, editorBox):
        self.contour = Contour()
        self.editor = editorBox
        self.set_active(True)
        self.editor.add_contour(self.contour)

    def set_active(self, state):
        if state is True:
            self.is_active = True
            self.contour = Contour()
            self.editor.add_contour(self.contour)
            self.connect_editor()
        else:
            self.is_active = False
            self.disconnect_editor()

    def get_active(self):
        return self.is_active

    def disconnect_editor(self):
        # for val, _ in enumerate(self.handle):
        # self.editor.disconnect(val)

        self.editor.disconnect(self.handle)

    def connect_editor(self):
        # add all the events here which the pen tool needs to listen to
        self.handle = self.editor.connect("button-press-event",
                                          self._on_point_press)

    def _on_point_press(self, widget, event):
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 1:
            print "Clicked on: (" + str(event.x) + ", " + str(event.y) + ")"
            # add point at the click locations
            if self.get_active():
                self.add_point(event.x, event.y)
            else:
                print "This shouldn't be happening"

    def add_point(self, x, y):

        print "add_point"
        print 0

        point = Point((globals.invX(x), globals.invY(y)))
        # point.x = globals.invX(x)
        # point.y = globals.invY(y)

        if len(self.contour[:]) == 0:
            # add the point to the contour
            point.segmentType = u'move'
            point.smooth = False

            self.contour.appendPoint(point)

        elif self._check_close_contour(point):
            # convert the first point to a line type
            print "the contour should be closed now"
            self.contour[0].segmentType = u'line'

        else:
            # add the point to the contour
            point.segmentType = u'line'
            point.smooth = False

            self.contour.appendPoint(point)

        self.editor.update_control_points()

    # check if the click is inside a zone defined by the
    # ZONE_R of the first point of the contour
    def _check_close_contour(self, point):
        if len(self.contour[:]) == 0:
            return False

        t = distance(self.contour[0].x, self.contour[0].y, point.x, point.y)
        if t <= ZONE_R:
            return True
        return False
