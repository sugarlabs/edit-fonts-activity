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
import sys
# include the path for the third party Libs to the sys path
sys.path.insert(0, os.path.relpath('./third_party'))

import logging
import time
from gettext import gettext as _

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.graphics.toolbutton import ToolButton
from sugar3.activity.widgets import ActivityButton
# from sugar3 import mime
from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import TitleEntry
from sugar3.activity.widgets import ShareButton
from sugar3.activity.widgets import DescriptionItem
from sugar3.graphics.objectchooser import ObjectChooser
from sugar3.graphics.objectchooser import FILTER_TYPE_MIME_BY_ACTIVITY
from sugar3.datastore import datastore
from sugar3 import profile
from sugar3.graphics.alert import Alert
from sugar3.graphics.icon import Icon

from defcon import Font
from ufo2ft import compileOTF
# from ufo2ft import compileTTF
import extractor

from editfonts.pages.summary_page import SummaryPage
from editfonts.pages.editor_page import EditorPage
from editfonts.pages.manager_page import ManagerPage
from editfonts.pages.welcome_page import WelcomePage
from editfonts.pages.create_font_page import CreateFontPage
# from editfonts.objects.basefont import BaseFont
from editfonts.globals import globals

"""
This Dictionary contains all the class types for pages the activity will
ever be needing with a key(eg. "MANAGER") that will be used to access
the class type for that page
"""

PAGE = {'WELCOME': WelcomePage,
        'SUMMARY': SummaryPage,
        'MANAGER': ManagerPage,
        'CREATEFONT': CreateFontPage,
        'EDITOR': EditorPage}

page_list = []

# Max number of pages stored in memory
# FIX ME: currently the pages are not updated if the page already exists
# currently this has been set to 1 to generate a new page
# everytime a new page is requested by the application
MAX_PAGE_NUM = 1


class EditFonts(activity.Activity):
    """Edit Fonts"""

    def __init__(self, handle):
        # Set up the EditFonts activity
        activity.Activity.__init__(self, handle)

        globals.A = self

        self.max_participants = 1
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(message)s',
                            filename='EditFonts.log',
                            filemode='w')

        logging.debug("Activity Handle Initialised")

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

        # Add the export/import load/save buttons

        separator_2 = Gtk.SeparatorToolItem()
        separator_2.show()
        toolbar_box.toolbar.insert(separator_2, -1)

        self.bt_save_ufo = ToolButton()
        self.bt_save_ufo.props.icon_name = 'save-as-otf'
        self.bt_save_ufo.connect('clicked', lambda _: self._save_ufo())
        self.bt_save_ufo.set_tooltip(_('Save UFO'))
        toolbar_box.toolbar.insert(self.bt_save_ufo, -1)
        self.bt_save_ufo.show()

        self.bt_save_as_otf = ToolButton()
        self.bt_save_as_otf.props.icon_name = 'save-as-otf'
        self.bt_save_as_otf.connect('clicked', lambda _: self.load_binary())
        self.bt_save_as_otf.set_tooltip(_('Export OTF'))
        toolbar_box.toolbar.insert(self.bt_save_as_otf, -1)
        self.bt_save_as_otf.show()

        """
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

        """

        separator = Gtk.SeparatorToolItem()
        toolbar_box.toolbar.insert(separator, -1)

        '''
        self.bt_open_page = ToolButton()
        self.bt_open_page.props.icon_name = 'manager'
        self.bt_open_page.connect('clicked',
                                     lambda _: self.set_page("MANAGER"))
        self.bt_open_page.set_tooltip(_('Open Manager Page'))
        toolbar_box.toolbar.insert(self.bt_open_page, -1)
        self.bt_open_page.show()
        '''

        self.bt_open_page = ToolButton()
        self.bt_open_page.props.icon_name = 'summary'
        self.bt_open_page.connect('clicked',
                                  lambda _: self.set_page("SUMMARY"))
        self.bt_open_page.set_tooltip(_('Open Summary Page'))
        toolbar_box.toolbar.insert(self.bt_open_page, -1)
        self.bt_open_page.show()

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

        """Starting the Main Canvas Design"""

        # a gtk notebook object will manage all the pages for this activity
        self.notebook = Gtk.Notebook()

        """Starting the Main Canvas Design"""

        # a gtk notebook object will manage all the pages of the application
        # for this activity
        self.notebook = Gtk.Notebook()

        self.notebook.set_show_tabs(False)

        if self._jobject.file_path is not None and \
                self._jobject.file_path != '':
            self.load_ufo(self._jobject.file_path)
        else:
            self.set_page("WELCOME")

        self.set_canvas(self.notebook)
        self.show_all()

    def set_page(self, page_name):

        page_num = self.create_page(page_name)
        self.notebook.set_current_page(page_num)

    def create_page(self, page_name):

        global page_list

        # check if page already exists
        try:
            # TODO unpack this long line
            l = next(index for (index, page) in enumerate(page_list)
                     if isinstance(page, PAGE[page_name]))

        except StopIteration:
            logging.debug(page_name + " doesn't exist, let me create one")
            # create a new instance and add it to page_list
            self.page = PAGE[page_name]()

            if len(page_list) > MAX_PAGE_NUM - 1:
                page_list.remove(page_list[0])
                self.notebook.remove_page(0)
            page_list.append(self.page)
            self.notebook.append_page(self.page, Gtk.Label(page_name))

            # first delete the first element of the page_list
            page_list = page_list[1:]
            page_list.append(self.page)

        else:
            # print page_name + " exist, just updating it"

            # update the previous instance
            self.page = page_list[l]

        self.page.set_border_width(10)

        page_num = self.notebook.page_num(self.page)

        if page_num == -1:
            logging.error("ERROR: Unable to Create the Page <%s>" % page_name)

        return page_num

    def _load_binary_from_file(self, file_path):

        try:
            font = Font()
            extractor.extractUFO(file_path, font)
        except:
            logging.error("Unable to Open the chosen file")
            return 0
        else:
            globals.FONT = font

        return 1

    def load_binary(self, file_path=None):

        if file_path is None:

            # FIXME: Add compatibility for earlier versions
            # FIXME: Fix the filter type to include either
            # all the objects or only the .otf and .ttf font files
            try:
                chooser = ObjectChooser(
                    parent=self,
                    what_filter=self.get_bundle_id(),
                    filter_type=None)
            except:
                self._show_alert("Error",
                                 "This feature is not Implemented")
                logging.error("This feature is not Implemented")
                return
            else:
                try:
                    result = chooser.run()
                    if result == Gtk.ResponseType.ACCEPT:
                        jobject = chooser.get_selected_object()

                        if jobject and jobject.file_path:

                            if not self._load_binary_from_file(jobject.
                                                               file_path):
                                self._show_alert("Error",
                                                 "Invalid File type chosen")
                                logging.error("File type is invalid")
                                return
                            else:
                                self.set_page("SUMMARY")

                finally:
                    chooser.destroy()
                    del chooser

        else:
            if not self._load_binary_from_file(file_path):
                self._show_alert("Error",
                                 "Invalid File type chosen")
                logging.error("File type is invalid")
                return
            else:
                # save the ufo in the instance folder
                # so that we have a font path which can be
                # needed to perform other actions on the font
                if self._create_font_instance() is not None:
                    self.set_page("SUMMARY")

        # print success message
        self._show_alert("Success",
                         "Imported Font: " + str(globals.FONT.info.familyName))

    def _load_ufo_from_file(self, file_path):

        import zipfile

        try:
            zf = zipfile.ZipFile(file_path)
        except:
            logging.error("Cannot Open Zip file at %s", str(file_path))
            return 0
        else:
            # Get the activities Instance folders path
            instance_path =\
                os.path.join(self.get_activity_root(),
                             'instance', 'tmp%i' % time.time())

            zf.extractall(instance_path)

            # now check if the file extracted is a valid UFO file
            try:
                new_font = Font(instance_path)
            except:
                logging.error("invalid UFO file %s", str(instance_path))
                return 0
            else:
                globals.FONT = new_font
                globals.FONT_PATH = instance_path

        return 1

    def load_ufo(self, file_path=None):
        """
        If the filePath is None this function opens the Object Chooser Dialog
        for choosing a .zip type file
        If the file contains a *.ufo folder than that
        UFO Font file will be loaded using defcon
        and the current page will be set to Font Summary Page
        if the filepath is specified than the ufo from that filepath is opened
        """
        if file_path is None:

            # FIX ME: Add compatibility for earlier versions
            try:
                chooser = ObjectChooser(
                    parent=self,
                    what_filter=self.get_bundle_id(),
                    filter_type=FILTER_TYPE_MIME_BY_ACTIVITY)
            except:
                self._show_alert("Error",
                                 "This feature is not Implemented")
                logging.error("This feature is not Implemented")
                return
            try:
                result = chooser.run()
                if result == Gtk.ResponseType.ACCEPT:
                    jobject = chooser.get_selected_object()

                    if jobject and jobject.file_path:

                        # Now we know the file exists
                        # Check if the file is of the valid format

                        if not self._load_ufo_from_file(jobject.file_path):
                            self._show_alert("Error",
                                             "Invalid File type chosen")
                            logging.error("File type is invalid")
                            return
                        else:
                            self.set_page("SUMMARY")
            finally:
                chooser.destroy()
                del chooser

        else:
            if not self._load_ufo_from_file(file_path):
                self._show_alert("Error",
                                 "Invalid File type chosen")
                logging.error("File type is invalid")
                return
            else:
                self.set_page("SUMMARY")

        # print success message
        self._show_alert("Success",
                         "Imported Font: " + str(globals.FONT.info.familyName))

    def _create_font_instance(self):
        # save the font as a  ufo in a temp path
        instance_path =\
            os.path.join(self.get_activity_root(),
                         'instance', self.metadata['title'] + '.ufo')
        try:
            globals.FONT.save(instance_path)
        except:
            self._show_alert("Error",
                             "Font " + str(globals.FONT.info.familyName) +
                             " has an error")
            self.welcome()
            return None
        else:
            globals.FONT_PATH = instance_path
            return instance_path

    def _save_ufo(self):
        """
        This function should save the current font loaded
        in globals.FONT as a .ufo.zip file
        the file will be saved in the activity data folder
        """
        instance_path = self._create_font_instance()

        if instance_path is None:
            return

        # zip the folder
        import zipfile

        # create an empty zip file in the data folder
        file_path =\
            os.path.join(self.get_activity_root(),
                         'data', self.metadata['title'] + '.ufo.zip')
        zipf = zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED)

        for root, dirs, files in os.walk(instance_path):
            for file in files:
                relroot = os.path.relpath(root, instance_path)
                zipf.write(os.path.join(root, file),
                           os.path.join(relroot, file))
        zipf.close()

        # create a journal entry
        jobject = datastore.create()
        jobject.metadata['icon-color'] = profile.get_color().to_string()
        jobject.metadata['mime_type'] = 'application/zip'
        jobject.metadata['title'] = self.metadata['title']
        jobject.file_path = file_path
        datastore.write(jobject, transfer_ownership=True)
        self._object_id = jobject.object_id

        # create an alert
        success_title = 'Success'
        success_msg = 'A UFO Font zip file was created in the Journal'
        self._show_journal_alert(_(success_title), _(success_msg))

    def _export_otf(self, button):
        """
        This function should save the current font loaded
        in globals.FONT as a .ttf file
        the file will be saved in the activity data folder
        """
        # save the font as a  ufo in a temp path
        file_path =\
            os.path.join(self.get_activity_root(),
                         'data', globals.FONT.info.familyName + '.otf')

        # converting the font to a OTF
        otf = compileOTF(globals.FONT)
        otf.save(file_path)

        # create a journal entry
        jobject = datastore.create()
        jobject.metadata['icon-color'] = profile.get_color().to_string()
        jobject.metadata['mime_type'] = 'application/x-font-opentype'
        jobject.metadata['title'] = globals.FONT.info.familyName + '.otf'
        jobject.file_path = file_path
        datastore.write(jobject, transfer_ownership=True)
        self._object_id = jobject.object_id

        success_title = 'Success'
        success_msg = 'A OTF Font file was created in the Journal'
        self._show_journal_alert(_(success_title), _(success_msg))

    """
    def _export_ttf(self, button):
        #FIX ME: This doesn't work

        # save the font as a  ufo in a temp path
        file_path =\
            os.path.join(self.get_activity_root(),
                         'data', globals.FONT.info.familyName + '.ttf')

        # converting the font to a TTF
        otf = compileTTF(globals.FONT)
        otf.save(file_path)

        # create a journal entry
        jobject = datastore.create()
        jobject.metadata['icon-color'] = profile.get_color().to_string()
        jobject.metadata['mime_type'] = 'application/x-font-ttf'
        jobject.metadata['title'] = globals.FONT.info.familyName + '.ttf'
        jobject.file_path = file_path
        datastore.write(jobject, transfer_ownership=True)
        self._object_id = jobject.object_id

        success_title = 'Success'
        success_msg = 'A TTF Font file was created in the Journal'
        self._show_journal_alert(_(success_title), _(success_msg))
    """

    def _show_journal_alert(self, title, msg):
        _stop_alert = Alert()
        _stop_alert.props.title = title
        _stop_alert.props.msg = msg
        _stop_alert.add_button(Gtk.ResponseType.APPLY,
                               _('Show in Journal'),
                               Icon(icon_name='zoom-activity'))
        _stop_alert.add_button(Gtk.ResponseType.OK, _('Ok'),
                               Icon(icon_name='dialog-ok'))
        # Remove other alerts
        for alert in self._alerts:
            self.remove_alert(alert)

        self.add_alert(_stop_alert)
        _stop_alert.connect('response', self.__stop_response_cb)
        _stop_alert.show_all()

    def _show_alert(self, title, msg):
        _stop_alert = Alert()
        _stop_alert.props.title = title
        _stop_alert.props.msg = msg
        _stop_alert.add_button(Gtk.ResponseType.OK, _('Ok'),
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
