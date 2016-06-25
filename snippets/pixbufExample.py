import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')

from gi.repository import Gtk, WebKit, GLib, GdkPixbuf


svg = """
<svg height="55px" width="55px">
    <g display="block">
        <polygon display="inline" style="fill:rgb(0,0,255);stroke-width:3.5;stroke:rgb(0,0,0)" points="27.5,7.266 34.074,20.588 48.774,22.723    38.138,33.092 40.647,47.734 27.5,40.82 14.353,47.734 16.862,33.092 6.226,22.723 20.926,20.588" />
    </g>
</svg>

"""

class CellRendererPixbufWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="CellRendererPixbuf Example")

        self.set_default_size(200, 200)

        self.liststore = Gtk.ListStore(str, str)
        self.liststore.append(["New", "document-new"])
        self.liststore.append(["Open", "document-open"])
        self.liststore.append(["Save", "document-save"])

        treeview = Gtk.TreeView(model=self.liststore)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Text", renderer_text, text=0)
        treeview.append_column(column_text)

        renderer_pixbuf = Gtk.CellRendererPixbuf()

        loader = GdkPixbuf.PixbufLoader()
        loader.write(svg.encode())
        loader.close()  
        renderer_pixbuf.props.pixbuf = loader.get_pixbuf()
        column_pixbuf = Gtk.TreeViewColumn("Image", renderer_pixbuf)
        treeview.append_column(column_pixbuf)

        self.add(treeview)

win = CellRendererPixbufWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()