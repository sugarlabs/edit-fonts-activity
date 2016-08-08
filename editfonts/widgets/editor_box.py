from gi.repository import Gtk, Gdk
import cairo
import math

from sugar3.graphics import style
# from defcon import Font

# Making a glyph editor box
from editfonts.objects.gtkpen import GtkPen
from editfonts.widgets.drag_point import DragPoint
# from editfonts.objects.basesegment import BaseSegment
from editfonts.objects.bezierpen import BezierPenTool
import editfonts.globals as globals


def bind(A, O, B):

    # FIX ME: a none type point shouldn't be bind to a curve
    # type point with a line or curve type point next to it
    # This currently shows an error
    # This shows an error for glyph 'M' for TT Coats Light Font
    if A.point.segmentType != u'line' or A.point.segmentType != u'curve' \
            or B.point.segmentType != u'line' \
            or B.point.segmentType != u'curve':
        A.bind_to(O, B)
        B.bind_to(O, A)

    O.bind_to(A, B)


class EditorBox(Gtk.EventBox):

    def __init__(self, id='EDITOR', fill=False):

        super(EditorBox, self).__init__()
        self.id = id
        self.set_size_request(globals.EDITOR_AREA[self.id]
                              ['EDITOR_BOX_WIDTH'],
                              globals.EDITOR_AREA[self.id]
                              ['EDITOR_BOX_HEIGHT'])

        self.fixed = Gtk.Fixed()
        self.fixed.set_size_request(globals.EDITOR_AREA[self.id]
                                    ['EDITOR_BOX_WIDTH'],
                                    globals.EDITOR_AREA[self.id]
                                    ['EDITOR_BOX_HEIGHT'])
        self.add(self.fixed)

        self.da = Gtk.DrawingArea()
        self.da.set_size_request(globals.EDITOR_AREA[self.id]
                                 ['EDITOR_BOX_WIDTH'],
                                 globals.EDITOR_AREA[self.id]
                                 ['EDITOR_BOX_HEIGHT'])
        self.da.modify_bg(Gtk.StateType.NORMAL,
                          style.Color(globals.EDITOR_AREA[self.id]
                                      ['EDITOR_BOX_BG'])
                          .get_gdk_color())

        self.fixed.put(self.da, 0, 0)

        # declare the list for storing all the contours
        self.contours = globals.EDITOR_AREA[self.id]['GLYPH'][:]

        self.tool = {}

        # declare the list for storing the drag points in the editing session
        self.points = []

        self.update_control_points()

        self.show_all()

        # connect the drawing area to the required events
        self.da.connect('draw', self._draw)

        self.connect("button-press-event", self._on_point_press)

        self.FILL = fill

        '''
        self.da.set_events(self.get_events()
                | Gdk.EventMask.LEAVE_NOTIFY_MASK
                | Gdk.EventMask.BUTTON_PRESS_MASK
                | Gdk.EventMask.POINTER_MOTION_MASK
                | Gdk.EventMask.POINTER_MOTION_HINT_MASK)
        '''
        # self.connect('key-press-event',self._on_key_press)
        # self.set_events(self.get_events() | Gdk.EventMask.KEY_PRESS_MASK)

    def _draw(self, da, cr):

        # draw all contours with control points
        self.draw_all_contours(cr, 0)

        # draw baseline, ascender, etc
        # return False

    def _on_point_press(self, widget, event):

        if event.type == Gdk.EventType.BUTTON_PRESS\
                and event.button == 3:
            # toggle the bezier pen tool
            # print "a right click was noticed"

            try:
                flag = isinstance(self.tool["BezierPen"], BezierPenTool)

            except Exception:
                flag = False

            if flag:
                if self.tool["BezierPen"].get_active():
                    self.tool["BezierPen"].set_active(False)
                    # print "pen tool deactivated"
                    self.update_control_points()
                else:
                    self.tool["BezierPen"].set_active(True)
                    # print "pen tool activated"
            else:
                self.tool["BezierPen"] = BezierPenTool(self)
                # print "pen tool activated"

    def update_control_points(self):
        # delete the current set of drag points
        for point in self.points:
            self.fixed.remove(point)
            point.destroy()
            del point

        del self.points
        self.points = []

        for contour in self.contours:
            # print len(contour)
            for point in contour:
                # print "adding: " + str(point.x) + ", " + str(point.y)
                self.add_point(point)

        self.update_bindings()

    def update_bindings(self):
        c = 0
        for contour in self.contours:
            for j, point in enumerate(contour):
                if point.segmentType == u'curve' \
                        and point.smooth is True:
                    if j != 0:
                        bind(self.points[c - 1], self.points[c],
                             self.points[c + 1])
                    else:
                        bind(self.points[c + len(contour) - 1],
                             self.points[c], self.points[c + 1])
                c += 1

    def add_contour(self, contour):

        self.contours.append(contour)
        self.update_control_points()

    def draw_all_contours(self, cr, pos):

        for contour in self.contours:
            if len(contour[:]) != 0:

                # Set line style
                cr.set_source_rgb(0, 0, 0)
                cr.set_line_width(3)
                pen = GtkPen(cr, pos, self.id)
                contour.draw(pen)

                # close the contour

                # Draw a Hallo around the first point of an open contour
                if self.FILL is True or contour.open is False:
                    cr.close_path()
                else:
                    if contour.dirty is True:
                        cr.stroke()
                        cr.set_source_rgb(0.3, 0.3, 0.3)
                        cr.set_line_width(1)

                        r = globals.X(contour[0].x + globals.ZONE_R,
                                      self.id) -\
                            globals.X(contour[0].x, self.id)
                        pen.moveTo((contour[0].x + globals.ZONE_R,
                                    contour[0].y))
                        cr.arc(globals.X(contour[0].x. self.id),
                               globals.Y(contour[0].y. self.id),
                               r, 0, 2 * math.pi)

                cr.stroke()

                # draw construction lines
                cr.set_source_rgb(0.3, 0.3, 0.3)
                cr.set_line_width(1)

                for i, segment in enumerate(contour.segments):
                    if segment[-1].segmentType == u'line' and\
                            len(segment) == 1:
                        # print "line"
                        # No construction lines required
                        pass

                    elif segment[-1].segmentType == u'move' and\
                            len(segment) == 1:
                        # No construction lines required
                        pass

                    elif segment[-1].segmentType == u'curve' and\
                            len(segment) == 3:
                        pen.moveTo((contour.segments[i - 1][-1].x,
                                    contour.segments[i - 1][-1].y))
                        pen.lineTo((segment[0].x, segment[0].y))
                        pen.moveTo((segment[1].x, segment[1].y))
                        pen.lineTo((segment[2].x, segment[2].y))

                    else:
                        # print segment[-1].segmentType
                        # print len(segment)
                        raise NotImplementedError

                    cr.stroke()

        if self.FILL is True:

            cr.set_source_rgb(1, 1, 1)
            cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
            cr.fill()

    def add_point(self, p):

        point = DragPoint(p, self.id)
        point.connect("notify", self.redraw)
        self.fixed.put(point, point.get_corner_x(), point.get_corner_y())
        self.points.append(point)

        # Bidirectional binding between the Defcon Point and the Drag Point
        # point.is_appearance_for(p)
        # point.connect("notify", lambda _: p.x = widget.x)

    def redraw(self, point, property):

        self.da.queue_draw()
