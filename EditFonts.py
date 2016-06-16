# Copyright 2016 Yash Agarwal
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

"""Edit Fonts Activity: Kids make fonts!"""

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
from sugar3.graphics.toolbarbox import ToolbarBox , ToolbarButton
from sugar3.graphics.toolbutton import ToolButton
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.activity.widgets import StopButton

from sugar3.activity.widgets import ActivityButton
from sugar3.activity.widgets import TitleEntry
from sugar3.activity.widgets import ShareButton
from sugar3.activity.widgets import DescriptionItem
import cairo

import math
from defcon import Font
from ufo2ft import compileOTF, compileTTF
import extractor

#This has all the custom made widgets required for this library
from defconGTK.summaryPage import SummaryPage
from defconGTK.editorPage import EditorPage

#import pager

PAGE = {"EDITOR":1 , "SUMMARY":0 }

class EditFonts(activity.Activity):
    """Edit Fonts"""

    def __init__(self, handle):
        """Set up the EditFonts activity."""
        activity.Activity.__init__(self, handle)

        # we do not have collaboration features
        # make the share option insensitive
        self.max_participants = 1

        """
        Toolbar
        """
        toolbar_box = ToolbarBox()

        activity_button = ActivityButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        title_entry = TitleEntry(self)
        toolbar_box.toolbar.insert(title_entry, -1)
        title_entry.show()

        description_item = DescriptionItem(self)
        toolbar_box.toolbar.insert(description_item, -1)
        description_item.show()

        share_button = ShareButton(self)
        toolbar_box.toolbar.insert(share_button, -1)
        share_button.show()

        separator_2 = Gtk.SeparatorToolItem()
        separator_2.show()
        toolbar_box.toolbar.insert(separator_2, -1)

        self.bt_save_as_ttf = ToolButton()
        self.bt_save_as_ttf.props.icon_name = 'save-as-ttf'
        self.bt_save_as_ttf.connect('clicked', self._write_ttf)
        self.bt_save_as_ttf.set_tooltip(_('Export TTF'))
        toolbar_box.toolbar.insert(self.bt_save_as_ttf, -1)
        self.bt_save_as_ttf.show()

        self.bt_save_as_otf = ToolButton()
        self.bt_save_as_otf.props.icon_name = 'save-as-otf'
        self.bt_save_as_otf.connect('clicked', self._write_otf)
        self.bt_save_as_otf.set_tooltip(_('Export OTF'))
        toolbar_box.toolbar.insert(self.bt_save_as_otf, -1)
        self.bt_save_as_otf.show()

        self.bt_load_otf = ToolButton()
        self.bt_load_otf.props.icon_name = 'save-as-otf'
        self.bt_load_otf.connect('clicked', self._load_otf)
        self.bt_load_otf.set_tooltip(_('Load OTF'))
        toolbar_box.toolbar.insert(self.bt_load_otf, -1)
        self.bt_load_otf.show()

        self.bt_save_ufo = ToolButton()
        self.bt_save_ufo.props.icon_name = 'save-as-otf'
        self.bt_save_ufo.connect('clicked', self._write_ufo)
        self.bt_save_ufo.set_tooltip(_('Save UFO'))
        toolbar_box.toolbar.insert(self.bt_save_ufo, -1)
        self.bt_save_ufo.show()

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

        """
        Toolbar ends here
        """

        #testing defcon 
        self.main_path = "ufo/sample.ufo"
        self.main_font = Font(self.main_path)
       
        self.glyphName = 'A'

        """
        Starting the Main Canvas Design
        """
        #a gtk notebook object will manga all the pages of the application for this activity
        self.notebook= Gtk.Notebook()
        
        self.notebook.set_show_tabs(False)

        self.create_all_pages()
        self.set_page("SUMMARY")

        self.set_canvas(self.notebook)
        self.show_all()


    def create_all_pages(self):
        
        for pageName, pageNumber in PAGE.iteritems():
            self.create_page(pageName)

    def set_page(self, pageName):

        self.create_page(pageName)
        
        if pageName == "SUMMARY":
            self.notebook.set_current_page(PAGE[pageName])
        
        elif pageName == "EDITOR":
            self.notebook.set_current_page(PAGE[pageName])
        
    def create_page(self, pageName):

        if pageName == "SUMMARY":
            self.summary_page = SummaryPage(self)
            self.summary_page.set_border_width(10)
            self.notebook.remove_page(PAGE[pageName])
            self.notebook.insert_page(self.summary_page, Gtk.Label("Summary Page") , PAGE[pageName])
            
        elif pageName == "EDITOR":
            self.editor_page = EditorPage(self)
            self.editor_page.set_border_width(10)
            self.notebook.remove_page(PAGE[pageName])
            self.notebook.insert_page(self.editor_page, Gtk.Label("Summary Page") , PAGE[pageName])

    def _load_otf(self, button):
        ##NOT WORKING##
        ##unable to access the path##

        path = "NotoSerif-Regular.ttf"
        file_name = os.path.join(self.get_activity_root(),
                                 path)

        extractor.extractUFO(file_name, self.main_font)

    def _write_ttf(self, button):
        ##NOT WORKING##
        ##Error: defcon.errors.DefconError: the kerning data is not valid##

        file_name = os.path.join(self.get_activity_root(), 'instance',
                                 '%s.ttf' % self.metadata['title'])

        #file_name = self.metadata['title'] + '.ttf' 

        ttf = compileTTF(self.main_font)
        ttf.save(file_name)
        
        jobject = datastore.create()
        jobject.metadata['icon-color'] = profile.get_color().to_string()
        jobject.metadata['mime_type'] = 'application/ttf'

        jobject.metadata['title'] = self.metadata['title']
        jobject.file_path = file_name

        # jobject.metadata['preview'] = \
        #    self._get_preview_image(file_name)

        datastore.write(jobject, transfer_ownership=True)
        self._object_id = jobject.object_id

        self._show_journal_alert(_('Success'),
                                 _('A TTF Font file was created in the Journal'))

    def _write_ufo(self, button):
        ##NOT WORKING##
        ##Error: defcon.errors.DefconError: the kerning data is not valid##

        file_name = os.path.join(self.get_activity_root(), 'instance',
                                 '%s.ufo' % self.metadata['title'])

        #file_name = self.metadata['title'] + '.ttf' 
        self.main_font.save(file_name)

        jobject = datastore.create()
        jobject.metadata['icon-color'] = profile.get_color().to_string()
        jobject.metadata['mime_type'] = 'application/ufo'

        jobject.metadata['title'] = self.metadata['title']
        jobject.file_path = file_name

        # jobject.metadata['preview'] = \
        #    self._get_preview_image(file_name)

        datastore.write(jobject, transfer_ownership=True)
        self._object_id = jobject.object_id

        self._show_journal_alert(_('Success'),
                                 _('A UFO Font file was created in the Journal'))

    def _write_otf(self, button):
        ##NOT WORKING##
        ##Error: defcon.errors.DefconError: the kerning data is not valid##

        file_name = os.path.join(self.get_activity_root(), 'instance',
                                 '%s.otf' % self.metadata['title'])

        otf = compileTTF(self.main_font)
        otf.save(file_name)
        
        jobject = datastore.create()
        jobject.metadata['icon-color'] = profile.get_color().to_string()
        jobject.metadata['mime_type'] = 'application/otf'

        jobject.metadata['title'] = self.metadata['title']
        jobject.file_path = file_name

        datastore.write(jobject, transfer_ownership=True)
        self._object_id = jobject.object_id

        self._show_journal_alert(_('Success'),
                                 _('A OTF Font file was created in the Journal'))

