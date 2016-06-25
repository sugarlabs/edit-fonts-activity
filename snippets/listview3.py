#!/usr/bin/env python

import gobject
import time  # This is just used for slowing down the threads
import os
import threading
import gtk


class FileBrowser:

    def __init__(self):
        self.window = gtk.Window()
        self.window.show_all()
        self.window.connect("destroy", self._destroy)

        box = gtk.VBox()
        box.show()

        self.scrolled_w = gtk.ScrolledWindow()
        self.scrolled_w.show()
        self.window.add(box)

        self.status = gtk.Label("...")  # I added a status label to see when scan is done
        self.status.show()
        box.pack_start(self.status, False, False, 2)

        self.button = gtk.Button("start")
        self.button.show()
        self.button.connect("clicked",self.start_scanning)
        self.button.set_size_request(30,50)
        box.pack_start(self.button,False,False,4)

        self.model=gtk.TreeStore(str)
        self.treeview = gtk.TreeView(self.model)
        self.treeview.show()

        col = gtk.TreeViewColumn("FileName")
        cell = gtk.CellRendererText()

        self.treeview.append_column(col)
        col.pack_start(cell,0)
        col.set_attributes(cell,text=0)

        box.pack_start(self.scrolled_w,10)
        self.scrolled_w.add(self.treeview)
        self.window.set_size_request(600,300)

        self.threads = list()  # I made this be part of the full application
        """ That allows us to wait for all threads on close-down, don't know how
        necessary it is."""

    def start_scanning(self,w):

        self.button.set_sensitive(False)  # To disallow stacking scan-stats
        self.status.set_text("Scanning...")  # Let user know it is started
        self.model.clear()
        main_dir= os.path.expanduser("~")  # I just wanted my home-dir instead
        list_dir = os.listdir(main_dir)
        no_of_threads = len(list_dir)
        for i in range(no_of_threads):
            t = threading.Thread(target=self._thread_scanning,args=(main_dir,list_dir[i],))
            self.threads.append(t)
            t.start()

        gobject.timeout_add(200, self._callback)  # This will cause the main app to
        #check every 200 ms if the threads are done.

    def _callback(self):

        if threading.active_count() == 1:  # If only one left, scanning is done
            self.status.set_text("Done!")
            self.button.set_sensitive(True)  # Allow button being pressed again
            return False  # False make callback stop

        print threading.active_count()
        return True

    def _thread_scanning(self,main_d,list_d):
        path = os.sep.join((main_d, list_d))  # Made use of os's sep instead...
        if os.path.isdir(path):
            list_subd = os.listdir(path)
            par = self.model.append(None,[list_d])
            for sub in list_subd:
                self.model.append(par,[sub])

        time.sleep(3)  # Useless other than to delay finish of thread.

    def main(self):

        gtk.main()


    def _destroy(self, *args, **kwargs):

        #Own destroy that waits for all threads...
        for t in self.threads:
            t.join()

        gtk.main_quit(*args, **kwargs)

if __name__=="__main__":
    gobject.threads_init()
    fb=FileBrowser()
    fb.main()