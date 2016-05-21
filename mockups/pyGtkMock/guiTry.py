import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from defcon import Font


class FlowBoxWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Character Map Demo")
        self.set_border_width(10)
        self.set_default_size(800, 800)

        header = Gtk.HeaderBar(title="Character Map")
        header.set_subtitle("Sample Character Map app")
        header.props.show_close_button = True

        self.set_titlebar(header)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        flowbox = Gtk.FlowBox()
        flowbox.set_valign(Gtk.Align.START)
        flowbox.set_max_children_per_line(30)
        flowbox.set_selection_mode(Gtk.SelectionMode.NONE)

        self.create_flowbox(flowbox)

        scrolled.add(flowbox)

        self.add(scrolled)
        self.show_all()

    def glyph_box_new(self, str_name):
        
        button = Gtk.Button(label=str_name)

        #draw the glyph in the box 
        
        #area = Gtk.DrawingArea()
        #area.set_size_request(50, 50)
        #button.add(area)

        #set button size
        button.set_size_request(100,100)

        return button

    def create_flowbox(self, flowbox):

        #load the font
        path = "sample"
        font = Font(path)
        #print(len(font));

        for glyph in font:
            #just trying out some stuff on the glyphs
            #print(glyph.representationKeys());
            
            button = self.glyph_box_new("Name: " + glyph.name + "\n" + "Unicode: " + str(glyph.unicode) )
            flowbox.add(button)
                        

win = FlowBoxWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
