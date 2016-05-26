from gi.repository import Gtk, Gdk
import cairo
import math
from defcon import Font
from defconGTK.renderGlyph import renderGlyph

class characterMap(Gtk.Box):

    #Grid Parameters
    #default values
    GRID_HEIGHT= 7   #number of rows
    GRID_WIDTH = 10  #number of columns  
    GRID_BOX_SIZE = 60
    GRID_ROW_SPACING = 5
    GRID_COLUMN_SPACING = 5
    
    def __init__(self,font, w=10, h=80, ui_type= 'Button'):
        
        super(characterMap, self).__init__()
        
        
        self.GRID_WIDTH = w;  #number of columns  
        self.GRID_HEIGHT= h;  #number of rows
        self.GRID_BOX_SIZE = 60;
        self.GRID_ROW_SPACING = 5;
        self.GRID_COLUMN_SPACING = self.GRID_ROW_SPACING;
        
        # The alignment keeps the grid center aligned
        self.align = Gtk.Alignment(xalign=0.5,
                              yalign=0.5,
                              xscale=0,
                              yscale=0)
        self.pack_start(self.align, True, True, 0)
        
        self.font =font
        self.h= font.info.ascender - font.info.descender 
        self.b= -font.info.descender

        self.glyphList=self.font.keys()
        self.marker=0    
        self.increment=self.GRID_HEIGHT*self.GRID_WIDTH
        
        if ui_type == 'Button':
            self.init_ui_button()
        elif ui.type == 'Scrolled':
            self.init_ui_scrollable()
        else:
            print("WARNING: Invalid ui_type for characterMap: " + ui_type)
            print("Choosing Button type instead")
            self.init_ui_button()

    def init_ui_button(self):

        #add buttons
        #back button goes at (0,int(gridHeight/2))
        #next button goes at (w+1,int(gridHeight/2))
        
        self.grid = Gtk.Grid()
        
        self.grid.set_row_spacing(self.GRID_ROW_SPACING)
        self.grid.set_column_spacing(self.GRID_COLUMN_SPACING)

        self.backButton= Gtk.Button("Back");
        self.nextButton= Gtk.Button("Next");
    
        self.backButton.connect("clicked", self._updateMarker,-self.increment)
        self.nextButton.connect("clicked", self._updateMarker,self.increment)

        self.grid.attach(self.backButton, 0,self.GRID_HEIGHT/2, 1, 1)
        self.grid.attach(self.nextButton, self.GRID_WIDTH + 2 ,self.GRID_HEIGHT/2, 1, 1)
          
        i=1
        j=0
        
        print("diplaying glyphs " + str(self.marker) + " to " + str(self.marker+self.GRID_HEIGHT*self.GRID_WIDTH))
        for glyphName in self.glyphList[self.marker:self.marker+self.GRID_HEIGHT*self.GRID_WIDTH]:
            
            box= Gtk.Box()
            #print(glyphName)
            glyphBox = renderGlyph(self.font[glyphName], self.GRID_BOX_SIZE, self.GRID_BOX_SIZE, self.h, self.b)     
            box.add(glyphBox)
            self.grid.attach(box, i, j, 1, 1)
            #print(str(i) + "," + str(j))
            i+=1
            if(i >= self.GRID_WIDTH+1):                
                i=1
                j+=1

        self.align.add(self.grid)
        self.show_all()

    def _updateMarker(self, handle, increment):
        
        #a very stupid way to do this
        #TODO: have to look for something better
        self.grid.destroy()
        
        self.marker+=increment
        
        if self.marker < 0:
            self.marker = 0
        elif self.marker >= len(self.glyphList) - self.GRID_WIDTH*self.GRID_HEIGHT :
            self.marker = len(self.glyphList) - self.GRID_WIDTH*self.GRID_HEIGHT -1

        self.init_ui_button()
        
    def init_ui_button(self):

        self.grid = Gtk.Grid()
        
        self.grid.set_row_spacing(self.GRID_ROW_SPACING)
        self.grid.set_column_spacing(self.GRID_COLUMN_SPACING)

        self.backButton= Gtk.Button("Back");
        self.nextButton= Gtk.Button("Next");
    
        self.backButton.connect("clicked", self._updateMarker,-self.increment)
        self.nextButton.connect("clicked", self._updateMarker,self.increment)

        self.grid.attach(self.backButton, 0,self.GRID_HEIGHT/2, 1, 1)
        self.grid.attach(self.nextButton, self.GRID_WIDTH + 2 ,self.GRID_HEIGHT/2, 1, 1)
          
        i=1
        j=0
        
        print("diplaying glyphs " + str(self.marker) + " to " + str(self.marker+self.GRID_HEIGHT*self.GRID_WIDTH))
        for glyphName in self.glyphList[self.marker:self.marker+self.GRID_HEIGHT*self.GRID_WIDTH]:
            
            box= Gtk.Box()
            #print(glyphName)
            glyphBox = renderGlyph(self.font[glyphName], self.GRID_BOX_SIZE, self.GRID_BOX_SIZE, self.h, self.b)     
            box.add(glyphBox)
            self.grid.attach(box, i, j, 1, 1)
            #print(str(i) + "," + str(j))
            i+=1
            if(i >= self.GRID_WIDTH+1):                
                i=1
                j+=1

        self.align.add(self.grid)
        self.show_all()
     
     
