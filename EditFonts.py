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
import time
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
from sugar3.graphics.toolbutton import ToolButton
from sugar3.activity.widgets import ActivityButton
from sugar3.graphics.toggletoolbutton import ToggleToolButton

from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import TitleEntry
from sugar3.activity.widgets import ShareButton
from sugar3.activity.widgets import DescriptionItem
from sugar3.graphics.objectchooser import ObjectChooser
from sugar3.graphics.objectchooser import FILTER_TYPE_MIME_BY_ACTIVITY
from sugar3.datastore import datastore
from sugar3 import profile
from sugar3.graphics import style
from sugar3.graphics.alert import Alert
from sugar3.graphics.icon import Icon
from sugar3.graphics.palette import Palette

import cairo

import math
from defcon import Font
from ufo2ft import compileOTF, compileTTF
import extractor

from editfonts.pages.summary_page import SummaryPage
from editfonts.pages.editor_page import EditorPage
from editfonts.pages.manager_page import ManagerPage
from editfonts.pages.welcome_page import WelcomePage
from editfonts.pages.create_font_page import CreateFontPage


""" 
This Dictionary contains all the class types for pages the activity will ever be needing with a 
key(eg. "MANAGER") that will be used to access the class type for that page 

"""
PAGE = {'SUMMARY': SummaryPage, 
        'EDITOR': EditorPage, 
        'MANAGER': ManagerPage,
        'WELCOME': WelcomePage,
        'CREATEFONT': CreateFontPage}

page_list = []

#Max number of pages stored in memory
MAX_PAGE_NUM = 3

class EditFonts(activity.Activity):
    """Edit Fonts"""

    def __init__(self, handle):
        """Set up the EditFonts activity."""
        activity.Activity.__init__(self, handle)

        #self.modify_bg(Gtk.StateType.NORMAL,
        #                        style.Color('#D6EAF8').get_gdk_color())

        # we do not have collaboration features
        # make the share option insensitive
        self.max_participants = 1
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(message)s',
                            filename='EditFonts.log',
                            filemode='w')
        """Toolbar"""
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
        self.bt_load_otf.connect('clicked', lambda _: self._load_binary())
        self.bt_load_otf.set_tooltip(_('Load OTF/TTF'))
        toolbar_box.toolbar.insert(self.bt_load_otf, -1)
        self.bt_load_otf.show()

        self.bt_save_ufo = ToolButton()
        self.bt_save_ufo.props.icon_name = 'save-as-otf'
        self.bt_save_ufo.connect('clicked', self._write_ufo)
        self.bt_save_ufo.set_tooltip(_('Save UFO'))
        toolbar_box.toolbar.insert(self.bt_save_ufo, -1)
        self.bt_save_ufo.show()

        separator = Gtk.SeparatorToolItem()
        toolbar_box.toolbar.insert(separator, -1)

        self.bt_open_manager = ToolButton()
        self.bt_open_manager.props.icon_name = 'manager'
        self.bt_open_manager.connect('clicked',
                                     lambda _: self.set_page("MANAGER"))
        self.bt_open_manager.set_tooltip(_('Open Manager'))
        toolbar_box.toolbar.insert(self.bt_open_manager, -1)
        self.bt_open_manager.show()

        self.bt_open_editor = ToolButton()
        self.bt_open_editor.props.icon_name = 'edit'
        self.bt_open_editor.connect('clicked',
                                    lambda _: self.set_page("EDITOR"))
        self.bt_open_editor.set_tooltip(_('Open Editor(Temporary Button)'))
        toolbar_box.toolbar.insert(self.bt_open_editor, -1)
        self.bt_open_editor.show()


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
        
        """Toolbar ends here"""
        
        """Loading Font"""

        self.main_path = "test_fonts/sample.ufo"
        self.main_font = Font(self.main_path)

        self.glyphName = 'A'
        
        """Starting the Main Canvas Design"""

        #a gtk notebook object will manage all the pages for this activity
        self.notebook = Gtk.Notebook()

        self.notebook.set_show_tabs(True)

        self.set_page("WELCOME")

        self.set_canvas(self.notebook)
        self.show_all()

    def set_page(self, page_name):

        self.notebook.set_current_page(self.create_page(page_name))

    def create_page(self, page_name):

        global page_list

        #check if page already exists
        try:
            l = next(index for (index, page) in enumerate(page_list)
                     if isinstance(page, PAGE[page_name]))

        except StopIteration:
            logging.debug(page_name + " doesn't exist, let me create one")
            #create a new instance and add it to page_list
            self.page = PAGE[page_name](self)

            if len(page_list) > MAX_PAGE_NUM - 1:
                page_list.remove(page_list[0])
                self.notebook.remove_page(0)
            page_list.append(self.page)
            self.notebook.append_page(self.page, Gtk.Label(page_name))

        else:
            print page_name + " already exists, just updating it"

            #update the previous instance
            self.page = page_list[l]
            self.page.update(self)

        self.page.set_border_width(10)
        
        page_num = self.notebook.page_num(self.page)

        if page_num == -1:
            logging.error("ERROR: Unable to Create the Page <%s>" % page_name)
                    
        return page_num

    def _load_binary(self, filePath=None):

        if filePath is None:

            #FIX ME: Add compatibility for earlier versions
            try:
                chooser = ObjectChooser(
                    parent=self,
                    what_filter=self.get_bundle_id(),
                    filter_type=FILTER_TYPE_MIME_BY_ACTIVITY)
            except:
                chooser = ObjectChooser(parent=self,
                                        what_filter=mime.GENERIC_TYPE_TEXT)

            try:
                result = chooser.run()
                if result == Gtk.ResponseType.ACCEPT:
                    logging.error('ObjectChooser: %r' %
                                  chooser.get_selected_object())
                    jobject = chooser.get_selected_object()
                    if jobject and jobject.file_path:
                        logging.error("imagen seleccionada: %s",
                                      jobject.file_path)
                        tempfile_name = \
                            os.path.join(self.get_activity_root(),
                                         'instance', 'tmp%i' % time.time())
                        os.link(jobject.file_path, tempfile_name)
                        logging.error("tempfile_name: %s", tempfile_name)
                        newFont = Font()
                        extractor.extractUFO(tempfile_name, newFont)
                        self.main_font = newFont
                        self.set_page("SUMMARY")
            finally:
                chooser.destroy()
                del chooser

        else:

            filePath = 'test_fonts/Noto.ttf'
            #path = "test_fonts/Noto.ttf"
            #file_name = os.path.join(self.get_activity_root(),path)
            newFont = Font()

            try:
                extractor.extractUFO(filePath, newFont)
                #print Gio.content_type_guess(filePath, None)[0]
                #FIX ME: Check that if main_font has unsaved changes
                self.main_font = newFont
                self.set_page("SUMMARY")
            except Exception, e:
                raise e

    def load_ufo(self, filePath=None):
        """
        If the filePath is None this function opens the Object Chooser Dialog
        for choosing a .plist type file 
        If the file is named metainfo.plist and in contained within a *.ufo folder
        than that ufo will be loaded using defcon
        and the current page will be set to Font Summary Page
        if the filepath is specified than the ufo from that filepath is opened
        """
        if filePath is None:

            #FIX ME: Add compatibility for earlier versions
            try:
                chooser = ObjectChooser(
                    parent=self,
                    what_filter=self.get_bundle_id(),
                    filter_type=FILTER_TYPE_MIME_BY_ACTIVITY)
            except:
                chooser = ObjectChooser(parent=self,
                                        what_filter=mime.GENERIC_TYPE_TEXT)

            try:
                result = chooser.run()
                if result == Gtk.ResponseType.ACCEPT:
                    logging.error('ObjectChooser: %r' %
                                  chooser.get_selected_object())
                    jobject = chooser.get_selected_object()
                    print jobject.file_path
                    
                    if jobject and jobject.file_path:
                        
                        logging.error("Selected File: %s",
                                      jobject.file_path)
                        
                        tempfile_name = \
                            os.path.join(self.get_activity_root(),
                                         'instance', 'tmp%i' % time.time())
                        os.link(jobject.file_path, tempfile_name)
                        logging.error("tempfile_name: %s", tempfile_name)
                        newFont = Font()
                        extractor.extractUFO(tempfile_name, newFont)
                        self.main_font = newFont
                        self.set_page("SUMMARY")
                        
            finally:
                chooser.destroy()
                del chooser

        else:

            filePath = 'test_fonts/Noto.ttf'
            #path = "test_fonts/Noto.ttf"
            #file_name = os.path.join(self.get_activity_root(),path)
            newFont = Font()

            try:
                extractor.extractUFO(filePath, newFont)
                #print Gio.content_type_guess(filePath, None)[0]
                #FIX ME: Check that if main_font has unsaved changes
                self.main_font = newFont
                self.set_page("SUMMARY")
            except Exception, e:
                raise e


    def _write_ttf(self, button):
        ##NOT WORKING##
        ##Error: defcon.errors.DefconError: the kerning data is not valid##

        file_name = os.path.join(self.get_activity_root(), 'data',
                                 '%s.ttf' % self.metadata['title'])

        #file_name = "a.ttf"
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

        self._show_journal_alert(
            _('Success'), _('A TTF Font file was created in the Journal'))

    def _write_ufo(self, button):
        ##NOT WORKING##
        ##Error: defcon.errors.DefconError: the kerning data is not valid##

        #file_name = os.path.join(self.get_activity_root(), 'data',
        #                         '%s.ufo' % self.metadata['title'])
        #file_obj = open(file_name, 'w')

        file_name = "~/Documents/UFOs/abc1.ufo"

        #file_name = self.metadata['title'] + '.ttf'
        print "Printing UFO"
        self.main_font.save(file_name)
        print "Printing UFO Done"

        #file_obj.close()

        jobject = datastore.create()
        jobject.metadata['icon-color'] = profile.get_color().to_string()
        jobject.metadata['mime_type'] = 'application/x-plist'
        print "a"

        jobject.metadata['title'] = self.metadata['title']
        jobject.file_path = os.path.join(file_name, "metainfo.plist")

        # jobject.metadata['preview'] = \
        #    self._get_preview_image(file_name)
        print "b"

        datastore.write(jobject, transfer_ownership=True)
        print "c"

        self._object_id = jobject.object_id
        print "d"

        self._show_journal_alert(
            _('Success'), _('A UFO Font file was created in the Journal'))
        print "e"

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

        self._show_journal_alert(
            _('Success'), _('A OTF Font file was created in the Journal'))

    def _show_journal_alert(self, title, msg):
        _stop_alert = Alert()
        _stop_alert.props.title = title
        _stop_alert.props.msg = msg
        _stop_alert.add_button(Gtk.ResponseType.APPLY,
                               _('Show in Journal'),
                               Icon(icon_name='zoom-activity'))
        _stop_alert.add_button(Gtk.ResponseType.OK,
                               _('Ok'),
                               Icon(icon_name='dialog-ok'))
        # Remove other alerts
        for alert in self._alerts:
            self.remove_alert(alert)

        self.add_alert(_stop_alert)
        _stop_alert.connect('response', self.__stop_response_cb)
        _stop_alert.show_all()

    def __stop_response_cb(self, alert, response_id):
        if response_id is Gtk.ResponseType.APPLY:
            activity.show_object_in_journal(self._object_id)
        self.remove_alert(alert)

    def create_font(self):
        self.set_page("CREATEFONT")
