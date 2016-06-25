#!/usr/bin/env python
# -*- Mode: Python; py-indent-offset: 4 -*-
# vim: tabstop=4 shiftwidth=4 expandtab
#
# Copyright (C) 2010 Red Hat, Inc., John (J5) Palmieri <johnp@redhat.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

title = "List Store"
description = """
The GtkListStore is used to store data in list form, to be used later on by a
GtkTreeView to display it. This demo builds a simple GtkListStore and displays
it. See the Stock Browser demo for a more advanced example.
"""


from gi.repository import Gtk, GObject, GLib


class FontEntry:
    def __init__(self, is_fav, name, query, is_activated):
        self.is_fav = is_fav
        self.name = name
        self.query = query
        self.is_activated = is_activated

    def get_arr(self):
        return [self.is_fav, self.name, self.query, self.is_activated]

query = ''
# initial data we use to fill in the store
data = [FontEntry(False, "Normal", query, True),
        FontEntry(False, "Critical", query, True),
        FontEntry(False, "Major", query, True),
        FontEntry(True,  "Major",  query, True),
        FontEntry(False, "Normal",  query, True),
        FontEntry(True, "Normal",  query, True),
        FontEntry(False, "Normal",  query, True)]


class ListStoreApp:
    (COLUMN_FAV,
     COLUMN_NAME,
     COLUMN_TEXT,
     COLUMN_ACTIVE) = range(4)

    def __init__(self):
        self.window = Gtk.Window()
        self.window.set_title('Font List Demo')
        self.window.connect('destroy', Gtk.main_quit)

        vbox = Gtk.VBox(spacing=8)
        self.window.add(vbox)

        label = Gtk.Label(label='Welcome!')
        vbox.pack_start(label, False, False, 0)

        self.entry = Gtk.Entry()
        self.entry.set_text("Hello World")
        vbox.pack_start(self.entry, True, True, 0)

        self.entry.connect("notify::text", self._search, self.entry)

        sw = Gtk.ScrolledWindow()
        sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        sw.set_policy(Gtk.PolicyType.NEVER,
                      Gtk.PolicyType.AUTOMATIC)
        vbox.pack_start(sw, True, True, 0)

        self.create_model()
        treeview = Gtk.TreeView(model=self.model)
        treeview.set_rules_hint(True)
        treeview.set_search_column(self.COLUMN_NAME)
        sw.add(treeview)

        self.add_columns(treeview)

        self.window.set_default_size(280, 250)
        self.window.show_all()

    def _search(self, widget, event, entry):
        
        query = entry.get_text()
        print query

        iter_ = self.model.get_iter_first()
        
        while iter_ != None:
            self.model.set_value(iter_, self.COLUMN_TEXT, query)
            iter_ = self.model.iter_next(iter_)

    def create_model(self):
        self.model = Gtk.ListStore(bool,
                                   str,
                                   str,
                                   bool)

        for font in data:
            self.model.append(font.get_arr())

    def add_columns(self, treeview):
        model = treeview.get_model()

        # column for is_fav toggle
        renderer = Gtk.CellRendererToggle()
        renderer.connect('toggled', self.is_fav_toggled, model)

        column = Gtk.TreeViewColumn("Favorite?", renderer,
                                    active=self.COLUMN_FAV)
        column.set_fixed_width(50)
        column.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
        treeview.append_column(column)

        cell_favorite = CellRendererClickablePixbuf()
        #cell_favorite.props.mode = Gtk.CellRendererMode.ACTIVATABLE
        cell_favorite.connect('clicked', self.__favorite_clicked_cb)
        
        cell_favorite = CellRendererClickablePixbuf()
        cell_favorite.connect('clicked', self.is_fav_toggled, model)
        column = Gtk.TreeViewColumn()
        column.pack_start(cell_favorite, True)
        column.set_cell_data_func(cell_favorite, self.__favorite_set_data_cb)
        self.append_column(column)

        # column for font name
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Name", renderer,
                                    text=self.COLUMN_NAME)
        column.set_sort_column_id(self.COLUMN_NAME)
        treeview.append_column(column)

        # column for description
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Description", renderer,
                                    text=self.COLUMN_TEXT)
        column.set_sort_column_id(self.COLUMN_TEXT)
        treeview.append_column(column)

        # column for is_fav toggle
        renderer = Gtk.CellRendererToggle()
        renderer.connect('toggled', self.is_active_toggled, model)

        column = Gtk.TreeViewColumn("active?", renderer,
                                    active=self.COLUMN_ACTIVE)
        column.set_fixed_width(50)
        column.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
        treeview.append_column(column)

    def is_fav_toggled(self, cell, path_str, model):
        # get toggled iter
        iter_ = model.get_iter(path_str)
        is_fav = model.get_value(iter_, self.COLUMN_FAV)

        # do something with value
        is_fav ^= 1

        model.set_value(iter_, self.COLUMN_FAV, is_fav)

    def is_active_toggled(self, cell, path_str, model):
        # get toggled iter
        iter_ = model.get_iter(path_str)
        is_active = model.get_value(iter_, self.COLUMN_ACTIVE)

        # do something with value
        is_active ^= 1

        model.set_value(iter_, self.COLUMN_ACTIVE, is_active)

def main(demoapp=None):
    ListStoreApp()
    Gtk.main()

if __name__ == '__main__':
    main()
