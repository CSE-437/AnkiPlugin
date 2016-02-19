#import main window object (mw) from ankiqt
from aqt import mw
#import show info
from aqt.utils import showInfo
#import all of the Qt GUI library
from aqt.qt import *

#We're going to add a menu item below. First we want to create a function
#to be called when the menu item is activated.

def testFunction():
    # get the number of cards in the current collections, whith is stored in
    # the main window
    cardCount = mw.col.cardCount()
    #show a message box
    showInfo("Card count: %d" %cardCount)

#create a new menu item, "test"
action = QAction("test", mw)
#set action to call test function when it is clicked.
mw.connect(action, SIGNAL("triggered()"), testFunction)
#and add it to the tools menu
mw.form.menuTools.addAction(action)
