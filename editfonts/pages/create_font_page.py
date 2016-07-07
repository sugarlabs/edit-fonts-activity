import os
import shutil
import logging
import subprocess
from gettext import gettext as _

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from editfonts.widgets.custom_box import PageHeading
from editfonts.widgets.custom_box import ImageButton
from editfonts.widgets.form_box import InlineTextInputBox
from editfonts.widgets.form_box import InlineNumberInputBox
from editfonts.objects.basefont import BaseFont
import x

class CreateFontPage(Gtk.VBox):
    """
    This Class Creates the "Create Font" Page
    
    """

    def __init__(self):
        super(CreateFontPage, self).__init__()
        self._init_ui()

    def _init_ui(self):

        heading = PageHeading("Let's Create a new Font", fontSize = '20000')
        self.pack_start(heading, False, False, 10)
        
        #a container box for the form
        form_container = Gtk.HBox()

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER,
                                   Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_border_width(10)

        alignment_box = Gtk.Alignment(xalign=0.5,
                      yalign=0.5,
                      xscale=0,
                      yscale=0)
        scrolled_window.add_with_viewport(alignment_box)
        self.pack_start(scrolled_window, True, True, 0)

        #a vbox to store the form fields 
        form_box = Gtk.VBox()
        alignment_box.add(form_box)

        #Adding the form fields

        #Family Name 
        #Type: Text
        #TODO: Text Formatting: Capitalised
        self.family_name = InlineTextInputBox("Family Name", 
                                        "Enter the name of your font",
                                        "", "*")
        form_box.pack_start(self.family_name, False, False, 10)

        #Style Name 
        #Type: Dropdown
        #Only have "Regular" for now
        vbox = Gtk.VBox()
        hbox = Gtk.HBox()
        name = Gtk.Label("Style Name")
        name.set_tooltip_text('Enter the style of your font')
        msg = Gtk.Label("")
        hbox.pack_start(name, False, False, 5)
        hbox.pack_start(msg, False, False, 5)
        vbox.pack_start(hbox, False, False, 10)
        self.style_name_combo = Gtk.ComboBoxText.new()
        self.style_name_combo.append('regular', 'Regular')
        self.style_name_combo.set_active(0)
        vbox.pack_start(self.style_name_combo, False, False, 0)
        form_box.pack_start(vbox, False, False, 10)

        #Version
        #Default Value: 1.000
        #Type: Text
        self.version = InlineTextInputBox("Version", 
                                        "Enter the version of your font",
                                        "1.000")
        form_box.pack_start(self.version, False, False, 10)

        #Year
        #Default Value: 2016
        #Type: Number
        self.year = InlineNumberInputBox("Year", 
                                        "The year in which the font was created",
                                        "2016", "")
        form_box.pack_start(self.year, False, False, 10)

        #Trademark        
        #Default Value: Blank
        #Type: Text
        self.trademark = InlineTextInputBox("Trademark", 
                                        "Enter the trademark of your font")
        form_box.pack_start(self.version, False, False, 10)

        #Author Info
        #Default Value: Blank
        #Type: Text
        self.author_info = InlineTextInputBox("Author Info", 
                                        "Enter the Name of all the Authors separated a by \',\'",
                                        "", "*")
        form_box.pack_start(self.author_info, False, False, 10)

        #Copyright 
        #Default Value: year The familyname Authors
        #Type: Text
        self.copyright = InlineTextInputBox("Copyright", 
                                        "Enter the Copyright Info",
                                        "2016 The " + self.family_name.get_text()  
                                        + " " + self.author_info.get_text())
        form_box.pack_start(self.copyright, False, False, 10)

        #License,
        #Default Value: This Font Software is licensed under the SIL Open Font License, \
        # Version 1.1. This license is available with a FAQ at: http://scripts.sil.org/OFL
        #Type: Text
        self.license = InlineTextInputBox("License", 
                                        "Enter the license for your font",
                                        "This Font Software is licensed under the SIL Open Font License, Version 1.1.",
                                        "")
        form_box.pack_start(self.license, False, False, 10)
        
        #License URL
        #Default Value: http://scripts.sil.org/OFL
        #Type: Text
        self.license_url = InlineTextInputBox("License URL", 
                                        "Enter a url of the above mentioned license",
                                        "http://scripts.sil.org/OFL", "")
        form_box.pack_start(self.license_url, False, False, 10)
        
        #Cap Height
        #Default Value: 800
        #Type: Number
        self.cap_height = InlineNumberInputBox("Cap Height", 
                                        "The height of the capital letters of the font",
                                        "800", "")
        form_box.pack_start(self.cap_height, False, False, 10)

        #x-height
        #Default Value: 500
        #Type: Number
        self.x_height = InlineNumberInputBox("x Height", 
                                        "The height of the small letters of the font",
                                        "500", "")
        form_box.pack_start(self.x_height, False, False, 10)

        #Ascender 
        #Default Value: 800
        #Type: Number
        self.ascender = InlineNumberInputBox("Ascender", 
                                        "",
                                        "800", "")
        form_box.pack_start(self.ascender, False, False, 10)

        #Descender 
        #Default Value: -200
        #Type: Number
        self.descender = InlineNumberInputBox("Descender", 
                                        "",
                                        "-200", "")
        form_box.pack_start(self.descender, False, False, 10)
                
        #Units per em
        #Default Value: 1000
        #Type: Number
        self.unit_per_em = InlineNumberInputBox("Units per em", 
                                        "",
                                        "1000", "")
        form_box.pack_start(self.unit_per_em, False, False, 10)

        submit_button = ImageButton(icon_name='dialog-ok-active',
                                    fill_color='#32B232')
        submit_button.connect("clicked",self._submit_form)
        
        form_box.pack_start(submit_button, False, False, 10)
          
        self.show_all()

    def _submit_form(self, handle):
        
        #a dictionary for storing the form inputs
        data  = {}
        
        #FIXME: Validate these entries and show an alert if the input is wrong
        #FIXME: Ask for confirmation before the submission 
        data["familyName"] = self.family_name.get_text() 
        data["copyright"] = self.copyright.get_text()
        data["trademark"] = self.trademark.get_text()
        data["styleName"] = self.style_name_combo.get_active_text()
        
        data["ascender"] = int(self.ascender.get_text())
        data["descender"] = int(self.descender.get_text())
        data["capHeight"] = int(self.cap_height.get_text())
        data["unitsPerEm"] = int(self.unit_per_em.get_text())
        data["xHeight"] = int(self.x_height.get_text())
        data["year"] = int(self.year.get_text())
        version = self.version.get_text().split('.')
        data["versionMajor"] = int(version[0])
        data["versionMinor"] = int(version[1])
         
        x.FONT = BaseFont.new_standard_font(data = data)
        
        ##FIXME: Check if font was created or not 
        x.A.set_page("SUMMARY")
