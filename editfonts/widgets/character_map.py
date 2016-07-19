import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
# from gi.repository import Pango

from editfonts.widgets.render_glyph import RenderGlyph

from sugar3.graphics.icon import Icon
from sugar3.graphics import style
from editfonts.globals import globals


class CharacterMap(Gtk.Box):

    def __init__(self, w=10, h=80, ui_type='BUTTON'):

        super(CharacterMap, self).__init__()

        # Grid Parameters
        # default values
        self.GRID_WIDTH = w  # number of columns
        self.GRID_HEIGHT = h  # number of rows
        self.GRID_BOX_SIZE = 60
        self.GRID_ROW_SPACING = 5
        self.GRID_COLUMN_SPACING = self.GRID_ROW_SPACING

        self.h = globals.FONT.info.ascender - globals.FONT.info.descender
        self.b = -globals.FONT.info.descender

        self.glyphList = globals.FONT.keys()
        self.marker = 0
        self.gridSize = self.GRID_HEIGHT * self.GRID_WIDTH

        # The alignment keeps the grid center aligned
        self.align = Gtk.Alignment(xalign=0.5, yalign=0.5, xscale=0, yscale=0)

        if ui_type == 'BUTTON':
            self.init_ui_button()

        elif ui_type == 'SCROLL':
            self.init_ui_scrollable()

        else:
            print("WARNING: Invalid ui_type for characterMap: " + ui_type)
            print("Choosing Button type instead")
            self.init_ui_button()

    def init_ui_button(self):

        self.grid = Gtk.Grid()
        self.align.add(self.grid)

        self.grid.set_row_spacing(self.GRID_ROW_SPACING)
        self.grid.set_column_spacing(self.GRID_COLUMN_SPACING)

        # creating a back button
        self.backButton = Gtk.EventBox()
        backIcon = Icon(pixel_size=self.GRID_BOX_SIZE)
        backIcon.props.icon_name = 'go-previous'
        self.backButton.add(backIcon)
        self.backButton.connect("button-press-event", self._update_marker, -1)

        # creating a next button
        self.nextButton = Gtk.EventBox()
        nextIcon = Icon(pixel_size=self.GRID_BOX_SIZE)
        nextIcon.props.icon_name = 'go-next'
        self.nextButton.add(nextIcon)
        self.nextButton.connect("button-press-event", self._update_marker, 1)

        # adding the buttons to the character map
        self.set_border_width(10)
        self.pack_start(self.backButton, True, False, 0)
        self.pack_start(self.align, False, False, 0)
        self.pack_end(self.nextButton, True, False, 0)

        # making a separate function for filling the grid so that this can be
        # used to update without destroying and rebuilding the entire grid
        # every time the user clicks on the side arrows
        self._fill_grid()

    def init_ui_scrollable(self):

        self.grid = Gtk.Grid()
        self.align.add(self.grid)

        self.grid.set_row_spacing(self.GRID_ROW_SPACING)
        self.grid.set_column_spacing(self.GRID_COLUMN_SPACING)

        i, j = 0, 0

        for glyphName in self.glyphList:

            self._draw_box(glyphName, i, j)

            i += 1

            if i > self.GRID_WIDTH:
                i = 0
                j += 1

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER,
                                   Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_border_width(10)
        scrolled_window.add_with_viewport(self.align)
        self.pack_start(scrolled_window, True, True, 0)

        self.show_all()

    def _fill_grid(self):

        for i in range(self.GRID_WIDTH):
            for j in range(self.GRID_HEIGHT):

                try:
                    glyphName = self.glyphList[self.marker + j *
                                               self.GRID_WIDTH + i]
                except IndexError:
                    glyphName = None

                child = self.grid.get_child_at(i, j)
                if child is not None:
                    self.grid.remove(child)

                if glyphName is not None:
                    self._draw_box(glyphName, i, j)

                """
                else:

                    # check whether there already is a child at this position
                    child = self.grid.get_child_at(i, j)
                    if child is not NULL:
                        grid.remove(child)

                """
        self.show_all()

    def _draw_box(self, glyphName, i, j):

        eventBox = Gtk.EventBox()
        self.grid.attach(eventBox, i, j, 1, 1)
        eventBox.connect("button-press-event", self._glyph_clicked, glyphName)
        eventBox.modify_bg(Gtk.StateType.NORMAL,
                           style.Color(globals.GLYPH_BOX_COLOR)
                           .get_gdk_color())

        box = Gtk.VBox()
        eventBox.add(box)

        unicodeLable = Gtk.Label(glyphName)
        unicodeLable.set_size_request(self.GRID_BOX_SIZE / 2,
                                      self.GRID_BOX_SIZE / 3)

        # FIX ME: find a way to set the ellisize mode on this lable to be true
        # unicodeLable.set_max_width_chars(6)
        # unicodeLable.set_property('ellipsize', Pango.PANGO_ELLIPSIZE_END)

        box.pack_start(unicodeLable, False, False, 2)

        alignment = Gtk.Alignment(xalign=0.5, yalign=0.5, xscale=0, yscale=0)
        box.pack_start(alignment, True, False, 0)

        glyphBox = RenderGlyph(glyphName, self.GRID_BOX_SIZE,
                               self.GRID_BOX_SIZE, self.h, self.b)
        eventBox.connect("button-press-event", self._glyph_clicked, glyphName)

        alignment.add(glyphBox)

    def _glyph_clicked(self, handle, event, glyphName):

        globals.GLYPH_NAME = glyphName
        globals.GLYPH = globals.FONT[globals.GLYPH_NAME]
        globals.A.set_page("EDITOR")

    def _update_marker(self, handle, event, increment):

        self.marker += increment * self.gridSize

        if self.marker < 0:
            self.marker = 0
        elif self.marker > len(self.glyphList) - \
                len(self.glyphList) % self.gridSize:
            self.marker = len(self.glyphList) - \
                len(self.glyphList) % self.gridSize

        self._fill_grid()
