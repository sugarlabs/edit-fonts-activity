import os
# import shutil
import logging
# import subprocess
# from gettext import gettext as _

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# from gi.repository import GConf
from gi.repository import GObject

from gi.repository import Gdk
from gi.repository import GdkPixbuf
# from gi.repository import Gio
from gi.repository import Pango

# from sugar3 import env
# from sugar3.graphics import style
# from sugar3.graphics.icon import CellRendererIcon
# from sugar3.graphics.xocolor import XoColor

# from sugar3.activity import activity
# from sugar3.graphics.toolbarbox import ToolbarBox
# from sugar3.activity.widgets import ActivityToolbarButton
# from sugar3.activity.widgets import StopButton
# from sugar3.graphics.icon import Icon

# gi.require_version('WebKit', '3.0')
# from gi.repository import WebKit
# from gi.repository import GLib

import editfonts.widgets.localIcon as localIcon

QUERY = ''

# favorite fonts config file
fav_fonts_file_path = './fonts.config'
fav_fonts = []

# active fonts folder
active_fonts_file_path = '/home/broot/.fonts'
active_fonts_path = []

_all_system_fonts = []

# inactive fonts folder
inactive_fonts_file_path = '/home/broot/.fonts-inactive'

# FIX ME:Only font names will be shown for the Inactive fonts as I can't
# upload any ttf file using Pango
# this can be done in two of the following ways
# temporarily install the font and draw using Pango
# convert to ufo format
inactive_fonts_path = []

STAR_ICON_NAME = ''
STAR_INACTIVE_ICON_NAME = '1'


class ManagerPage(Gtk.Box):
    """This Class Creates the "Font Manager" Page

    """

    def __init__(self):
        super(ManagerPage, self).__init__()
        self._init_ui()

    def _init_ui(self):

        self.init_fonts()
        self.font_list = FontsList()
        self.pack_start(self.font_list, True, True, 0)
        self.show_all()

    def init_fonts(self):

        global _all_system_fonts
        global active_fonts_path
        global inactive_fonts_path
        global fav_fonts

        # Active Fonts

        # check if the ~/.fonts directory exists
        if not os.path.isdir(active_fonts_file_path):
            os.makedirs(active_fonts_file_path)

        (_, _, active_fonts_path) = os.walk(active_fonts_file_path).next()

        # get all files in the folder
        active_fonts_path = []
        for i, val in enumerate(active_fonts_path):
            if val.endswith('.ttf'):
                active_fonts_path.append(val.strip('.ttf'))
        context = self.get_pango_context()
        # context = self.activity.get_pango_context()

        for family in context.list_families():
            name = family.get_name()
            _all_system_fonts.append(name)

        # Inactive Fonts

        # check if the ~/.fonts-inactive exists
        if not os.path.isdir(inactive_fonts_file_path):
            os.makedirs(inactive_fonts_file_path)

        # get all files in the folder
        (_, _, inactive_fonts_path) = os.walk(inactive_fonts_file_path).next()

        # Favorite Fonts

        inactive_fonts_path = []
        for i, val in enumerate(inactive_fonts_path):
            if val.endswith('.ttf'):
                inactive_fonts_path.append(val.strip('.ttf'))

        # open or write the favorite fonts file
        if not os.path.exists(fav_fonts_file_path):
            file = open(fav_fonts_file_path, 'w')
            file.close()

        # get the font names in the file to the white list
        file = open(fav_fonts_file_path, 'r')
        # get the font names in the file to the white list
        t = file.read()
        fav_fonts = t.split('\n')
        file.close()
        print fav_fonts

        # FIX ME: Automatic change monitoring not working


class FontsTreeView(Gtk.TreeView):

    __gtype_name__ = 'SugarActivitiesTreeView'

    def __init__(self):
        super(FontsTreeView, self).__init__()

        self._query = ''
        # client = GConf.Client.get_default()
        # self.xo_color =
        # XoColor(client.get_string('/desktop/sugar/user/color'))

        self.set_headers_visible(False)
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK |
                        Gdk.EventMask.TOUCH_MASK |
                        Gdk.EventMask.BUTTON_RELEASE_MASK)

        selection = self.get_selection()
        selection.connect('changed', self.on_treeview_selection_changed)

        # if selection is not None:
        #    selection.set_mode(Gtk.SelectionMode.NONE)

        # TODO not used so commented out, can be moved?
        # model = self.get_model()

        # stars column
        cell_favorite = CellRendererClickablePixbuf()
        loader = GdkPixbuf.PixbufLoader()
        loader.write(localIcon.svg_active.encode())
        loader.close()
        cell_favorite.props.pixbuf = loader.get_pixbuf()
        cell_favorite.props.mode = Gtk.CellRendererMode.ACTIVATABLE
        cell_favorite.connect('clicked', self.__favorite_clicked_cb)
        column = Gtk.TreeViewColumn()
        column.pack_start(cell_favorite, True)
        column.set_cell_data_func(cell_favorite, self.__favorite_set_data_cb)
        self.append_column(column)

        # Font name column
        cell_text = Gtk.CellRendererText()
        cell_text.props.ellipsize_set = False
        cell_text.props.height = 60
        column = Gtk.TreeViewColumn()
        column.props.sizing = Gtk.TreeViewColumnSizing.GROW_ONLY
        column.props.expand = False
        column.set_sort_column_id(ListModel.COLUMN_FONT_NAME)
        column.pack_start(cell_text, True)
        column.add_attribute(cell_text, 'text', ListModel.COLUMN_FONT_NAME)
        # column.add_attribute(cell_text, 'font', ListModel.COLUMN_FONT_NAME)
        column.add_attribute(cell_text, 'scale',
                             ListModel.COLUMN_FONT_NAME_SCALE)
        column.add_attribute(cell_text, 'scale-set',
                             ListModel.COLUMN_SCALE_SET)
        self.append_column(column)

        # Font sample text column
        cell_text = Gtk.CellRendererText()
        cell_text.props.ellipsize = Pango.EllipsizeMode.MIDDLE
        cell_text.props.ellipsize_set = True
        cell_text.set_property("background", "white")
        column = Gtk.TreeViewColumn()
        column.set_alignment(1)
        column.props.sizing = Gtk.TreeViewColumnSizing.GROW_ONLY
        column.props.resizable = True
        column.props.reorderable = True
        column.props.expand = True
        column.set_sort_column_id(ListModel.COLUMN_TEST)
        column.pack_start(cell_text, True)
        column.add_attribute(cell_text, 'text', ListModel.COLUMN_TEST)
        column.add_attribute(cell_text, 'font', ListModel.COLUMN_FONT_NAME)
        column.add_attribute(cell_text, 'scale', ListModel.COLUMN_SCALE)
        column.add_attribute(cell_text, 'scale-set',
                             ListModel.COLUMN_SCALE_SET)
        self.append_column(column)

        # activate/deactivate button
        cell_activate_button = CellRendererClickablePixbuf()
        loader = GdkPixbuf.PixbufLoader()
        loader.write(localIcon.activate.encode())
        loader.close()
        cell_activate_button.props.pixbuf = loader.get_pixbuf()
        cell_activate_button.props.mode = Gtk.CellRendererMode.ACTIVATABLE
        cell_activate_button.connect('clicked', self.__activate_clicked_cb)
        column = Gtk.TreeViewColumn()
        column.pack_start(cell_activate_button, True)
        column.add_attribute(cell_activate_button, 'visible',
                             ListModel.COLUMN_SELECTED)
        column.set_cell_data_func(cell_activate_button,
                                  self.__activate_set_data_cb)
        self.append_column(column)

        # load font button, this will open font summary page
        cell_edit_font = CellRendererClickablePixbuf()
        loader = GdkPixbuf.PixbufLoader()
        loader.write(localIcon.edit.encode())
        loader.close()
        cell_edit_font.props.pixbuf = loader.get_pixbuf()
        cell_edit_font.connect('clicked', self.__load_font)
        column = Gtk.TreeViewColumn()
        column.pack_start(cell_edit_font, True)
        column.add_attribute(cell_edit_font, 'visible',
                             ListModel.COLUMN_SELECTED)
        self.append_column(column)

        # I dont know what this means
        # self.set_search_column(ListModel.COLUMN_FONT_NAME)
        # self.set_enable_search(True)

        # FIX ME: This will only work in Gtk+ 3.8 and later.
        # self.props.activate_on_single_click = True
        # self.connect('row-activated', self.__row_activated_cb)

    def on_treeview_selection_changed(self, selection):
        # FIX ME: only show the activate/edit buttons if the row is selected
        # the activate and edit buttons should be shown in top toolbar
        # print "Selection Changed"

        selection = self.get_selection()
        model = self.get_model()

        # disable all buttons in all rows
        _iter = model.get_iter_first()
        while _iter is not None:
            model.set_value(_iter, ListModel.COLUMN_SELECTED, False)
            _iter = model.iter_next(_iter)

        if selection is not None:
            store, _iter = selection.get_selected()
            if _iter is not None:
                # enable extra buttons in this row
                model.set_value(_iter, ListModel.COLUMN_SELECTED, True)

    def __row_activated_cb(self, treeview, path, col):
        model = self.get_model()
        row = model[path]
        if col is treeview.get_column(0):
            # TODO ** flake8 error, not used **
            # iter_ = model.get_iter(path)
            # is_fav = model.get_value(iter_, 0)
            model.set_value(row, 0, model[row][0] ^ 1)
            # print "Star clicked"

        else:
            # print "Row clicked"
            pass

    def __favorite_set_data_cb(self, column, cell, model, tree_iter, data):
        model = self.get_model()
        font_name = model[tree_iter][ListModel.COLUMN_FONT_NAME]
        favorite = font_name in fav_fonts
        if favorite:
            loader = GdkPixbuf.PixbufLoader()
            loader.write(localIcon.svg_active.encode())
            loader.close()
            cell.props.pixbuf = loader.get_pixbuf()
        else:
            loader = GdkPixbuf.PixbufLoader()
            loader.write(localIcon.svg_inactive.encode())
            loader.close()
            cell.props.pixbuf = loader.get_pixbuf()

    def __activate_set_data_cb(self, column, cell, model, tree_iter, data):

        # DOUBT: Currently I'm showing the a green icon when the font is active
        # and a red icon when its deactivated so I'm using the this cell as a
        # status indicator rather than a button with when shows a green tick
        # sign means the cell will be activated if the button is clicked -
        # is this setting correct?

        # FIX ME: add tooltips here to that the user what icons mean what

        is_activated = model[tree_iter][ListModel.COLUMN_ACTIVATE]

        if is_activated is 1:
            loader = GdkPixbuf.PixbufLoader()
            loader.write(localIcon.activate.encode())
            loader.close()
            cell.props.pixbuf = loader.get_pixbuf()

        elif is_activated is 0:
            loader = GdkPixbuf.PixbufLoader()
            loader.write(localIcon.deactivate.encode())
            loader.close()
            cell.props.pixbuf = loader.get_pixbuf()

        else:
            loader = GdkPixbuf.PixbufLoader()
            loader.write(localIcon.lock.encode())
            loader.close()
            cell.props.pixbuf = loader.get_pixbuf()

    def __load_font(self, column, cell, model, tree_iter, data):
        pass

    def __activate_clicked_cb(self, cell, path):
        """
        What happens when the user clicks on the activate/deactivate button

        """

        model = self.get_model()
        iter_ = model.get_iter(path)
        is_activated = model.get_value(iter_, ListModel.COLUMN_ACTIVATE)
        # TODO ** flake8 error, not used **
        # row = model[path]
        # font_name = row[ListModel.COLUMN_FONT_NAME]

        # change the value in the model
        if is_activated is 1:
            is_activated = 0
        elif is_activated is 0:
            is_activated = 1
        else:
            # print "This font is locked so the state cannot be changed"
            pass

        model.set_value(iter_, ListModel.COLUMN_ACTIVATE, is_activated)

        # TODO ** flake8 error, not used **
        # update the fav_fonts list
        # if is_activated:
        #    activate font here
        #    batcmd = "mv " + inactive_fonts_file_path + "/" + font_name + \
        #       ".ttf " + active_fonts_file_path + "/" + font_name + ".ttf "
        #    result = subprocess.check_output(batcmd, shell=True)
        #    batcmd = "fc-cache -f -v"
        # else:
        #    TODO ** flake8 error, not used **
        #    deactivate font here
        #    batcmd = "mv " + active_fonts_file_path + "/" + font_name + \
        #       ".ttf " + inactive_fonts_file_path + "/" + font_name + ".ttf "
        #    result = subprocess.check_output(batcmd, shell=True)
        #    batcmd = "fc-cache -f -v"

        context = self.get_pango_context()
        # context = self.activity.get_pango_context()

        for family in context.list_families():
            name = family.get_name()
            print name

    def __favorite_clicked_cb(self, cell, path):
        """
        What happens when the user clicks on any of the stars

        """

        model = self.get_model()
        iter_ = model.get_iter(path)
        is_fav = model.get_value(iter_, ListModel.COLUMN_FAVORITE)
        row = model[path]
        font_name = row[ListModel.COLUMN_FONT_NAME]

        # change the value in the model
        is_fav ^= True
        model.set_value(iter_, ListModel.COLUMN_FAVORITE, is_fav)

        # update the fav_fonts list
        if is_fav:
            fav_fonts.append(font_name)
        else:
            fav_fonts.remove(font_name)

        # Update the fav fonts config file
        fonts_file = open(fav_fonts_file_path, 'w')
        for font_name in fav_fonts:
            fonts_file.write('%s\n' % font_name)
        fonts_file.close()

    def set_filter(self, query):
        """Set a new query and refilter the model, return the number
        of matching activities.
        """
        self._query = query.decode('utf-8')
        self.get_model().refilter()
        matches = self.get_model().iter_n_children(None)
        return matches

    def __model_visible_cb(self, model, tree_iter, data):
        title = model[tree_iter][ListModel.COLUMN_FONT_NAME]
        return title is not None and title.find(self._query) > -1


class ListModel(Gtk.ListStore):
    __gtype_name__ = 'SugarListModel'

    (COLUMN_FAVORITE,
     COLUMN_FONT_NAME,
     COLUMN_TEST,
     COLUMN_SCALE,
     COLUMN_FONT_NAME_SCALE,
     COLUMN_SCALE_SET,
     COLUMN_ACTIVATE,
     COLUMN_SELECTED) = range(8)

    def __init__(self):
        super(ListModel, self).__init__(bool, str, str, float, float,
                                        bool, int, bool)
        self.set_sort_column_id(ListModel.COLUMN_FONT_NAME,
                                Gtk.SortType.ASCENDING)

        # load the model
        global _all_system_fonts
        global active_fonts_path
        global inactive_fonts_path
        global fav_fonts

        # load the system fonts
        for font_name in _all_system_fonts:
            favorite = font_name in fav_fonts
            print favorite
            data = [favorite, font_name,
                    'The quick brown fox jumps over the lazy dog',
                    1.7, 1, True, -1, False]

            self.append(data)

        # load the active fonts
        for font_name in active_fonts_path:
            font_name = font_name.strip(".ttf")
            favorite = font_name in fav_fonts
            data = [favorite, font_name,
                    'The quick brown fox jumps over the lazy dog',
                    1.7, 1, True, 1, False]
            # print data
            self.append(data)

        # load the inactive fonts
        for font_name in inactive_fonts_path:
            font_name = font_name.strip(".ttf")
            data = [False, font_name,
                    '', 1.7, 1, True, 0, False]
            # print data
            self.append(data)


class CellRendererClickablePixbuf(Gtk.CellRendererPixbuf):

    __gsignals__ = {'clicked':
                    (GObject.SignalFlags.RUN_FIRST, None, ([str]))}

    def __init__(self):
        super(CellRendererClickablePixbuf, self).__init__()

        self.props.icon_name = STAR_ICON_NAME
        self.props.mode = Gtk.CellRendererMode.ACTIVATABLE

    def do_activate(self, event, widget, path, background_area, cell_area,
                    flags):
        self.emit('clicked', path)


class FontsList(Gtk.VBox):
    __gtype_name__ = 'SugarActivitiesList'

    def __init__(self):
        logging.debug('STARTUP: Loading the activities list')

        Gtk.VBox.__init__(self)

        bar = Gtk.HBox()

        # Creating the ListStore model
        self.data_liststore = ListModel()

        self.label = Gtk.Label("Edit Me:")
        bar.pack_start(self.label, False, False, 5)

        self.entry = Gtk.Entry()
        self.entry.set_text("The quick brown fox jumps over the lazy dog")
        bar.pack_start(self.entry, False, False, 5)
        self.entry.connect("notify::text", self._update, self.entry)

        """
        self.entry = Gtk.Entry()
        self.entry.set_text("Search")
        bar.pack_start(self.entry, True, False, 5)

        self.entry.connect("notify::text", self._search, self.entry)
        """

        self.pack_start(bar, False, False, 10)

        # self.current_filter_query = None
        # Creating the filter, feeding it with the liststore model
        # self.font_name_filter = self.data_liststore.filter_new()

        # setting the filter function
        # self.font_name_filter.set_visible_func(self.font_name_filter_func)

        # creating the treeview, making it use the filter as a model,
        # and adding the columns
        # self._tree_view = FontsTreeView.new_with_model(self.font_name_filter)
        # self._tree_view = FontsTreeView(self.font_name_filter)
        self._tree_view = FontsTreeView()
        self._tree_view.set_model(self.data_liststore)

        self._scrolled_window = Gtk.ScrolledWindow()
        self._scrolled_window.set_policy(Gtk.PolicyType.NEVER,
                                         Gtk.PolicyType.AUTOMATIC)
        self._scrolled_window.set_shadow_type(Gtk.ShadowType.NONE)
        self._scrolled_window.connect('key-press-event',
                                      self.__key_press_event_cb)
        self.pack_start(self._scrolled_window, True, True, 0)
        self._scrolled_window.show()

        self._scrolled_window.add(self._tree_view)
        self._tree_view.show()

    def font_name_filter_func(self, model, iter, data):
        """Tests if the language in the row is the one in the filter"""
        """
        if self.current_filter_query is None
                or self.current_filter_query == "None":
            return True
        else:
            c = model[iter][ListModel.COLUMN_FONT_NAME]\
                                               .find(self.current_filter_query)
            if c >= 0:
                return True
            else:
                return False
        """

    def _search(self, widget, event, entry):

        """Called on any of the button clicks"""
        """
        #we set the current language filter to the button's label
        self.current_filter_query = entry.get_text()
        #we update the filter, which updates in turn the view
        self.font_name_filter.refilter()
        """

    def _update(self, widget, event, entry):

        query = entry.get_text()
        model = self._tree_view.get_model()
        iter_ = model.get_iter_first()

        while iter_ is not None:
            model.set_value(iter_, ListModel.COLUMN_TEST, query)
            iter_ = model.iter_next(iter_)

    def grab_focus(self):
        # overwrite grab focus in order to grab focus from the parent
        self._tree_view.grab_focus()

    def __key_press_event_cb(self, scrolled_window, event):
        keyname = Gdk.keyval_name(event.keyval)

        vadjustment = scrolled_window.props.vadjustment
        if keyname == 'Up':
            if vadjustment.props.value > vadjustment.props.lower:
                vadjustment.props.value -= vadjustment.props.step_increment
        elif keyname == 'Down':
            max_value = vadjustment.props.upper - vadjustment.props.page_size
            if vadjustment.props.value < max_value:
                vadjustment.props.value = min(
                    vadjustment.props.value + vadjustment.props.step_increment,
                    max_value)
        else:
            return False

        return True
