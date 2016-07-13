from gi.repository import Gtk, Gdk
# import cairo
# import math
# from defcon import Font
import editfonts.globals as globals

# Making a glyph editor box
from editfonts.objects.gtkpen import GtkPen
from editfonts.widgets.dragpoint import DragPoint
# from editfonts.objects.basesegment import BaseSegment
from editfonts.objects.bezierpen import BezierPenTool


def bind(A, O, B):

    # FIX ME: a none type point shouldn't be bind to a curve
    # type point with a line or curve type point next to it
    # This currently shows an error
    if A.point.segmentType != u'line' or A.point.segmentType != u'curve' \
            or B.point.segmentType != u'line' \
            or B.point.segmentType != u'curve':
        A.bind_to(O, B)
        B.bind_to(O, A)

    O.bind_to(A, B)


class EditorBox(Gtk.EventBox):

    def __init__(self):

        super(EditorBox, self).__init__()

        self.set_size_request(globals.EDITOR_BOX_WIDTH,
                              globals.EDITOR_BOX_HEIGHT)

        self.fixed = Gtk.Fixed()
        self.fixed.set_size_request(globals.EDITOR_BOX_WIDTH,
                                    globals.EDITOR_BOX_HEIGHT)
        self.add(self.fixed)

        self.da = Gtk.DrawingArea()
        self.da.set_size_request(globals.EDITOR_BOX_WIDTH,
                                 globals.EDITOR_BOX_HEIGHT)

        self.fixed.put(self.da, 0, 0)

        # declare the list for storing all the contours
        self.contours = globals.GLYPH[:]

        self.tool = {}

        # declare the list for storing the drag points in the editing session
        self.points = []

        self.update_control_points()

        self.show_all()

        # connect the drawing area to the required events
        self.da.connect('draw', self._draw)

        self.connect("button-press-event", self._on_point_press)

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
            print "a right click was noticed"

            try:
                flag = isinstance(self.tool["BezierPen"], BezierPenTool)

            except Exception:
                flag = False

            if flag:
                if self.tool["BezierPen"].get_active():
                    self.tool["BezierPen"].set_active(False)
                    print "pen tool deactivated"
                else:
                    self.tool["BezierPen"].set_active(True)
                    print "pen tool activated"
            else:
                self.tool["BezierPen"] = BezierPenTool(self)
                print "pen tool activated"

    def update_control_points(self):
        # delete the current set of drag points
        for point in self.points:
            point.destroy()
            del point

        self.points = []

        for contour in self.contours:
            for point in contour:
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

        pen = GtkPen(cr, pos)
        for contour in self.contours:
            if len(contour[:]) != 0:
                cr.set_source_rgb(0, 0, 0)
                cr.set_line_width(3)
                contour.draw(pen)
                # close the contour

                cr.close_path()
                cr.stroke()

                # draw control points
                cr.set_source_rgb(0.3, 0.3, 0.3)
                cr.set_line_width(1)

                for i, seg in enumerate(contour.segs):
                    if seg[-1].segType == u'line' and len(seg) == 1:
                        # print "line"
                        # No construction lines required
                        pass

                    elif seg[-1].segType == u'move' and len(seg) == 1:
                        # No construction lines required
                        pass

                    elif seg[-1].segType == u'curve' and len(seg) == 3:
                        pen.moveTo((contour.segs[i - 1][-1].x,
                                    contour.segs[i - 1][-1].y))
                        pen.lineTo((seg[0].x, seg[0].y))
                        pen.moveTo((seg[1].x, seg[1].y))
                        pen.lineTo((seg[2].x, seg[2].y))

                    else:
                        print seg[-1].segType
                        print len(seg)
                        raise NotImplementedError

                cr.close_path()
                cr.stroke()

    def add_point(self, p):

        point = DragPoint(p)
        point.connect("notify", self.redraw)
        self.fixed.put(point, point.get_corner_x(), point.get_corner_y())
        self.points.append(point)

        # Bidirectional binding between the Defcon Point and the Drag Point
        # point.is_appearance_for(p)
        # point.connect("notify", lambda _: p.x = widget.x)

    def redraw(self, point, property):

        self.da.queue_draw()
