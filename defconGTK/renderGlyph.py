from gi.repository import Gtk, Gdk
import cairo
import math
from defcon import Font
 
class renderGlyph(Gtk.Box):

    _boxWidth = 100
    _boxHeight= 100

    def __init__(self, glyph, boxHeight=100, boxWidth=100):
        super(renderGlyph, self).__init__()
        self._boxHeight = boxHeight
        self._boxWidth = boxWidth
        self.glyph = glyph
        self.init_ui()
        
    def init_ui(self):    
        self.da = Gtk.DrawingArea()
        self.da.connect("draw", self.drawGlyph)
        self.da.set_size_request(self._boxWidth, self._boxHeight)
        self.add(self.da)             
        
        #find the bounds of the glyph to normalise the points later
        bounds = self.glyph.bounds;
        self.glyphWidth  = bounds[2] - bounds[0]
        self.glyphHeight = bounds[3] - bounds[1]

        self.show_all()

    def drawGlyph(self, widget, cr):
        
        # Normalizing the canvas
        cr.scale(self._boxWidth, self._boxHeight) 
        cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)

        cr.rectangle (0, 0, 1, 1) # Rectangle(x0, y0, x1, y1)
        cr.set_source_rgb(1, 1, 1)
        cr.fill ()

        cr.set_source_rgb(0, 0, 0)

        for contour in self.glyph:
            
            #move to initial point
            point = contour[0]
            cr.move_to(self.X(point.x),self.Y(point.y))
                        
            for segment in contour.segments:
                #first determine type of Segment
                if len(segment) == 3:
                    #its a bezier
                    cr.curve_to(self.X(segment[0].x),self.Y(segment[0].y),self.X(segment[1].x),self.Y(segment[1].y),self.X(segment[2].x),self.Y(segment[2].y))

                elif len(segment) == 1:
                    #its a line
                    cr.line_to(self.X(segment[0].x),self.Y(segment[0].y))

                else:
                    print("Error: Unknown Case Found")            
                    print(segment)

            #close the contour
            cr.close_path()
            
        #fill the contour
        cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD);
        cr.fill();             
        cr.stroke()
    
    def X (self, x):
        t=float(x - self.glyph.bounds[0])/self.glyphWidth
        return t

    def Y (self, y):
        t=float(y - self.glyph.bounds[1])/self.glyphHeight
        return 1-t
