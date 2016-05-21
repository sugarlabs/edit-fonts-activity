#
# ReadEtextsActivity2.py  A version of ReadEtextsActivity with better
# toolbars and other refinements.
# Copyright (C) 2010  James D. Simmons
# Copyright (C) 2012  Aneesh Dogra <lionaneesh@gmail.com>
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
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
import zipfile
import re
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango
from sugar3.activity import activity
from sugar3.graphics import style
from sugar3.graphics.toolbutton import ToolButton
from sugar3.graphics.toolbarbox import ToolbarButton
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import EditToolbar
from sugar3.activity.widgets import ActivityToolbar
from sugar3.activity.widgets import _create_activity_icon
from toolbar import ViewToolbar
from gettext import gettext as _


class CustomActivityToolbarButton(ToolbarButton):
    """
        Custom Activity Toolbar button, adds the functionality to disable or
        enable the share button.
    """
    def __init__(self, activity, shared=False, **kwargs):
        toolbar = ActivityToolbar(activity, orientation_left=True)

        if not shared:
            toolbar.share.props.visible = False

        ToolbarButton.__init__(self, page=toolbar, **kwargs)

        icon = _create_activity_icon(activity.metadata)
        self.set_icon_widget(icon)
        icon.show()

