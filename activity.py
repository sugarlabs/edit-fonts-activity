# Copyright (C) 2013 One Laptop per Child
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
import shutil
import logging
from gettext import gettext as _

from gi.repository import GConf
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import Pango

from sugar3 import env
from sugar3.graphics import style
from sugar3.graphics.icon import CellRendererIcon
from sugar3.graphics.xocolor import XoColor

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.activity.widgets import StopButton


DEFAULT_FONTS = ['Sans', 'Serif', 'Monospace']
USER_FONTS_FILE_PATH = env.get_profile_path('fonts')
GLOBAL_FONTS_FILE_PATH = '/etc/sugar_fonts'


class FontsActivity(activity.Activity):

    def __init__(self, handle):
        """Set up the HelloWorld activity."""
        activity.Activity.__init__(self, handle)

        self.max_participants = 1

        toolbar_box = ToolbarBox()

        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        self.init_fonts()

        self.font_list = FontsList(self._all_fonts, self._font_white_list)
        self.set_canvas(self.font_list)
        self.show_all()

    def init_fonts(self):

        # load the data in the model
        self._all_fonts = []
        context = self.get_pango_context()
        for family in context.list_families():
            name = family.get_name()
            self._all_fonts.append(name)

        # copied from fontcombobox

        self._font_white_list = []
        self._font_white_list.extend(DEFAULT_FONTS)

        # check if there are a user configuration file
        if not os.path.exists(USER_FONTS_FILE_PATH):
            # verify if exists a file in /etc
            if os.path.exists(GLOBAL_FONTS_FILE_PATH):
                shutil.copy(GLOBAL_FONTS_FILE_PATH, USER_FONTS_FILE_PATH)

        if os.path.exists(USER_FONTS_FILE_PATH):
            # get the font names in the file to the white list
            fonts_file = open(USER_FONTS_FILE_PATH)
            # get the font names in the file to the white list
            for line in fonts_file:
                self._font_white_list.append(line.strip())
            # monitor changes in the file
            gio_fonts_file = Gio.File.new_for_path(USER_FONTS_FILE_PATH)
            self.monitor = gio_fonts_file.monitor_file(
                Gio.FileMonitorFlags.NONE, None)
            self.monitor.connect('changed', self._reload_fonts)

    def _reload_fonts(self, monitor, gio_file, other_file, event):
        if event != Gio.FileMonitorEvent.CHANGES_DONE_HINT:
            return
        font_white_list = []
        font_white_list.extend(DEFAULT_FONTS)
        fonts_file = open(USER_FONTS_FILE_PATH)
        for line in fonts_file:
            font_name = line.strip()
            if font_name not in font_white_list:
                font_white_list.append(font_name)
        logging.error('font list file updated %s', font_white_list)


class FontsTreeView(Gtk.TreeView):

    __gtype_name__ = 'SugarActivitiesTreeView'

    def __init__(self, all_fonts, favorites):
        Gtk.TreeView.__init__(self)

        self._query = ''
        client = GConf.Client.get_default()
        self.xo_color = XoColor(client.get_string('/desktop/sugar/user/color'))

        self.set_headers_visible(False)
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK |
                        Gdk.EventMask.TOUCH_MASK |
                        Gdk.EventMask.BUTTON_RELEASE_MASK)
        selection = self.get_selection()
        selection.set_mode(Gtk.SelectionMode.NONE)

        model = ListModel(all_fonts, favorites)
        model.set_visible_func(self.__model_visible_cb)
        self.set_model(model)

        cell_favorite = CellRendererFavorite(self)
        cell_favorite.connect('clicked', self.__favorite_clicked_cb)
        column = Gtk.TreeViewColumn()
        column.pack_start(cell_favorite, True)
        column.set_cell_data_func(cell_favorite, self.__favorite_set_data_cb)
        self.append_column(column)

        cell_text = Gtk.CellRendererText()
        cell_text.props.ellipsize_set = False
        column = Gtk.TreeViewColumn()
        column.props.sizing = Gtk.TreeViewColumnSizing.GROW_ONLY
        column.props.expand = False
        column.set_sort_column_id(ListModel.COLUMN_FONT_NAME)
        column.pack_start(cell_text, True)
        column.add_attribute(cell_text, 'text', ListModel.COLUMN_FONT_NAME)
        column.add_attribute(cell_text, 'font', ListModel.COLUMN_FONT_NAME)
        column.add_attribute(cell_text, 'scale', ListModel.COLUMN_SCALE)
        column.add_attribute(cell_text, 'scale-set',
                             ListModel.COLUMN_SCALE_SET)
        self.append_column(column)

        cell_text = Gtk.CellRendererText()
        cell_text.props.ellipsize = Pango.EllipsizeMode.MIDDLE
        cell_text.props.ellipsize_set = True
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

        self.set_search_column(ListModel.COLUMN_FONT_NAME)
        self.set_enable_search(False)

    def __favorite_set_data_cb(self, column, cell, model, tree_iter, data):
        font_name = model[tree_iter][ListModel.COLUMN_FONT_NAME]
        favorite = font_name in model._favorites
        if favorite:
            cell.props.xo_color = self.xo_color
        else:
            cell.props.xo_color = None

    def __favorite_clicked_cb(self, cell, path):
        model = self.get_model()
        row = model[path]
        font_name = row[ListModel.COLUMN_FONT_NAME]
        model.chage_favorite(font_name)

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


class ListModel(Gtk.TreeModelSort):
    __gtype_name__ = 'SugarListModel'

    COLUMN_FAVORITE = 0
    COLUMN_FONT_NAME = 1
    COLUMN_TEST = 2
    COLUMN_SCALE = 3
    COLUMN_SCALE_SET = 4

    def __init__(self, all_fonts, favorites):
        self._model = Gtk.ListStore(bool, str, str, int, bool)
        self._model_filter = self._model.filter_new()
        Gtk.TreeModelSort.__init__(self, model=self._model_filter)
        self.set_sort_column_id(ListModel.COLUMN_FONT_NAME,
                                Gtk.SortType.ASCENDING)

        # load the model
        self._all_fonts = all_fonts
        self._favorites = favorites
        for font_name in self._all_fonts:
            favorite = font_name in self._favorites
            self._model.append([
                favorite, font_name,
                _('The quick brown fox jumps over the lazy dog.'), 2, True])

    def set_visible_func(self, func):
        self._model_filter.set_visible_func(func)

    def refilter(self):
        self._model_filter.refilter()

    def chage_favorite(self, font_name):
        if font_name in self._favorites:
            self._favorites.remove(font_name)
        else:
            self._favorites.append(font_name)

        fonts_file = open(USER_FONTS_FILE_PATH, 'w')
        for font_name in self._favorites:
            fonts_file.write('%s\n' % font_name)
        fonts_file.close()


class CellRendererFavorite(CellRendererIcon):
    __gtype_name__ = 'SugarCellRendererFavorite'

    def __init__(self, tree_view):
        CellRendererIcon.__init__(self, tree_view)

        self.props.width = style.GRID_CELL_SIZE
        self.props.height = style.GRID_CELL_SIZE
        self.props.size = style.SMALL_ICON_SIZE
        self.props.icon_name = 'emblem-favorite'
        self.props.mode = Gtk.CellRendererMode.ACTIVATABLE
        prelit_color = tree_view.xo_color
        self.props.prelit_stroke_color = prelit_color.get_stroke_color()
        self.props.prelit_fill_color = prelit_color.get_fill_color()


class FontsList(Gtk.VBox):
    __gtype_name__ = 'SugarActivitiesList'

    def __init__(self, all_fonts, favorites):
        logging.debug('STARTUP: Loading the activities list')

        Gtk.VBox.__init__(self)

        self._scrolled_window = Gtk.ScrolledWindow()
        self._scrolled_window.set_policy(Gtk.PolicyType.NEVER,
                                         Gtk.PolicyType.AUTOMATIC)
        self._scrolled_window.set_shadow_type(Gtk.ShadowType.NONE)
        self._scrolled_window.connect('key-press-event',
                                      self.__key_press_event_cb)
        self.pack_start(self._scrolled_window, True, True, 0)
        self._scrolled_window.show()

        self._tree_view = FontsTreeView(all_fonts, favorites)
        self._scrolled_window.add(self._tree_view)
        self._tree_view.show()

    def grab_focus(self):
        # overwrite grab focus in order to grab focus from the parent
        self._tree_view.grab_focus()

    def set_filter(self, query):
        matches = self._tree_view.set_filter(query)
        if matches == 0:
            self._show_clear_message()
        else:
            self._hide_clear_message()

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
