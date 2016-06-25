#!/usr/bin/env python3
import gi
gi.require_version('WebKit', '3.0')

from gi.repository import Gtk, WebKit, GLib, GdkPixbuf

svg = """
<svg height="55px" width="55px">
    <g display="block">
        <polygon display="inline" style="fill:rgb(0,0,255);stroke-width:3.5;stroke:rgb(0,0,0)" points="27.5,7.266 34.074,20.588 48.774,22.723    38.138,33.092 40.647,47.734 27.5,40.82 14.353,47.734 16.862,33.092 6.226,22.723 20.926,20.588" />
    </g>
</svg>

"""

class Window(Gtk.Window):
    def __init__(self):
        super(Window, self).__init__()
        self.connect('delete-event', Gtk.main_quit)

        loader = GdkPixbuf.PixbufLoader()
        loader.write(svg.encode())
        loader.close()  
        pixbuf = loader.get_pixbuf()
        image = Gtk.Image.new_from_pixbuf(pixbuf)

        self.add(image)
        self.show_all()


if __name__ == "__main__":
    Window()
    Gtk.main()