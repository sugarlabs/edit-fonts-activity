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
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.activity.widgets import StopButton

from sugar3.activity.widgets import ActivityButton
from sugar3.activity.widgets import TitleEntry
from sugar3.activity.widgets import ShareButton
from sugar3.activity.widgets import DescriptionItem
import cairo

import math
from defcon import Font

#This has all the custom made widgets required for this library
from defconGTK.summaryPage import SummaryPage
from defconGTK.editorPage import EditorPage

from toolbar import BasicToolbar
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

        toolbar_box = BasicToolbar(self)
        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        #testing defcon 
        self.main_path = "sample"
        self.main_font = Font(self.main_path)
       
        self.glyphName = 'A'

        #Starting the Main Canvas Design
        #a gtk notebook object will manga all the pages of the application for this activity

        self.notebook= Gtk.Notebook()
        
        self.notebook.set_show_tabs(False)

        self.create_all_pages()
        self.set_page("SUMMARY")

        """
        #PAGE_MANAGER.font = font
        
        #Outermost invisible box  
        #this will be added to the canvas later
        vbox = Gtk.VBox(homogeneous=False, spacing=8)
        
        #Making the Page Heading
        headingBox = Gtk.Box()

        HEADING_STRING = "<span foreground='black' size='20000' font='Cantarell' font_weight='bold'>Character Map</span>"

        pageHeading = Gtk.Label()
        pageHeading.set_markup(HEADING_STRING)
        headingBox.add(pageHeading)

        alignHeading = Gtk.Alignment(xalign=0.5,
                              yalign=0.5,
                              xscale=0,
                              yscale=0)
        alignHeading.add(headingBox)
        
        vbox.pack_start(alignHeading, False, False, 30)

        #using scroll view
        #CharacterMap = characterMap(font, 15, 10, 'SCROLL')
        
        #using button view
        #CharacterMap = characterMap(font, 15, 10, 'BUTTON')

        #single line character map for Eli's Layout
        characterMap = CharacterMap(font, 15, 10, 'BUTTON')
       
        vbox.pack_start(characterMap, True, True, 0)
        
        """
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