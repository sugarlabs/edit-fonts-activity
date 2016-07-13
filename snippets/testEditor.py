import math

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf, GLib, Gio, GObject

import cairo

from defcon import Font, Point, Contour  

from fontTools.pens.basePen import BasePen


EDITOR_BOX_WIDTH = 600
EDITOR_BOX_HEIGHT = 600

FONT = Font("../test_fonts/Noto.ufo")
GLYPH = FONT["P"]


"""
class GContour(Contour):
	
	def __init__(self):

"""

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
		
		#self.points = [(i*50, i*40) for i in range(6)]
		
		self.points = []
		
		for i in range(6):
			self.add_point(200, i*50)
		
		self.show_all()

		self.contours = GLYPH[:]

		#declare bezier curves for the above points
		self.curves = [Curve(self.points[:4]), Curve(self.points[3:])]
		
		#declare the bindings 
		bind(self.points[2], self.points[3], self.points[4])
		
		#connect the drawing area to the required events
		self.da.connect('draw', self._draw)
		
		#self.set_events(Gdk.EventType.BUTTON_PRESS)
		#self.da.connect("button-press-event", self._on_button_press)

		'''
		self.da.set_events(self.get_events()
				| Gdk.EventMask.LEAVE_NOTIFY_MASK
				| Gdk.EventMask.BUTTON_PRESS_MASK
				| Gdk.EventMask.POINTER_MOTION_MASK
				| Gdk.EventMask.POINTER_MOTION_HINT_MASK)
		'''

	def _on_point_press(self, widget, event):
		
		if event.type == Gdk.EventType.BUTTON_PRESS:
			print "Yo1"    

	def _on_point_release(self, widget, event):
		
		if event.type == Gdk.EventType.BUTTON_RELEASE:
			print "Yo2"    

	def add_contour(self, contour):

		self.contours.append(contour)


	def _on_button_press(self, w, e):

		print "Yo"

		if e.type == Gdk.EventType.BUTTON_PRESS: 
			#\
		    #and e.button == MouseButtons.LEFT_BUTTON:
		    print e.button
		    #self.coords.append([e.x, e.y])
		    
			#if e.type == Gdk.EventType.BUTTON_PRESS \
			#    and e.button == MouseButtons.RIGHT_BUTTON:
			#    
			#    self.darea.queue_draw()                                                                   


	def draw_all_contours(self, cr, pos):
		pen = GPen(cr, pos)
		for contour in self.contours:
			cr.set_line_width(3)
			contour.draw(pen)
			#close the contour
			cr.close_path()
			cr.stroke()

			#draw control points
			for segment in contour.segments:
				if segment[-1].segmentType == u'line':
					pass
					#print "It's a line of " + str(len(segment))  
				elif segment[-1].segmentType == u'curve':
					pass
					#print "It's a curve of " + str(len(segment)) 
				elif segment[-1].segmentType == u'move':
					pass
					#print "It's a move of " + str(len(segment))
				elif segment[-1].segmentType == u'qcurve':
					pass
					#print "It's a qcurve of " + str(len(segment)) 
 

	def _draw(self, da, cr):

		#draw all contours with control points
		self.draw_all_contours(cr, 0)
		
		"""
		pos += FONT["Y"].width
		self.contours = FONT["a"][:]
		self.draw_glyph(cr, 200)
		"""
		#draw baseline, ascender, etc

		return False

	def add_point(self, x, y):
		
		point = DragPoint(x, y)
		point.connect("notify", self.redraw)
		self.fixed.put(point,point.get_corner_x(),point.get_corner_y())
		self.points.append(point)

	def redraw(self, point, property):
		
		self.da.queue_draw()




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


