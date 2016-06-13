from gi.repository import Gtk, Gdk
from defcon import Font
from sugar3.activity import activity
from defconGTK.summaryPage import SummaryPage
from defconGTK.editorPage import EditorPage

PAGE_NAME= ["Manager","Summary","Create","Editor"]

class PageManager(Gtk.Notebook):

    def __init__(self, font=None, tabview=False):
        super(PageManager, self).__init__()
        self.font = font
        if not tabview:
            self.set_show_tabs(False)

        if font:
            #go to the font info page
            self.append_page(SummaryPage(self,self.font),Gtk.Label('Font Summary'))
            #self.append_page(Gtk.Box(),Gtk.Label('Font Info'))
              
        else:
            #go to the create new font page
            #self.append_page(CreateNewFont(),Gtk.Label('Create New Font'))  
            self.append_page(Gtk.Box(),Gtk.Label('Create New Font'))  
            
    def startEditor(glyphName = 'A'):        
        #start the Editor View
        n = PAGE_NAME.index("Editor")
        self.remove_page(n)
        self.insert_page(EditorPage(self,self.font,glyphName),Gtk.Label('Editor View'),n)
        self.set_current_page(n)


PAGE_MANAGER = PageManager()

"""
#I am trying a to make a singleton class to manage all the pages of the application

def singleton(MyClass):
    instances = {}
    def getInstance(*args, **kwargs):
        if myClass not in instances:
            instances[MyClass] = myClass(*args,**kwargs)
        return instances[myClass]
    return getInstance

class PageManagerInstance(PageManager):
    __metaclass__ = Singleton
    
    def __init__(self, font=None, tabview=False):
        super(MyClass,self).__init__(font=None, tabview=False)
"""

