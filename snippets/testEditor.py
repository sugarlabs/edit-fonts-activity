import math

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import cairo
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib, Gio, GObject

from defcon import Font, Point, Contour  

from fontTools.pens.basePen import BasePen

EDITOR_BOX_WIDTH = 600
EDITOR_BOX_HEIGHT = 600

FONT = Font("../test_fonts/Noto.ufo")
GLYPH = FONT["J"]

class GPen(BasePen):
	"""
	This class is a subclass of the BasePen Class from fontTools 
	which converts any segement type to simple moveto, lineto, curveto statements
	"""

	def __init__(self, cr, pos):
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

	#define the transformations for the points here
	def X(self, x):
		t = self.pos + float(self.w - x) * EDITOR_BOX_HEIGHT/ self.h
		#print("X=" + str(t))
		return t

	def Y(self, y):
		t = float(self.h - y - self.b) * EDITOR_BOX_HEIGHT/ self.h
		#print("Y=" + str(t))
		return t

	def _moveTo(self, p):
		x, y = p
		self.cr.move_to(self.X(x),self.Y(y))
		print "move ->" + str(x) + "," + str(y)

	def _lineTo(self, p):
		x, y = p
		self.cr.line_to(self.X(x),self.Y(y))
		print "line ->" + str(x) + "," + str(y)

	def _curveToOne(self, p1, p2, p3):
		x1, y1 = p1
		x2, y2 = p2
		x3, y3 = p3
		self.cr.curve_to(self.X(x1),self.Y(y1),self.X(x2),self.Y(y2),self.X(x3),self.Y(y3))
		print "curve ->" + str(x1) + "," + str(y1) + "|" + str(x2) + "," + str(y2) + "|" + str(x3) + "," + str(y3)

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

"""
class GContour(Contour):
	
	def __init__(self):

"""


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

		"""
		if self.point_type is "OffCurveSmooth":
			self.binding.append(points[0])
			self.binding.append(points[1])

		elif self.point_type is "OnCurveSmooth":
			self.binding[0] = points[0]
			self.binding[1] = points[1]
	
		"""

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
			
			print "moving B"

		elif self.type is "OnCurveSmooth":
			A = self.binding[0]
			B = self.binding[1]
			
			B.update(B.get_x() + dx, B.get_y() + dy) 
			A.update(A.get_x() + dx, A.get_y() + dy) 

			print "moving A and B"

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
			print "I'm here"
			print self.binding
			print self.type
			self.update_connected_points(dx - self.r, dy - self.r)

		return True

	def update(self, x, y):
		self.set_x(x)
		self.set_y(y)

		print "[" + str(self.x) + "," + str(self.x) + "]"   

		self.get_parent().move(self, self.get_corner_x(), self.get_corner_y())

	def get_x(self):

		return self.x

	def get_y(self):

		return self.y

	def set_x(self, x):

		self.x = x
	
		#validate the move
		#see that the points dont go outside the drawing area
		if self.x > EDITOR_BOX_WIDTH: 
			self.x = EDITOR_BOX_WIDTH
		elif self.x < 0: 
			self.x = 0

	def set_y(self, y):

		self.y = y
	
		#validate the move
		#see that the points dont go outside the drawing area
		if self.y > EDITOR_BOX_HEIGHT: 
			self.y = EDITOR_BOX_HEIGHT
		elif self.y < 0: 
			self.y = 0

class Curve:

	def __init__(self, pointList):

		self.points = pointList[:]

	def draw(self, cr):

		cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)

		#setting the line style to solid

		cr.set_line_width(4)
		cr.set_source_rgb(0.1, 0.1, 0.1)

		#Drawing the Bezier Curve
		cr.move_to(self.points[0].x, self.points[0].y)
		cr.curve_to(self.points[1].x, self.points[1].y, self.points[2].x \
				, self.points[2].y, self.points[3].x, self.points[3].y)
		
		cr.stroke_preserve()
		cr.stroke ()
		
		#Drawing the support lines
		
		#setting the line style to dashed
		cr.set_line_width(1)
		cr.set_source_rgb(0.3, 0.3, 0.3)

		cr.move_to(self.points[0].x, self.points[0].y)
		cr.line_to(self.points[1].x, self.points[1].y)
		cr.move_to(self.points[2].x, self.points[2].y)
		cr.line_to(self.points[3].x, self.points[3].y)
				
		cr.stroke_preserve()
		cr.stroke()

		#cr.close_path ()
		#cr.fill ()
		return False

class EditorBox(Gtk.EventBox):

	def __init__(self):
		
		super(EditorBox, self).__init__()
		
		self.set_size_request(EDITOR_BOX_WIDTH, EDITOR_BOX_HEIGHT)
		
		self.fixed = Gtk.Fixed()
		self.fixed.set_size_request(EDITOR_BOX_WIDTH, EDITOR_BOX_HEIGHT)
		self.add(self.fixed)

		self.da = Gtk.DrawingArea()
		self.da.set_size_request(EDITOR_BOX_WIDTH, EDITOR_BOX_HEIGHT)

		self.fixed.put(self.da,0,0)
		
		self.points = []
		self.show_all()

		self.contours = GLYPH[:]

		#declare bezier curves for the above points
		#self.curves = [Curve(self.points[:4]), Curve(self.points[3:])]
		
		#declare the bindings 
		#bind(self.points[2], self.points[3], self.points[4])
		
		#connect the drawing area to the required events
		self.da.connect('draw', self._draw)
		#self.da.connect("button-press-event", self._on_button_press)

	def add_contour(self, contour):

		self.contours.append(contour)

	def _on_button_press(self, w, e):

		if e.type == Gdk.EventType.BUTTON_PRESS: 
			#\
		    #and e.button == MouseButtons.LEFT_BUTTON:
		    print e.button
		    #self.coords.append([e.x, e.y])
		    
			#if e.type == Gdk.EventType.BUTTON_PRESS \
			#    and e.button == MouseButtons.RIGHT_BUTTON:
			#    
			#    self.darea.queue_draw()                                                                   

	def draw_all_contours(self, cr):
		for contour in self.contours:
			pen = GPen(cr, 50)
			cr.set_line_width(3)
			contour.draw(pen)
			#close the contour
			cr.close_path()
			cr.stroke()

			#draw control points
			for segment in contour.segments:
				if segment[-1].segmentType == u'line':
					print "It's a line of " + str(len(segment))  
				elif segment[-1].segmentType == u'curve':
					print "It's a curve of " + str(len(segment)) 
				elif segment[-1].segmentType == u'move':
					print "It's a move of " + str(len(segment))
				elif segment[-1].segmentType == u'qcurve':
					print "It's a qcurve of " + str(len(segment)) 
 

	def _draw(self, da, cr):

		#draw all contours with control points
		self.draw_all_contours(cr)

		#draw baseline, ascender, etc

		return False

	def add_point(self, x, y):
		
		point = DragPoint(x, y)
		point.connect("notify", self.redraw)
		self.fixed.put(point,point.get_corner_x(),point.get_corner_y())
		self.points.append(point)

	def redraw(self, point, property):
		
		self.da.queue_draw()

"""
class BezierPenTool:

	def __init__(self):
		self.is_active = True
		self.Contour

	def set_state_active(self, state):
		if state == True:
			self.is_active = True 
		else:
			self.is_active = False 

	def get_state(self):
		return self.is_active

"""

class MyWindow(Gtk.Window):

    def __init__(self):
		Gtk.Window.__init__(self, title="Editor Area")
		self.set_size_request(EDITOR_BOX_WIDTH, EDITOR_BOX_HEIGHT)		
		self.editorBox = EditorBox()
		self.add(self.editorBox)

		self.show_all()

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()


