#!/usr/bin/python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import cairo
import math
from defcon import Font
 
class Render(Gtk.Window):

    def __init__(self):
        super(Render, self).__init__()
        
        self.init_ui()
        
        
    def init_ui(self):    

        self.darea = Gtk.DrawingArea()
        self.darea.connect("draw", self.on_draw)
        #self.darea.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)        
        self.add(self.darea)
        
        self.coords = []
                     
        #self.darea.connect("button-press-event", self.on_button_press)

        self.set_title("Redering the Glyph")
        self.resize(1000, 1000)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()


    #def drawSegment(self, wid, cr, segment):

        
    def on_draw(self, wid, cr):

        #load glyph data
        path = "sample"
        font = Font(path)
        glyph = font["P"]

        cr.set_source_rgb(0, 0, 0)
        cr.set_line_width(10)
        cr.scale(0.6, 0.6)

        for contour in glyph:
            
            #move to initial point
            point = contour[0]
            cr.move_to(point.x,1000 - point.y)
            
            for segment in contour.segments:
                #drawSegment(wid, cr, segment)
                #first determine type of Segment
                if len(segment) == 3:
                    #its a bezier
                    cr.curve_to(segment[0].x,1000-segment[0].y,segment[1].x,1000-segment[1].y,segment[2].x,1000-segment[2].y)

                elif len(segment) == 1:
                    #its a line
                    cr.line_to(segment[0].x,1000-segment[0].y);

                else:
                    print("Error: Unknown Case Found")            
                    print(segment)
                    Gtk.main_quit()

            #cr.set_line_join(cairo.LINE_JOIN_ROUND)
            cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD);
            cr.fill();
            #cr.stroke()
            #close the contour
            #consider it closed
            #fill the contour
                         
def main():
    
    app = Render()
    Gtk.main()
        
        
if __name__ == "__main__":    
    main()