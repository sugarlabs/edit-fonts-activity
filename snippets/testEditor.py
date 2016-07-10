import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import cairo
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib, Gio, GObject

from defcon import Font, Point, Contour  
import math

EDITOR_BOX_WIDTH = 500
EDITOR_BOX_HEIGHT = 500

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
		ctx = cairo.Context (surface)
		ctx.scale (WIDTH, HEIGHT) # Normalizing the canvas
		ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)

		ctx.set_line_width(0.1)
		ctx.set_source_rgb(0.7, 0.2, 0.0)
		ctx.translate (0.5, 0.5)
		ctx.arc(0, 0, 0.3, 0, 2 * math.pi)
		ctx.stroke_preserve()
		
		ctx.close_path ()
		ctx.fill ()
		ctx.stroke ()

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

	def draw(self, ctx):

		ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)

		#setting the line style to solid

		ctx.set_line_width(4)
		ctx.set_source_rgb(0.1, 0.1, 0.1)

		#Drawing the Bezier Curve
		ctx.move_to(self.points[0].x, self.points[0].y)
		ctx.curve_to(self.points[1].x, self.points[1].y, self.points[2].x \
				, self.points[2].y, self.points[3].x, self.points[3].y)
		
		ctx.stroke_preserve()
		ctx.stroke ()
		
		#Drawing the support lines
		
		#setting the line style to dashed
		ctx.set_line_width(1)
		ctx.set_source_rgb(0.3, 0.3, 0.3)

		ctx.move_to(self.points[0].x, self.points[0].y)
		ctx.line_to(self.points[1].x, self.points[1].y)
		ctx.move_to(self.points[2].x, self.points[2].y)
		ctx.line_to(self.points[3].x, self.points[3].y)
				
		ctx.stroke_preserve()
		ctx.stroke()

		#ctx.close_path ()
		#ctx.fill ()
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

		for i in range(7):
			self.add_point(i*40 + 100, i*20 + 50)
		
		#declare bezier curves for the above points
		self.curves = [Curve(self.points[:4]), Curve(self.points[3:])]
		
		#declare the bindings 
		bind(self.points[2], self.points[3], self.points[4])
		
		#connect the drawing area to the required events
		self.da.connect('draw', self._draw)
		self.da.connect("button-press-event", self._on_button_press)

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

	def _draw(self, da, ctx):

		#draw all bezier curves
		for curve in self.curves:
			curve.draw(ctx) 

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


