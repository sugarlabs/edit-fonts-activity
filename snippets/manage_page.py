import os
import shutil
import logging
from gettext import gettext as _

import gi
gi.require_version('Gtk', '3.0')

#from gi.repository import GConf
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import Pango

#from sugar3 import env
#from sugar3.graphics import style
#from sugar3.graphics.icon import CellRendererIcon
#from sugar3.graphics.xocolor import XoColor

#from sugar3.activity import activity
#from sugar3.graphics.toolbarbox import ToolbarBox
#from sugar3.activity.widgets import ActivityToolbarButton
#from sugar3.activity.widgets import StopButton
#from sugar3.graphics.icon import Icon

gi.require_version('WebKit', '3.0')

from gi.repository import WebKit, GLib, GdkPixbuf

svg_inactive = """
<svg viewBox="0 0 60 55" width="50" height="25">
    <g display="block">
        <polygon display="inline" style="fill:rgb(255,255,255);stroke-width:3.5;stroke:rgb(0,0,0)" points="27.5,7.266 34.074,20.588 48.774,22.723    38.138,33.092 40.647,47.734 27.5,40.82 14.353,47.734 16.862,33.092 6.226,22.723 20.926,20.588" />
    </g>
</svg>

"""

svg_active = """
<svg viewBox="0 0 60 55" width="50" height="25">
    <g display="block">
        <polygon display="inline" style="fill:rgb(229,0,0);stroke-width:3.5;stroke:rgb(0,0,0)" points="27.5,7.266 34.074,20.588 48.774,22.723    38.138,33.092 40.647,47.734 27.5,40.82 14.353,47.734 16.862,33.092 6.226,22.723 20.926,20.588" />
    </g>
</svg>

"""

QUERY = ''

#favorite fonts config file
fav_fonts_file_path = 'fonts.config'
fav_fonts = []

#active fonts folder
fonts_file_path = '~/.fonts'
_all_active_fonts = []

#inactive fonts folder
inactive_fonts_file_path = '~/.fonts-inactive'

#FIX ME:Only font name will be shown for the Inactive fonts as I can't upload any ttf file using Pango
#this can be done in two of the following ways 
#temporarily install the font and draw using Pango
#convert to ufo format
inactive_fonts_path = []

STAR_ICON_NAME = ''
STAR_INACTIVE_ICON_NAME = '1'

class ManagerPage(Gtk.Box):
    """This Class Creates the "Font Manager" Page
    
    """

    def __init__(self, activity):
        
        super(ManagerPage, self).__init__()    
        self.activity = activity

        self._init_ui()

    def update(self, activity):
        #FIX ME: this shouldn't destroy anything
        #just update all the information in the modal 

        self.activity = activity
        
    def _init_ui(self):
        
        self.init_fonts()
        self.font_list = FontsList()
        self.pack_start(self.font_list, True, True, 0)
        self.show_all()

    def init_fonts(self):

        #Active Fonts

        #check if the ~/.fonts directory exists
        if not os.path.isdir(fonts_file_path):
            os.makedirs(fonts_file_path)

        #get all installed fonts
        global _all_active_fonts
        
        context = self.get_pango_context()
        #context = self.activity.get_pango_context()

        for family in context.list_families():
            name = family.get_name()
            _all_active_fonts.append(name)

        #Inactive Fonts

        #check if the ~/.fonts-inactive exists
        if not os.path.isdir(inactive_fonts_file_path):
            os.makedirs(inactive_fonts_file_path)

        #get all files in the folder
        #store all the filenames in self.inactive_FONTS
        (_, _, self.inactive_fonts_path) = os.walk(inactive_fonts_file_path).next()        

        #Favorite Fonts

        #open or write the favorite fonts file
        if not os.path.exists(fav_fonts_file_path):
            print "No font-config file found"
            print "Creating one"
            file = open(fav_fonts_file_path, 'w')
            file.close()            

        if os.path.exists(fav_fonts_file_path):
            print "font-config file found"
            print "Opening it"
            
            # get the font names in the file to the white list
            file = open(fav_fonts_file_path, 'r')
            # get the font names in the file to the white list
            t = file.read()
            fav_fonts = t.split(';')
            file.close()
            
        #FIX ME: Automatic change monitoring not working


class FontsTreeView(Gtk.TreeView):

    __gtype_name__ = 'SugarActivitiesTreeView'

    def __init__(self):
        Gtk.TreeView.__init__(self)

        self._query = ''
        #client = GConf.Client.get_default()
        #self.xo_color = XoColor(client.get_string('/desktop/sugar/user/color'))

        self.set_headers_visible(False)
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK |
                        Gdk.EventMask.TOUCH_MASK |
                        Gdk.EventMask.BUTTON_RELEASE_MASK)
        selection = self.get_selection()
        selection.set_mode(Gtk.SelectionMode.NONE)

        self.model = ListModel()
        #self.model.set_visible_func(self.__model_visible_cb)
        self.set_model(self.model)

        #FIX ME: This widget is not receiving the click event
        cell_favorite = CellRendererClickablePixbuf()
        
        loader = GdkPixbuf.PixbufLoader()
        loader.write(svg_active.encode())
        loader.close()  
        cell_favorite.props.pixbuf = loader.get_pixbuf()

        print cell_favorite.props.pixbuf
        cell_favorite.props.mode = Gtk.CellRendererMode.ACTIVATABLE        

        #cell_favorite.props.mode = Gtk.CellRendererMode.ACTIVATABLE
        cell_favorite.connect('clicked', self.__favorite_clicked_cb)
        #print help(cell_favorite.activate)        
        #print help(cell_favorite.props.mode)        
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
        self.set_enable_search(True)

        #FIX ME: This will only work in Gtk+ 3.8 and later.
        #self.props.activate_on_single_click = True
        #self.connect('row-activated', self.__row_activated_cb)

    def __row_activated_cb(self, treeview, path, col):
        
        if col is treeview.get_column(0):
            iter_ = self.model.get_iter(path)
            is_fav = self.model.get_value(iter_, 0)
            self.model.set_value(row, 0, model[row][0]^1)
            print "Star clicked"

        else:
            print "Row clicked"

    def __favorite_set_data_cb(self, column, cell, model, tree_iter, data):
        font_name = model[tree_iter][ListModel.COLUMN_FONT_NAME]
        favorite = font_name in fav_fonts
        if favorite:
            loader = GdkPixbuf.PixbufLoader()
            loader.write(svg_active.encode())
            loader.close()  
            cell.props.pixbuf = loader.get_pixbuf()
        else:
            loader = GdkPixbuf.PixbufLoader()
            loader.write(svg_inactive.encode())
            loader.close()  
            cell.props.pixbuf = loader.get_pixbuf()

    def __favorite_clicked_cb(self, cell, path):
        """
        What happens when the user clicks on any of the stars 
        
        """
        print "star was clicked"
        
        model = self.get_model()
        iter_ = model.get_iter(path)
        is_fav = model.get_value(iter_, ListModel.COLUMN_FAVORITE)

        print is_fav        
        row = model[path]
        font_name = row[ListModel.COLUMN_FONT_NAME]
        
        #change the value in the model 
        is_fav ^=True
        print is_fav
        model.set_value(iter_, ListModel.COLUMN_FAVORITE, is_fav)
        #self.set_model(model)
        
        print model.get_value(iter_, ListModel.COLUMN_FAVORITE)
        
        #change the color of the icon
        #and update the fav_fonts list
        
        if is_fav:
            #cell.props.xo_color = self.xo_color
            fav_fonts.append(font_name)
        else:
            #cell.props.xo_color = None
            fav_fonts.remove(font_name)

        #Update the fav fonts config file
        #row = model[path]
        #font_name = row[ListModel.COLUMN_FONT_NAME]
        logging.debug(font_name + " clicked")
        
        fonts_file = open(fav_fonts_file_path, 'w')
        for font_name in fav_fonts:
            fonts_file.write('%s;' % font_name)
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

    COLUMN_FAVORITE = 0
    COLUMN_FONT_NAME = 1
    COLUMN_TEST = 2
    COLUMN_SCALE = 3
    COLUMN_SCALE_SET = 4

    def __init__(self):
        super(ListModel, self).__init__(bool, str, str, int, bool)
        self.set_sort_column_id(ListModel.COLUMN_FONT_NAME,
                                Gtk.SortType.ASCENDING)

        # load the model
        global _all_active_fonts
        global fav_fonts
        
        for font_name in _all_active_fonts:
            favorite = font_name in fav_fonts
            data = [favorite, font_name,
                _('The quick brown fox jumps over the lazy dog.'), 1, True]
            print data
            self.append(data)


"""
class ListModel(Gtk.TreeModelSort):
    __gtype_name__ = 'SugarListModel'

    COLUMN_FAVORITE = 0
    COLUMN_FONT_NAME = 1
    COLUMN_TEST = 2
    COLUMN_SCALE = 3
    COLUMN_SCALE_SET = 4

    def __init__(self):
        self._model = Gtk.ListStore(bool, str, str, int, bool)
        self._model_filter = self._model.filter_new()
        Gtk.TreeModelSort.__init__(self, model=self._model_filter)
        self.set_sort_column_id(ListModel.COLUMN_FONT_NAME,
                                Gtk.SortType.ASCENDING)

        # load the model
        global _all_active_fonts
        global fav_fonts
        
        for font_name in _all_active_fonts:
            favorite = font_name in fav_fonts
            self._model.append([
                favorite, font_name,
                _('The quick brown fox jumps over the lazy dog.'), 2, True])

    def set_visible_func(self, func):
        self._model_filter.set_visible_func(func)

    def refilter(self):
        self._model_filter.refilter()

    def chage_favorite(self, font_name):
        
        global fav_fonts

        if font_name in fav_fonts:
            fav_fonts.remove(font_name)
        else:
            fav_fonts.append(font_name)

        fonts_file = open(fav_fonts_file_path, 'w')
        for font_name in fav_fonts:
            fonts_file.write('%s\n' % font_name)
        fonts_file.close()

    def set_value(self, _iter, col, val):
        self._model.set_value( _iter, col, val)
"""

"""
class CellRendererFavorite(CellRendererIcon):
    __gtype_name__ = 'SugarCellRendererFavorite'

    def __init__(self):
        CellRendererIcon.__init__(self)

        self.props.width = style.GRID_CELL_SIZE
        self.props.height = style.GRID_CELL_SIZE
        self.props.size = style.SMALL_ICON_SIZE
        self.props.icon_name = "emblem-favorite"
        self.props.mode = Gtk.CellRendererMode.ACTIVATABLE
"""

class CellRendererClickablePixbuf(Gtk.CellRendererPixbuf):
    
    __gsignals__ = {
                    'clicked': (GObject.SignalFlags.RUN_FIRST, None,
                                ([str]))
                    }

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

        self._scrolled_window = Gtk.ScrolledWindow()
        self._scrolled_window.set_policy(Gtk.PolicyType.NEVER,
                                         Gtk.PolicyType.AUTOMATIC)
        self._scrolled_window.set_shadow_type(Gtk.ShadowType.NONE)
        self._scrolled_window.connect('key-press-event',
                                      self.__key_press_event_cb)
        self.pack_start(self._scrolled_window, True, True, 0)
        self._scrolled_window.show()

        self._tree_view = FontsTreeView()
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
