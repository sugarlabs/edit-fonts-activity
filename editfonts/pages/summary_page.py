from gi.repository import Gtk
# from gi.repository import Gdk
# import cairo
# import math
# from defcon import Font

# import pager

# from sugar3.graphics.icon import Icon
from sugar3.graphics import style

from editfonts.widgets.misc import ImageButton
from editfonts.widgets.misc import FormatLabel
from editfonts.widgets.character_map import CharacterMap
import editfonts.globals as globals


class SummaryPage(Gtk.Box):
    """This Class Creates the "Font:<familyName>" Page that loads up on
        clicking any Font
    """

    def __init__(self):
        super(SummaryPage, self).__init__()
        self._init_ui()

    def update(self, activity):
        self.activity = activity
        self.font = activity.main_font
        self.glyphName = activity.glyphName

    def _init_ui(self):

        self.set_property("orientation", Gtk.Orientation.HORIZONTAL)

        self.side_toolbar = self._create_toolbar()
        # self.side_toolbar.set_property("border-width", 40)

        self.pack_end(self.side_toolbar, False, False, 10)

        self.vbox = Gtk.VBox()
        self.pack_start(self.vbox, True, True, 10)

        """
        self.heading = FormatLabel("Font: " + globals.FONT.info.familyName,
                                   globals.TEXT_STYLE['HEADING'])

        self.infoBoxExpander = Gtk.Expander()
        expanderLabelText = "See Details"
        self.infoBoxExpander.set_property("use-markup", True)
        self.infoBoxExpander.set_label("something")

        self.infoBox = FontInfoBox(globals.FONT)

        self.infoBoxExpander.add(self.infoBox)

        self.vbox.pack_start(self.heading, False, False, 30)

        self.vbox.pack_start(Gtk.HSeparator(),
                             False, False, 0)

        self.vbox.pack_start(self.infoBoxExpander, False, False, 30)

        self.vbox.pack_start(Gtk.HSeparator(),
                             False, False, 0)
        """
        # FIXME: Number of Columns displayed are
        # 1 more than the arguement given
        self.characterMap = CharacterMap(9, 5, 'SCROLL')

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
        grid = Gtk.Grid()
        grid.set_border_color(style.Color('# 34495E').get_gdk_color())

        # GRID_HEIGHT = 3  # number of rows
        # GRID_WIDTH = 1  # number of columns
        # GRID_BOX_SIZE = 40
        GRID_ROW_SPACING = 10
        GRID_COLUMN_SPACING = 5

        frame.set_border_width(5)
        frame.add(grid)
        grid.set_column_spacing(GRID_COLUMN_SPACING)
        grid.set_row_spacing(GRID_ROW_SPACING)

        # Install Button
        vbox = Gtk.VBox()
        button = ImageButton('install',
                             pixel_size=globals.BUTTON_BOX_SIZE * 0.6)
        button.set_tooltip_text('Activate a Font')
        # button.connect("clicked", lambda _: pass)

        vbox.pack_start(button, False, False, 0)

        label = FormatLabel('Activate', globals.TEXT_STYLE['LABEL'])
        alignment_box = Gtk.Alignment(xalign=0.5,
                                      yalign=0.5,
                                      xscale=0,
                                      yscale=0)
        alignment_box.add(label)
        vbox.pack_start(alignment_box, True, True, 0)

        grid.attach(vbox, 0, 0, 1, 1)

        # Add Glyph
        vbox = Gtk.VBox()
        button = ImageButton('install',
                             pixel_size=globals.BUTTON_BOX_SIZE * 0.6)
        button.set_tooltip_text('Add a Glyph')
        # button.connect("clicked", lambda _: pass)

        vbox.pack_start(button, False, False, 0)

        label = FormatLabel('Add a Glyph', globals.TEXT_STYLE['LABEL'])
        alignment_box = Gtk.Alignment(xalign=0.5,
                                      yalign=0.5,
                                      xscale=0,
                                      yscale=0)
        alignment_box.add(label)
        vbox.pack_start(alignment_box, True, True, 0)

        grid.attach(vbox, 0, 1, 1, 1)

        """
        # Only displayed when any of the glyph is selected
        # Delete Glyph
        vbox = Gtk.VBox()
        button = ImageButton('install',
                             pixel_size=globals.BUTTON_BOX_SIZE * 0.6)
        button.set_tooltip_text('Activate a Font')
        button.connect("clicked", lambda _: self._clickInstall)

        vbox.pack_start(button, False, False, 0)

        label = FormatLabel('Activate', globals.TEXT_STYLE['LABEL'])
        alignment_box = Gtk.Alignment(xalign=0.5,
                                      yalign=0.5,
                                      xscale=0,
                                      yscale=0)
        alignment_box.add(label)
        vbox.pack_start(alignment_box, True, True, 0)

        grid.attach(vbox, 0, 0, 1, 1)


        # Add Glyph
        vbox = Gtk.VBox()
        button = ImageButton('install',
                             pixel_size=globals.BUTTON_BOX_SIZE * 0.6)
        button.set_tooltip_text('Activate a Font')
        button.connect("clicked", lambda _: self._clickInstall)

        vbox.pack_start(button, False, False, 0)

        label = FormatLabel('Activate', globals.TEXT_STYLE['LABEL'])
        alignment_box = Gtk.Alignment(xalign=0.5,
                                      yalign=0.5,
                                      xscale=0,
                                      yscale=0)
        alignment_box.add(label)
        vbox.pack_start(alignment_box, True, True, 0)

        grid.attach(vbox, 0, 0, 1, 1)
        """

        """
        # Edit Button
        image_icon = Icon(pixel_size=style.MEDIUM_ICON_SIZE,
                          icon_name='edit',
                          stroke_color=style.COLOR_BLACK.get_svg(),
                          fill_color=style.COLOR_WHITE.get_svg())
        editButton = Gtk.Button()
        editButton.add(image_icon)
        editButton.props.relief = Gtk.ReliefStyle.NONE
        editButton.connect("clicked", self._clickEdit)
        grid.attach(editButton, 0, 1, 1, 1)
        """
        return frame

    def _clickDelete(self, handle):
        pass

    def _clickEdit(self, handle):
        # create a new page
        globals.A.set_page("EDITOR")

    def _clickInstall(self, handle):
        pass
