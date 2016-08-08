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
from sugar3.activity.widgets import ActivityToolbarButton
# from sugar3 import mime
from sugar3.activity.widgets import StopButton
# from sugar3.activity.widgets import TitleEntry
# from sugar3.activity.widgets import ShareButton
# from sugar3.activity.widgets import DescriptionItem
from sugar3.graphics.objectchooser import ObjectChooser
from sugar3.graphics.objectchooser import FILTER_TYPE_MIME_BY_ACTIVITY
from sugar3.datastore import datastore
from sugar3 import profile
from sugar3.graphics import style

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
# from editfonts.widgets.misc import ImageButton
# from editfonts.objects.basefont import BaseFont
import editfonts.globals as globals

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
# FIXME: currently the pages are not updated if the page already exists
# currently this has been set to 1 to generate a new page
# everytime a new page is requested by the application
MAX_PAGE_NUM = 1


class EditFonts(activity.Activity):
    """Edit Fonts"""

    def __init__(self, handle):
        # Set up the EditFonts activity
        activity.Activity.__init__(self, handle)

        globals.A = self

        self.modify_bg(Gtk.StateType.NORMAL,
                       style.Color(globals.ACTIVITY_BG).get_gdk_color())

        self.max_participants = 1
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(message)s',
                            filename='EditFonts.log',
                            filemode='w')

        logging.debug("Activity Handle Initialised")

        """Toolbar"""
        toolbar_box = ToolbarBox()

        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        """
        title_entry = TitleEntry(self)
        toolbar_box.toolbar.insert(title_entry, -1)
        title_entry.show()

        description_item = DescriptionItem(self)
        toolbar_box.toolbar.insert(description_item, -1)
        description_item.show()
        """

        # Add the export/import load/save buttons
        separator = Gtk.SeparatorToolItem()
        separator.show()
        toolbar_box.toolbar.insert(separator, -1)

        self.load_btn = ToolButton()
        self.load_btn.props.icon_name = 'load-font'
        self.load_btn.connect('clicked', lambda _: self.load())
        self.load_btn.set_tooltip(_('Load Font'))
        toolbar_box.toolbar.insert(self.load_btn, -1)
        self.load_btn.show()

        self.save_btn = ToolButton()
        self.save_btn.props.icon_name = 'save-font'
        self.save_btn.connect('clicked', lambda _: self.save())
        self.save_btn.set_tooltip(_('Save Font'))
        toolbar_box.toolbar.insert(self.save_btn, -1)
        self.save_btn.show()

        self.import_btn = ToolButton()
        self.import_btn.props.icon_name = 'import-font'
        self.import_btn.connect('clicked', lambda _: self.import_font())
        self.import_btn.set_tooltip(_('Import Font from opentype font file'))
        toolbar_box.toolbar.insert(self.import_btn, -1)
        self.import_btn.show()

        self.export_btn = ToolButton()
        self.export_btn.props.icon_name = 'export-font'
        self.export_btn.connect('clicked', lambda _: self.export_font())
        self.export_btn.set_tooltip(_('Export Font as opentype font file'))
        toolbar_box.toolbar.insert(self.export_btn, -1)
        self.export_btn.show()

        # Add the buttons for all the pages
        separator = Gtk.SeparatorToolItem()
        separator.show()
        toolbar_box.toolbar.insert(separator, -1)

        # Welcome Page Icon
        self.welcome_page_btn = ToolButton()
        self.welcome_page_btn.props.icon_name = 'welcome-page'
        self.welcome_page_btn.connect('clicked',
                                      lambda _: self.set_page('WELCOME'))
        self.welcome_page_btn.set_tooltip(_('Go to the Welcome Page'))
        toolbar_box.toolbar.insert(self.welcome_page_btn, -1)
        self.welcome_page_btn.show()

        # Manager Page Icon
        self.manager_page_btn = ToolButton()
        self.manager_page_btn.props.icon_name = 'manager-page'
        self.manager_page_btn.connect('clicked',
                                      lambda _: self.set_page('MANAGER'))
        self.manager_page_btn.set_tooltip(_('Go to the Manager Page'))
        toolbar_box.toolbar.insert(self.manager_page_btn, -1)
        self.manager_page_btn.show()

        # Summary Page Icon
        self.summary_page_btn = ToolButton()
        self.summary_page_btn.props.icon_name = 'summary-page'
        self.summary_page_btn.connect('clicked',
                                      lambda _: self.set_page('SUMMARY'))
        self.summary_page_btn.set_tooltip(_('Go to the Summary Page'))
        toolbar_box.toolbar.insert(self.summary_page_btn, -1)
        self.summary_page_btn.show()

        # Editor Page Icon
        self.editor_page_btn = ToolButton()
        self.editor_page_btn.props.icon_name = 'editor-page'
        self.editor_page_btn.connect('clicked',
                                     lambda _: self.set_page('EDITOR'))
        self.editor_page_btn.set_tooltip(_('Go to the Editor Page'))
        toolbar_box.toolbar.insert(self.editor_page_btn, -1)
        self.editor_page_btn.show()

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
            self.load(self._jobject.file_path)
        else:
            self.set_page("WELCOME")

        self.set_canvas(self.notebook)
        self.show_all()

    # ############
    # Page Manager
    # ############

    def update_toolbar(self):
        page_num = self.notebook.get_current_page()
        page = self.notebook.get_nth_page(page_num)
        page_name = self.notebook.get_tab_label_text(page)
        if page_name == "WELCOME" or\
                page_name == "CREATEFONT":
            self.welcome_page_btn.set_sensitive(False)
            self.summary_page_btn.set_sensitive(False)
            self.editor_page_btn.set_sensitive(False)
            self.manager_page_btn.set_sensitive(False)

        elif page_name == "SUMMARY":
            self.welcome_page_btn.set_sensitive(True)
            self.summary_page_btn.set_sensitive(False)
            self.editor_page_btn.set_sensitive(True)
            self.manager_page_btn.set_sensitive(True)

        elif page_name == "EDITOR":
            self.welcome_page_btn.set_sensitive(True)
            self.summary_page_btn.set_sensitive(True)
            self.editor_page_btn.set_sensitive(False)
            self.manager_page_btn.set_sensitive(True)

        elif page_name == "MANAGER":
            self.welcome_page_btn.set_sensitive(True)
            self.summary_page_btn.set_sensitive(True)
            self.editor_page_btn.set_sensitive(True)
            self.manager_page_btn.set_sensitive(False)

        else:
            self.welcome_page_btn.set_sensitive(True)
            self.summary_page_btn.set_sensitive(True)
            self.editor_page_btn.set_sensitive(True)
            self.manager_page_btn.set_sensitive(True)

    def set_page(self, page_name):

        page_num = self.create_page(page_name)
        self.notebook.set_current_page(page_num)
        self.update_toolbar()

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

    # ############
    # Fundamentals
    # ############

    def welcome(self):
        self.set_page("WELCOME")

    def create_font(self):
        # FIXME: complete this # noqa
        # check if the current font is saved
        # save the font if its not saved
        # move to create font page
        self.set_page("CREATEFONT")

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

    # ########
    # Load UFO
    # ########

    def _load_from_file(self, file_path):

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

    def load(self, file_path=None):
        """
        If the filePath is None this function opens the Object Chooser Dialog
        for choosing a .zip type file
        If the file contains a *.ufo folder than that
        UFO Font file will be loaded using defcon
        and the current page will be set to Font Summary Page
        if the filepath is specified than the ufo from that filepath is opened
        """
        if file_path is None:

            # FIXME: Add compatibility for earlier versions # noqa
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

                        if not self._load_from_file(jobject.file_path):
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
            if not self._load_from_file(file_path):
                self._show_alert("Error",
                                 "Invalid File type chosen")
                logging.error("File type is invalid")
                return
            else:
                self.set_page("SUMMARY")

        # print success message
        self._show_alert("Success",
                         "Imported Font: " + str(globals.FONT.info.familyName))

    def load_sample(self):
        """
        Load the Sample Font mentioned in globals.py
        """
        # FIXME: Check wether the currently loaded font is saved

        globals.FONT = globals.SAMPLE_FONT
        self.set_page("SUMMARY")

        # print success message
        self._show_alert("Success",
                         "Sample Font Loaded: " +
                         str(globals.FONT.info.familyName))

    # ########
    # Save UFO
    # ########

    def save(self):
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

    # ######
    # Import
    # ######

    def _import_font_from_file(self, file_path):

        try:
            font = Font()
            extractor.extractUFO(file_path, font)
        except:
            logging.error("Unable to Open the chosen file")
            return 0
        else:
            globals.FONT = font

        return 1

    def import_font(self, file_path=None):

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

                            if not self._import_font_from_file(jobject.
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
            if not self._import_font_from_file(file_path):
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

    # ######
    # Export
    # ######

    def export_font(self):
        """
        This function should save the current font loaded
        in globals.FONT as a .otf file
        the file will be saved in the activity data folder
        """
        import subprocess

        def bash_command(cmd):
            subprocess.Popen(['/bin/bash', '-c', cmd])

        bash_command('python -m fontmake -u ' + globals.FONT_PATH +
                     ' -o otf')

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
        # FIXME: This doesn't work # noqa
        # save the font as a  ufo in a temp path
        file_path =\
            os.path.join(self.get_activity_root(),
                         'data', globals.FONT.info.familyName + '.ttf')

        # converting the font to a TTF
        otf = compileTTF(globals.FONT)  # noqa
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

    # ######
    # Alerts
    # ######

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
