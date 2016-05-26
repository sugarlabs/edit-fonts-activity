from gi.repository import Gtk, Gdk
import cairo
import math
from defcon import Font
from defconGTK.renderGlyph import renderGlyph


"""
This class makes a grid display with the assigned number of columns and the glyph list given
eg.
sampleGrid= glyphGridInstance(font, glyphList, 14, 80, 10)
"""
#this has to be converted to a GObject later -- still figuring this out
#GObject allow us to update these instances accordingly if any changes are made
class glyphGridInstance(Gtk.Box):

    #Grid Parameters
    #default values
    _GRID_HEIGHT= 7   #number of rows
    _GRID_WIDTH = 14  #number of columns  
    _GRID_BOX_SIZE = 80
    _GRID_ROW_SPACING = 10
    _GRID_COLUMN_SPACING = 10
    

    def __init__(self,font, glyphList, w=10, box_size=80, spacing=10):
        
        super(glyphGridInstance, self).__init__()
        self.grid = Gtk.Grid()
        self._GRID_WIDTH = w;  #number of columns  
        self._GRID_HEIGHT= len(glyphList)/w;  #number of rows
        self._GRID_BOX_SIZE = box_size;
        self._GRID_ROW_SPACING = spacing;
        self._GRID_COLUMN_SPACING = self._GRID_ROW_SPACING;
        
        self.grid.set_row_spacing(self._GRID_ROW_SPACING)
        self.grid.set_column_spacing(self._GRID_COLUMN_SPACING)

        # The alignment keeps the grid center aligned
        align = Gtk.Alignment(xalign=0.5,
                              yalign=0.5,
                              xscale=0,
                              yscale=0)
        align.add(self.grid)
        #self.set_orientation(Gtk.Orientation.VERTICAL)
        self.pack_start(align, True, True, 0)
        
        self.glyphList = glyphList
     
        self.font =font

        self.h= font.info.ascender - font.info.descender 

        self.b= -font.info.descender
 
        self.init_ui()
        print("yay")


    
    def init_ui(self):

        i=0
        j=0
        
        for glyphName in self.glyphList:
            
            box= Gtk.Box()
            print(glyphName)
            glyphBox = renderGlyph(self.font[glyphName], self._GRID_BOX_SIZE, self._GRID_BOX_SIZE, self.h, self.b)     
            box.add(glyphBox)
            self.grid.attach(box, i, j, 1, 1)
            print(str(i) + "," + str(j))
            i+=1
            if(i >= self._GRID_WIDTH):                
                i=0
                j+=1

    def changeList(self, glyphList):

        self.glyphList = glyphList
        self.init_ui()

    def changeFont(self, font):
        self.font = font                