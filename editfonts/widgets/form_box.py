import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from gi.repository import Gdk

from sugar3.graphics.icon import Icon
from sugar3.graphics import style

class NumberEntry(Gtk.Entry):
    
    def __init__(self):
        Gtk.Entry.__init__(self)
        self.connect('notify::text', self.on_changed)

    def on_changed(self, *args):
        text = self.get_text().strip()
        self.set_text(''.join([i for i in text if i in '-0123456789']))

class InlineTextInputBox(Gtk.HBox):
    
    def __init__(self, fieldName, description="" , defaultText="", message=""):
        Gtk.HBox.__init__(self)
        
        name = Gtk.Label(fieldName)
        name.set_tooltip_text(description)
        msg = Gtk.Label(message) 
        self.pack_start(name, False, False, 5)
        self.pack_start(msg, False, False, 5)
        self.entry = Gtk.Entry()
        self.set_text(defaultText)
        self.pack_start(self.entry, True, True, 0)
        self.show_all()

    def get_text(self):
        return self.entry.get_text()
        
    def set_text(self, data):
        self.entry.set_text(data)

class TextInputBox(Gtk.VBox):
    
    def __init__(self, fieldName, description="" , defaultText="", message=""):
        Gtk.VBox.__init__(self)
        
        hbox = Gtk.HBox()
        name = Gtk.Label(fieldName)
        name.set_tooltip_text(description)
        msg = Gtk.Label(message) 
        hbox.pack_start(name, False, False, 5)
        hbox.pack_start(msg, False, False, 5)
        self.pack_start(hbox, False, False, 10)
        self.entry = Gtk.Entry()
        self.set_text(defaultText)
        self.pack_start(self.entry, False, False, 0)
        self.show_all()

    def get_text(self):
        return self.entry.get_text()
        
    def set_text(self, data):
        self.entry.set_text(data)

class InlineNumberInputBox(Gtk.HBox):
    
    def __init__(self, fieldName, description="" , defaultText="0", message=""):
        Gtk.HBox.__init__(self)
        
        name = Gtk.Label(fieldName)
        name.set_tooltip_text(description)
        msg = Gtk.Label(message) 
        self.pack_start(name, False, False, 5)
        self.pack_start(msg, False, False, 5)
        self.entry = NumberEntry()
        self.set_text(defaultText)
        self.pack_start(self.entry, True, True, 0)
        self.show_all()

    def get_text(self):
        return self.entry.get_text()
        
    def set_text(self, data):
        self.entry.set_text(data)


class NumberInputBox(Gtk.VBox):
    
    def __init__(self, fieldName, description="" , defaultText="0", message=""):
        Gtk.VBox.__init__(self)
        
        hbox = Gtk.HBox()
        name = Gtk.Label(fieldName)
        name.set_tooltip_text(description)
        msg = Gtk.Label(message) 
        hbox.pack_start(name, False, False, 5)
        hbox.pack_start(msg, False, False, 5)
        self.pack_start(hbox, False, False, 0)
        self.entry = NumberEntry()
        self.set_text(defaultText)
        self.pack_start(self.entry, False, False, 0)
        self.show_all()

    def get_text(self):
        return self.entry.get_text()
        
    def set_text(self, data):
        self.entry.set_text(data)
