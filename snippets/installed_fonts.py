import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from gi.repository import Pango

o = Gtk.Box()
context = o.get_pango_context()

fonts_list = []

for family in context.list_families():
    name = family.get_name()
    fonts_list.append(name)
    print name

print len(fonts_list)
