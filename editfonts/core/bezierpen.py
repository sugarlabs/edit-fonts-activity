import math

from gi.repository import Gdk

from defcon import Contour
from defcon import Point
import editfonts.globals as globals


def distance(x1, y1, x2, y2):
    """Return the distance between the points (x1, y1) and (x2, y2)"""
    t1 = (x1 - x2)
    t2 = (y1 - y2)
    return math.sqrt(t1 * t1 + t2 * t2)


class BezierPenTool(object):
    """
    The Pen Tool used to Draw Bezier Curves inside a class:
                                            `~editfonts.widgets.glyph_box`.

    Current Status
    ~~~~~~~~~~~~~~~~~
    This tool is not complete and can only be used to draw contours with lines
    to activate the Bezier Pen Tool right click on the drawing area on the
    editor page and click any number of times to add a point to a new contour
    We can close those contours by clicking inside the halo around the starting
    point of the contour

    To be Implemented
    ~~~~~~~~~~~~~~~~~
    Add the Functionality to make Bezier Curves
    This can be done by monitoring the **drag event** on the Drawing Area
    inside a **GlyphBox** to implement the above features the following
    open source code file(s) may be usefull
    + .. drawingarea.py : https://github.com/
    GNOME/pygobject/blob/master/demos/gtk-demo/demos/drawingarea.py
    """

    def __init__(self, editorBox):
        self.editor = editorBox
        self.set_active(True)

    def set_active(self, state):
        """Activate/Deactivate the Bezier Pen Tool"""
        if state is True:
            self.is_active = True
            self.contour = Contour()
            self.contour.dirty = True
            self.editor.add_contour(self.contour)
            self.connect_editor()
        else:
            self.contour.dirty = False
            self.is_active = False
            self.disconnect_editor()

        globals.TOOL_ACTIVE['BezierPenTool'] = state

    def get_active(self):
        """
        Get the state of the Bezier Pen Tool
        True ~ is active
        False ~ is inactive
        """
        return self.is_active

    def disconnect_editor(self):
        """Disable Drawing with the Bezier Pen Tool"""
        self.editor.disconnect(self.handle_press)
        # self.editor.disconnect(self.handle_release)

    def connect_editor(self):
        """Enable Drawing with the Bezier Pen Tool"""
        # add all the events here which the pen tool needs to listen to
        self.handle_press = self.editor.connect("button-press-event",
                                                self._on_point_press)
        # self.handle_release = self.editor.connect("button-release-event",
        #                                           self._on_point_release)

    def _on_point_press(self, widget, event):
        """Enable Drawing with the Bezier Pen Tool"""
        if event.type == Gdk.EventType.BUTTON_PRESS\
                and event.button == 1:
            # print "Clicked on: (" + str(event.x) + ", " + str(event.y) + ")"
            # add point at the click locations
            # print self.get_active()
            if self.get_active():
                self.add_point(event.x, event.y)
            else:
                # print "This shouldn't be happening"
                pass

    def _on_point_release(self, widget, event):
        if event.type == Gdk.EventType.BUTTON_RELEASE\
                and event.button == 1:
            # print "Released on: (" + str(event.x) + ", " + str(event.y) + ")"
            # add point at the click locations
            """
            if self.get_active():
                self.add_point(event.x, event.y)
            else:
                print "This shouldn't be happening"
            """

    def add_point(self, x, y):
        """Add a Point to the currently active contour"""
        # print "Yahoo"
        point = Point((globals.invX(x), globals.invY(y)))
        # print "{" + str(point.x) + "," + str(point.y) + "}"
        # point.x = globals.invX(x)
        # point.y = globals.invY(y)

        if len(self.contour[:]) == 0:
            # add the point to the contour
            point.segmentType = u'move'
            point.smooth = False

            self.contour.appendPoint(point)

        elif self._check_close_contour(point):
            # convert the first point to a line type
            # print "the contour should be closed now"

            # close the contour
            self.contour[0].segmentType = u'line'

            # deactivate the bezier pen tool
            self.set_active(False)

            # No need for this
            # self.contour[0].segmentType = u'line'

        else:
            # add the point to the contour
            point.segmentType = u'line'
            point.smooth = False

            self.contour.appendPoint(point)

        self.editor.update_control_points()

    # check if the click is inside a zone defined by the
    # ZONE_R of the first point of the contour
    def _check_close_contour(self, point):
        """
        Check if the last click was within a certain distance
        **globals.ZONE_R** around the starting point of the contour
        """
        if len(self.contour[:]) == 0:
            return False

        t = distance(self.contour[0].x, self.contour[0].y, point.x, point.y)
        if t <= globals.ZONE_R:
            return True
        return False
