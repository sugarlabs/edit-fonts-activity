# Copyright 2016 Eli Heuer
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

class EditFonts(activity.Activity):
    """Edit Fonts"""

    def __init__(self, handle):
        """Set up the EditFonts activity."""
        activity.Activity.__init__(self, handle)

        # we do not have collaboration features
        # make the share option insensitive
        self.max_participants = 1

        # toolbar with the new toolbar redesign
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

        #testing defcon 
        path = "sample"
        font = Font(path)
        glyph = font['A']
        print(glyph.name)

        #Starting the Main Canvas Design

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

        #Grid Parameters
        GRID_HEIGHT= 7;   #number of rows
        GRID_WIDTH = 14;  #number of columns  
        GRID_BOX_SIZE = 80;
        GRID_ROW_SPACING = 10;
        GRID_COLUMN_SPACING = GRID_ROW_SPACING;
        GRID_ELEMENT_NUMBER = 100;

        grid = Gtk.Grid()
        grid.set_row_spacing(GRID_ROW_SPACING)
        grid.set_column_spacing(GRID_COLUMN_SPACING)

        # The alignment keeps the grid center aligned
        align = Gtk.Alignment(xalign=0.5,
                              yalign=0.5,
                              xscale=0,
                              yscale=0)
        align.add(grid)
        vbox.pack_start(align, True, True, 0)

        for j in range(0,GRID_HEIGHT): 
            for i in range(0,GRID_WIDTH):     
                da = Gtk.DrawingArea()
                da.set_size_request(GRID_BOX_SIZE, GRID_BOX_SIZE)
                box= Gtk.Box();
                box.pack_start(da, True, True, 0)
                grid.attach(box, i, j, 1, 1)
                #position = i*GRID_WIDTH + j
                #glyph = font[position]
                data = [glyph, GRID_BOX_SIZE]
                da.connect('draw', self.glyph_render_event, data)

        self.set_canvas(vbox)
        self.show_all()

    def glyph_render_event(self, da, cairo_ctx, data):

        BOX_SIZE = data[1]
        glyph = data[0]
        bounds = glyph.bounds
        
        #Currently the Glyph Rendering method is not Normalised
        """
        GLYPH_WIDTH=bounds[2]-bounds[0]
        GLYPH_HEIGHT=bounds[3]-bounds[1]

        cairo_ctx.set_source_rgb(0, 0, 0)
        #cairo_ctx.set_line_width(1)
        cairo_ctx.scale(BOX_SIZE, BOX_SIZE)

        for contour in glyph:
            
            #move to initial point
            point = contour[0]
            cairo_ctx.move_to(point.x/GLYPH_WIDTH, 1 - point.y/GLYPH_HEIGHT)
                        
            for segment in contour.segments:
                #drawSegment(wid, cr, segment)
                #first determine type of Segment
                #print(segment)
                if len(segment) == 3:
                    #its a bezier
                    cairo_ctx.curve_to(segment[0].x/GLYPH_WIDTH, 1 - segment[0].y/GLYPH_HEIGHT, segment[1].x/GLYPH_WIDTH ,1-segment[1].y/GLYPH_HEIGHT ,segment[2].x/GLYPH_WIDTH,1-segment[2].y/GLYPH_HEIGHT)

                elif len(segment) == 1:
                    #its a line
                    cairo_ctx.line_to(segment[0].x/GLYPH_WIDTH, 1-segment[0].y/GLYPH_HEIGHT);

                else:
                    print("Error: Unknown Case Found")            
                    print(segment)

            #close the contour
            cairo_ctx.close_path()
            
        #fill the contour
        cairo_ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD);
        cairo_ctx.fill();             
        cairo_ctx.stroke()
        """
        
        cairo_ctx.scale (BOX_SIZE, BOX_SIZE) # Normalizing the canvas
        cairo_ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    
        pat = cairo.LinearGradient (0.0, 0.0, 0.0, 1.0)
        pat.add_color_stop_rgba (1, 0.7, 0, 0, 0.5) # First stop, 50% opacity
        pat.add_color_stop_rgba (0, 0.9, 0.7, 0.2, 1) # Last stop, 100% opacity

        cairo_ctx.rectangle (0, 0, 1, 1) # Rectangle(x0, y0, x1, y1)
        cairo_ctx.set_source (pat)
        cairo_ctx.fill ()

        cairo_ctx.translate (0.1, 0.1) # Changing the current transformation matrix
        cairo_ctx.set_source_rgb (0.3, 0.2, 0.5) # Solid color
        cairo_ctx.set_line_width (0.02)

        cairo_ctx.move_to (0, 0)
        cairo_ctx.line_to (0.5, 0.1) # Line to (x,y)
        cairo_ctx.curve_to (0.5, 0.2, 0.5, 0.4, 0.2, 0.8) # Curve(x1, y1, x2, y2, x3, y3)
        cairo_ctx.close_path ()

        cairo_ctx.translate (0.15, 0.15) # Changing the current transformation matrix
        cairo_ctx.set_source_rgb (0.5, 0.5, 0.5) # Solid color
        cairo_ctx.set_line_width (0.2)
        cairo_ctx.move_to (0, 0)
        cairo_ctx.line_to (0.3, 0.1) # Line to (x,y)
        cairo_ctx.curve_to (0.3, 0.2, 0.1, 0.1, 0.1, 0.25) # Curve(x1, y1, x2, y2, x3, y3)
        cairo_ctx.close_path ()
        cairo_ctx.fill ()
        cairo_ctx.stroke ()
