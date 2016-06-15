from gi.repository import Gtk, Gdk
import cairo
import math
from defcon import Font
from defconGTK.customBox import PageHeading, FontInfoBox
from defconGTK.characterMap import CharacterMap
from sugar3.graphics.icon import Icon
from sugar3.graphics import style

class SummaryPage(Gtk.Box):
    """
    This Class Creates the "Font:<familyName>" Page that loads up on clicking any Font
    """

    def __init__(self, activity):
        
        super(SummaryPage, self).__init__()        
        self.activity = activity
        self.font = activity.main_font
        self._init_ui()

    def _init_ui(self):
        
        self.set_property("orientation", Gtk.Orientation.HORIZONTAL)
        
        self.side_toolbar = self._create_toolbar()
        self.side_toolbar.set_property("border-width",40)

        self.pack_end(self.side_toolbar, False, False, 10)
        
        self.vbox = Gtk.VBox()
        self.pack_start(self.vbox, False, False, 10)
        
        self.heading = PageHeading("Font: " + self.font.info.familyName )

        self.infoBoxExpander = Gtk.Expander()

        expanderLabelText="See Details"
        TEMP_STRING = "<span foreground='black' size='15000' font='Cantarell' font_weight='bold'>" + expanderLabelText +"</span>"
        self.infoBoxExpander.set_property("use-markup", True)
        self.infoBoxExpander.set_label(TEMP_STRING)

        self.infoBox = FontInfoBox(self.font)
        self.infoBoxExpander.add(self.infoBox)

        self.characterMap = CharacterMap(self, 10, 5, 'SCROLL')

        self.vbox.pack_start(self.heading, False, False, 30)
        
        self.vbox.pack_start(Gtk.HSeparator(),
                        False, False, 0)
        
        self.vbox.pack_start(self.infoBoxExpander, False, False, 30)
        
        self.vbox.pack_start(Gtk.HSeparator(),
                        False, False, 0)

        self.vbox.pack_start(self.characterMap, True, True, 30)

        self.show_all()

    def _create_toolbar(self):
        """
        This is a vertical toolbar for this page
        Elements are
        --Install Button
        --Edit Button
        --Delete Button
        """
        frame = Gtk.Frame()

        grid =Gtk.Grid()
        GRID_HEIGHT= 3  #number of rows
        GRID_WIDTH = 1  #number of columns  
        GRID_BOX_SIZE = 40
        GRID_ROW_SPACING = 20
        GRID_COLUMN_SPACING = 5

        frame.set_border_width(5)
        frame.add(grid)
        grid.set_column_spacing(GRID_COLUMN_SPACING)
        grid.set_row_spacing(GRID_ROW_SPACING)
        
        #Install Button
        image_icon = Icon(pixel_size=style.LARGE_ICON_SIZE,
                              icon_name='install',
                              stroke_color=style.COLOR_BUTTON_GREY.get_svg(),
                              fill_color=style.COLOR_TRANSPARENT.get_svg())
        installButton = Gtk.Button()
        installButton.add(image_icon)
        installButton.connect("clicked",self._clickInstall)
        grid.attach(installButton, 0, 0, 1, 1)

        #Edit Button
        image_icon = Icon(pixel_size=style.LARGE_ICON_SIZE,
                              icon_name='edit',
                              stroke_color=style.COLOR_BUTTON_GREY.get_svg(),
                              fill_color=style.COLOR_TRANSPARENT.get_svg())
        editButton = Gtk.Button()
        editButton.add(image_icon)
        editButton.connect("clicked",self._clickEdit)
        grid.attach(editButton, 0, 1, 1, 1)

        #Delete Button
        image_icon = Icon(pixel_size=style.LARGE_ICON_SIZE,
                              icon_name='delete',
                              stroke_color=style.COLOR_BUTTON_GREY.get_svg(),
                              fill_color=style.COLOR_TRANSPARENT.get_svg())

        deleteButton = Gtk.Button()
        deleteButton.add(image_icon)
        deleteButton.connect("clicked",self._clickDelete)
        grid.attach(deleteButton, 0, 2, 1, 1)
                
        return frame

    def _clickDelete(self, handle):
        pass
    def _clickEdit(self, handle):
        #create a new page
        self.activity.set_page("EDITOR")

    def _clickInstall(self, handle):
        pass

