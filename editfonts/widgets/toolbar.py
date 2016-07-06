from gi.repository import Gtk, Gdk
from defcon import Font
from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.activity.widgets import StopButton

from sugar3.activity.widgets import ActivityButton
from sugar3.activity.widgets import TitleEntry
from sugar3.activity.widgets import ShareButton
from sugar3.activity.widgets import DescriptionItem


class BasicToolbar(ToolbarBox):
    def __init__(self, activity, **kwargs):
        super(BasicToolbar, self).__init__(**kwargs)

        activity_button = ActivityButton(activity)
        self.toolbar.insert(activity_button, 0)
        activity_button.show()

        title_entry = TitleEntry(activity)
        self.toolbar.insert(title_entry, -1)
        title_entry.show()

        description_item = DescriptionItem(activity)
        self.toolbar.insert(description_item, -1)
        description_item.show()

        share_button = ShareButton(activity)
        self.toolbar.insert(share_button, -1)
        share_button.show()

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        self.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(activity)
        self.toolbar.insert(stop_button, -1)
        stop_button.show()
