import math

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import cairo
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib, Gio, GObject

from defcon import Font, Point, Contour  

from fontTools.pens.basePen import BasePen

TESTING_BOX_WIDTH = 600
TESTING_BOX_HEIGHT = 600

FONT = Font("../test_fonts/Noto.ufo")
GLYPH = FONT["P"]

class GPen(BasePen):
	"""
	This class is a subclass of the BasePen Class from fontTools 
	which converts any segement type to simple moveto, lineto, curveto statements
	"""

	def __init__(self, cr, pos, scale = 1.0):
		BasePen.__init__(self, glyphSet={})
		self.cr = cr
		
		#the position the glyph is at while drawing it in a string of glyphs
		self.pos = pos
		
		#The advance width of the glyph
		self.w = GLYPH.width

		#The difference in the ascender and the descender values
		self.h = FONT.info.ascender - FONT.info.descender

		#the distance between the baseline and the descender
		self.b = 0 - FONT.info.descender

		#the scale of the drawing
		self.scale = scale

	#define the transformations for the points here
	def X(self, x):
		t = self.pos + float(x) * TESTING_BOX_HEIGHT / self.h
		return t * self.scale

	def Y(self, y):
		t = float(self.h - y - self.b) * TESTING_BOX_HEIGHT / self.h
		return t * self.scale

	def convertToScale(self, X):
		return X * self.scale * TESTING_BOX_HEIGHT / float(self.h)
 
	def _moveTo(self, p):
		x, y = p
		self.cr.move_to(self.X(x),self.Y(y))

	def _lineTo(self, p):
		x, y = p
		self.cr.line_to(self.X(x),self.Y(y))

	def _curveToOne(self, p1, p2, p3):
		x1, y1 = p1
		x2, y2 = p2
		x3, y3 = p3
		self.cr.curve_to(self.X(x1),self.Y(y1),self.X(x2),self.Y(y2),self.X(x3),self.Y(y3))


def distance(X, Y):

	t1 = (X.get_x() - Y.get_x())
	t2 = (X.get_y() - Y.get_y())
	return math.sqrt(t1*t1 + t2*t2)

def slope(X, Y):

	t1 = (X.get_x() - Y.get_x())
	t2 = (X.get_y() - Y.get_y())
	return float(t2)/t1

def bind(A, O, B):
	
	A.set_type("OffCurveSmooth")
	A.bind_to(O, B)
	
	B.set_type("OffCurveSmooth")
	B.bind_to(O, A)
	
	O.set_type("OnCurveSmooth")
	O.bind_to(A, B)


class DragPoint(Gtk.EventBox):

	def __init__(self, x, y, pointType = "onCurve"):
		
		super(DragPoint, self).__init__()
		self.x = x
		self.y = y

		self.type = pointType
		self.binding = []

		#radius of the point
		self.r = 8
		
		self.set_size_request(self.r *2,self.r *2)		

		WIDTH = self.r *2
		HEIGHT = self.r *2		

		surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
		cr = cairo.Context (surface)
		cr.scale (WIDTH, HEIGHT) # Normalizing the canvas
		cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)

		cr.set_line_width(0.1)
		cr.set_source_rgb(0.7, 0.2, 0.0)
		cr.translate (0.5, 0.5)
		cr.arc(0, 0, 0.3, 0, 2 * math.pi)
		cr.stroke_preserve()
		
		cr.close_path ()
		cr.fill ()
		cr.stroke ()

		pixbuf = Gdk.pixbuf_get_from_surface(surface, 0, 0, self.r * 2, self.r * 2);
		transparent = pixbuf.add_alpha(True, 0xff, 0xff, 0xff)
		image = Gtk.Image.new_from_pixbuf(transparent)
		self.add(image)

		self.set_above_child(True)

		self.connect("motion-notify-event", self._on_motion)

		self.set_events(self.get_events()
				| Gdk.EventMask.LEAVE_NOTIFY_MASK
				| Gdk.EventMask.BUTTON_PRESS_MASK
				| Gdk.EventMask.POINTER_MOTION_MASK
				| Gdk.EventMask.POINTER_MOTION_HINT_MASK)

		self.show_all()

	def set_type(self, pointType):
		
		self.type = pointType

	def bind_to(self, *points):
		
		self.binding.append(points[0])
		self.binding.append(points[1])

	def update_connected_points(self, dx, dy):
		
		if self.type is "OffCurveSmooth":
			O = self.binding[0]
			B = self.binding[1]
			
			r = distance(O,B)
			d = distance(O,self)
			#m = slope(self,O)
			
			#t = r*r/(m*m + 1)
			#t = math.sqrt(t)
			
			#B.update(O.get_x() + t, O.get_y() + m*t)
			B.update(O.get_x() + (O.get_x()-self.get_x())*r/d, O.get_y() + (O.get_y()-self.get_y())*r/d)
			

		elif self.type is "OnCurveSmooth":
			A = self.binding[0]
			B = self.binding[1]
			
			B.update(B.get_x() + dx, B.get_y() + dy) 
			A.update(A.get_x() + dx, A.get_y() + dy) 

	def _on_point_press(self, widget, event):
		
		if event.type == Gdk.EventType.BUTTON_PRESS:
			self.drag_state = True
			return False    

	def _on_point_release(self, widget, event):
		
		if event.type == Gdk.EventType.BUTTON_RELEASE:
			self.drag_state = False
			return False   

	def get_corner_x(self):
		
		return self.x - self.r
	
	def get_corner_y(self):
		
		return self.y - self.r

	def _on_motion(self, widget, event):

		(window, dx, dy, state) = event.window.get_pointer()
		
		if state & Gdk.ModifierType.BUTTON1_MASK:

			#update the position of the point			
			self.update(self.get_x() + dx - self.r, self.get_y() + dy - self.r)
						
			#update the position of the points binded with this point
			self.update_connected_points(dx - self.r, dy - self.r)

		return True

	def update(self, x, y):
		self.set_x(x)
		self.set_y(y)

		self.get_parent().move(self, self.get_corner_x(), self.get_corner_y())

	def get_x(self):

		return self.x

	def get_y(self):

		return self.y

	def set_x(self, x):

		self.x = x
	
		#validate the move
		#see that the points dont go outside the drawing area
		if self.x > TESTING_BOX_WIDTH: 
			self.x = TESTING_BOX_WIDTH
		elif self.x < 0: 
			self.x = 0

	def set_y(self, y):

		self.y = y
	
		#validate the move
		#see that the points dont go outside the drawing area
		if self.y > TESTING_BOX_HEIGHT: 
			self.y = TESTING_BOX_HEIGHT
		elif self.y < 0: 
			self.y = 0


class TestingBox(Gtk.EventBox):

	def __init__(self):
		
		super(TestingBox, self).__init__()
		
		self.set_size_request(TESTING_BOX_WIDTH, TESTING_BOX_HEIGHT)
		
		self.fixed = Gtk.Fixed()
		self.fixed.set_size_request(TESTING_BOX_WIDTH, TESTING_BOX_HEIGHT)
		self.add(self.fixed)

		self.da = Gtk.DrawingArea()
		self.da.set_size_request(TESTING_BOX_WIDTH, TESTING_BOX_HEIGHT)

		self.fixed.put(self.da,0,0)
		
		self.string = "Hello"
		self.positions = []
		self.show_all()

		#connect the drawing area to the required events
		self.da.connect('draw', self._draw)

	def draw_glyph(self, glyph, cr, pos):
		
		pen = GPen(cr, pos, 0.3)
		
		print "position: " + str(pos)

		#glyph.draw(pen)
		for contour in glyph:
			cr.set_line_width(3)
			contour.draw(pen)
			#close the contour
			cr.close_path()
			cr.stroke()

		print glyph.width  
		self.positions.append(3 * pen.convertToScale(glyph.width))
		print self.positions

		"""
		for contour in glyph:
			cr.set_line_width(3)
			contour.draw(pen)
			#close the contour
			cr.close_path()
			cr.stroke()
		"""

	def _draw(self, da, cr):

		#draw all contours with control points
		self.positions = [0]

		for i , char in enumerate(self.string):
			self.draw_glyph(FONT[char], cr, self.positions[-1])

		"""
		pos += FONT["Y"].width
		self.contours = FONT["a"][:]
		self.draw_glyph(cr, 200)
		"""
		#draw baseline, ascender, etc

		return False

	def redraw(self, point, property):
		
		self.da.queue_draw()


class MyWindow(Gtk.Window):

    def __init__(self):
		Gtk.Window.__init__(self, title="Testing Area")
		self.set_size_request(TESTING_BOX_WIDTH, TESTING_BOX_HEIGHT)		
		self.testingBox = TestingBox()
		self.add(self.testingBox)

		self.show_all()


win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()