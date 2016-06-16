from gi.repository import Gtk, Gdk
import cairo
import math
from defcon import Font
from defconGTK.renderGlyph import renderGlyph

#Making a glyph editor box
"""
class EditorBox(Gtk.VBox):
"""
#This Box is the Area where the Glyph will be edited
"""
    def __init__(self, font, glyphName):
        super(EditorBox, self).__init__()
        
        self.boxWidth = 400
        self.boxHeight = 400
        self.font = font
        self.h= font.info.ascender - font.info.descender 
        self.b= -font.info.descender
        self.glyph = font[glyphName]
        self.init_ui()

    def init_ui(self):    
        self.da = Gtk.DrawingArea()
        self.da.connect("draw", self._drawGlyph)
        self.da.set_size_request(self.boxWidth, self.boxHeight)
        
        #self.pack_start(Gtk.Label("Hello"), False, False, 30)
        #self.da = renderGlyph(self.glpyh, self.boxWidth, self.boxHeight, self.h, self.b)
        
        self.pack_start(self.da, False, False, 30)                     
        self.show_all()

    def _drawGlyph(self, widget, cr):
        
        # Normalizing the canvas
        cr.scale(self.boxWidth, self.boxHeight) 
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
    
    #define the transformations for the points here
    
    def X (self, x):
        t= 0.5 - float(self.w)/(2*self.h) + float(x)/self.h
        #print("X=" + str(t))
        return t

    def Y (self, y):
        t= 1- float(self.b)/(self.h) - float(y)/self.h
        #print("Y=" + str(t))
        return t
"""

class EditorBox(Gtk.Box):

    def __init__(self, font, glyphName):
        super(EditorBox, self).__init__()
        self.boxWidth = 400
        self.boxHeight = 400
        
        self.glyph = font[glyphName]

        #The advance width of the glyph
        self.w  = self.glyph.width;
        
        #The difference in the ascender and the descender values
        self.h= font.info.ascender - font.info.descender
        
        #the distance between the baseline and the descender
        self.b= -font.info.descender

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
    
    #define the transformations for the points here
    
    def X (self, x):
        t= 0.5 - float(self.w)/(2*self.h) + float(x)/self.h
        #print("X=" + str(t))
        return t

    def Y (self, y):
        t= 1- float(self.b)/(self.h) - float(y)/self.h
        #print("Y=" + str(t))
        return t