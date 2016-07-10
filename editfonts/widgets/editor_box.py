from gi.repository import Gtk, Gdk
import cairo
import math
from defcon import Font
import x

#Making a glyph editor box

class EditorBox(Gtk.Box):
    
    def __init__(self):
        super(EditorBox, self).__init__()
        self.boxWidth = 400
        self.boxHeight = 400

        #The advance width of the glyph
        self.w = x.FONT[x.GLYPH_NAME].width

        #The difference in the ascender and the descender values
        self.h = x.FONT.info.ascender - x.FONT.info.descender

        #the distance between the baseline and the descender
        self.b = -x.FONT.info.descender

        self.init_ui()

    def init_ui(self):
        self.da = Gtk.DrawingArea()
        self.da.connect("draw", self.drawGlyph)
        self.da.set_size_request(self.boxWidth, self.boxHeight)
        self.add(self.da)

        #find the bounds of the glyph to normalise the points later

        self.show_all()

    def drawGlyph(self, widget, cr):

        # Normalizing the canvas
        cr.scale(self.boxWidth, self.boxHeight)
        cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)

        cr.rectangle(0, 0, 1, 1)  # Rectangle(x0, y0, x1, y1)
        cr.set_source_rgb(1, 1, 1)
        cr.fill()

        cr.set_source_rgb(0, 0, 0)
        
        for contour in x.FONT[x.GLYPH_NAME]:

            #move to initial point
            point = contour[0]
            cr.move_to(self.X(point.x), self.Y(point.y))
            #FIX ME: Validate the segments more thoroughly

            for segment in contour.segments:
                #first determine type of Segment
                if len(segment) >= 3 and segment[-1].segmentType == u'qcurve':
                    #its a Truetype quadractic B spline

                    for i, point in enumerate(segment):

                        if i is len(segment) - 2:
                            cr.curve_to(
                                self.X(point.x), self.Y(point.y),
                                self.X(point.x), self.Y(point.y),
                                self.X(segment[i + 1].x),
                                self.Y(segment[i + 1].y))

                            break

                        mid_point_x = (point.x + segment[i + 1].x) / 2
                        mid_point_y = (point.x + segment[i + 1].x) / 2
                        cr.curve_to(
                            self.X(point.x), self.Y(point.y), self.X(point.x),
                            self.Y(point.y), self.X(mid_point_x),
                            self.Y(mid_point_y))

                elif len(segment) is 3 and segment[-1].segmentType == u'curve':
                    #its a bezier
                    cr.curve_to(
                        self.X(segment[0].x), self.Y(segment[0].y),
                        self.X(segment[1].x), self.Y(segment[1].y),
                        self.X(segment[2].x), self.Y(segment[2].y))

                #Adding the support for qcurve
                elif len(segment) is 2 and segment[
                        -1].segmentType == u'qcurve':
                    #its a qcurve
                    cr.curve_to(
                        self.X(segment[0].x), self.Y(segment[0].y),
                        self.X(segment[0].x), self.Y(segment[0].y),
                        self.X(segment[1].x), self.Y(segment[1].y))

                elif len(segment) is 1 and segment[-1].segmentType == u'line':
                    #its a line
                    cr.line_to(self.X(segment[0].x), self.Y(segment[0].y))

                else:
                    #its a higher order curve or something
                    for point in segment:
                        cr.line_to(self.X(point.x), self.Y(point.y))

                    print("Error: Unknown Case Found")
                    print(segment)

            #close the contour
            cr.close_path()

            #fill the contour
    
        cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        cr.fill()
        cr.stroke()

    #define the transformations for the points here

    def X(self, x):
        t = 0.5 - float(self.w) / (2 * self.h) + float(x) / self.h
        #print("X=" + str(t))
        return t

    def Y(self, y):
        t = 1 - float(self.b) / (self.h) - float(y) / self.h
        #print("Y=" + str(t))
        return t
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
