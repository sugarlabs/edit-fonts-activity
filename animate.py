import sys
import pygtk
pygtk.require('2.0')

from gi.repository import  Clutter

Clutter.init(sys.argv)

stage = Clutter.Stage()

stage_color = Clutter.Color(0, 0, 0, 255)
actor_color = Clutter.Color(255, 255, 255, 99)

stage.set_size(200, 200)
stage.set_color(stage_color)

rect = Clutter.Rectangle.new_with_color(actor_color)
rect.set_size(40, 40)
rect.set_position(10, 10)
stage.add_actor(rect)
rect.show()

stage.show()

def on_alpha(alpha, data):
    timeline = alpha.get_timeline()
    return timeline.get_progress()

timeline = Clutter.Timeline.new(5000)
timeline.set_loop(True)
timeline.start()

#import pdb; pdb.set_trace()
alpha = Clutter.Alpha()
alpha.set_timeline(timeline)
alpha.set_func(on_alpha, None, None)
animation = rect.animate_with_alphav(alpha, 3,
                                     ["x", 150, "y", 150, "opacity", 0])

Clutter.main()