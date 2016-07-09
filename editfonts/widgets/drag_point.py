from gi.repository import Gtk, Gdk
# from gi.repository import GLib, GdkPixbuf, Gio, GObject
import math
import cairo
import x


class DragPoint(Gtk.EventBox):

    def __init__(self, x, y):
        super(DragPoint, self).__init__()
        self.x = x
        self.y = y

        # radius of the point
        self.r = 8

        self.set_size_request(self.r * 2, self.r * 2)

        WIDTH = self.r * 2
        HEIGHT = self.r * 2

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
        ctx = cairo.Context(surface)
        ctx.scale(WIDTH, HEIGHT)  # Normalizing the canvas
        ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)

        ctx.set_line_width(0.1)
        ctx.set_source_rgb(0.7, 0.2, 0.0)
        ctx.translate(0.5, 0.5)
        ctx.arc(0, 0, 0.3, 0, 2 * math.pi)
        ctx.stroke_preserve()

        ctx.close_path()
        ctx.fill()
        ctx.stroke()

        pixbuf = Gdk.pixbuf_get_from_surface(surface, 0, 0, self.r * 2,
                                             self.r * 2)
        transparent = pixbuf.add_alpha(True, 0xff, 0xff, 0xff)
        image = Gtk.Image.new_from_pixbuf(transparent)
        self.add(image)

        self.set_above_child(True)

        self.connect("motion-notify-event", self._on_motion)

        self.set_events(self.get_events() | Gdk.EventMask.LEAVE_NOTIFY_MASK |
                        Gdk.EventMask.BUTTON_PRESS_MASK |
                        Gdk.EventMask.POINTER_MOTION_MASK |
                        Gdk.EventMask.POINTER_MOTION_HINT_MASK)

        self.show_all()

    def _on_point_press(self, widget, event):
        if event.type == Gdk.EventType.BUTTON_PRESS:
            self.drag_state = True
            # print "P(%d,%d)" %(event.x,event.y)
            return False

    def _on_point_release(self, widget, event):
        if event.type == Gdk.EventType.BUTTON_RELEASE:
            self.drag_state = False
            # print "R(%d,%d)" %(event.x,event.y)
            return False

    def get_corner_x(self):

        return self.x - self.r

    def get_corner_y(self):

        return self.y - self.r

    def _on_motion(self, widget, event):

        (window, dx, dy, state) = event.window.get_pointer()
        # print "motion event running at(%d,%d)" %(self.x + x, self.y + y)
        # print state & Gdk.ModifierType.BUTTON1_MASK
        if state & Gdk.ModifierType.BUTTON1_MASK:
            # self.point.drag_state:
            self.x += dx - self.r
            self.y += dy - self.r

            self.x = (self.x + globals.EDITOR_BOX_WIDTH) % \
                globals.EDITOR_BOX_WIDTH
            self.y = (self.y + globals.EDITOR_BOX_WIDTH) % \
                globals.EDITOR_BOX_WIDTH

            # print "M(%d,%d)" %(self.x, self.y)
            self.get_parent().move(self, self.get_corner_x(),
                                   self.get_corner_y())

        return True

    def _validate(self):

        self.x = (self.x + globals.EDITOR_BOX_WIDTH) % globals.EDITOR_BOX_WIDTH
        self.y = (self.y + globals.EDITOR_BOX_WIDTH) % globals.EDITOR_BOX_WIDTH
