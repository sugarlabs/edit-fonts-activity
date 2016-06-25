
from gi.repository import Gtk, GObject, GLib
from manage_page import ManagerPage

if __name__=="__main__":
    window = Gtk.Window()
    window.set_title('Font List Demo')
    window.connect('destroy', Gtk.main_quit)

    page = ManagerPage(3)
    window.add(page)
    window.show_all()
    Gtk.main()

