from urllib2 import Request, urlopen, URLError
from pprint import pprint
import json
import requests

# import the main window object (mw) from ankiqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *

#myurl = 'http://localhost:5000/api/user/user.json'
myurl = 'http://jsonplaceholder.typicode.com'

def userApiTest():
  request = Request(myurl + '/users')

  try:
    response = urlopen(request)
    user = json.loads(response.read())
    pprint(user)
  except URLError, e:
    print 'sadness shit sucks', e

  showInfo("User: %s" % user[0]['name'])
  createSettings()

ankiHubURL = 'localhost:3000'
def sendDecks(decks):
#crashes
  requests.post(myurl+'/api/deck', data=json.dumps(decks))

def createSettings():
  mw.settings = QWidget()
  mw.settings.resize(560, 320)
  mw.settings.setWindowTitle("Hello World")
  mw.settings.show()

decks = {}

def uploadDecks():
    #ids = mw.col.db.all("select did from cards")
    #showInfo("IDS: %s" % ids[1:10])
    ids = mw.col.findCards("")
    for id in ids[1:3]:
        if not id in decks:
            decks[id] = []
        decks[id].append(mw.col.getCard(id))
    sendDecks(decks)
    #showInfo(str([method for method in dir(mw) if callable(getattr(mw, method))]))


action = QAction('user', mw)
mw.connect(action, SIGNAL('triggered()'), uploadDecks)
mw.form.menuTools.addAction(action)
#userApiTest()
