from AnkiHubLibs import webbrowser

from urllib2 import Request, urlopen, URLError
from pprint import pprint
import json

# import the main window object (mw) from ankiqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *

class AnkiHub:

  #myurl = 'http://localhost:5000/api/user/user.json'
  myurl = 'http://jsonplaceholder.typicode.com'
  ankiHubURL = 'localhost:3000'

  reponseJson = []
  decks = {}

  def userApiTest(self):
    request = Request(self.myurl + '/users')
    
    try:
      response = urlopen(request)
      user = json.loads(response.read())
      pprint(user)
    except URLError, e:
      print 'sadness shit sucks', e
    
    self.responseJson = user
    self.createSettings()
    
  def createSettings(self):
    mw.settings = QWidget()
    mw.settings.resize(560, 320)
    mw.settings.setWindowTitle("AnkiHub")
    
    mw.settings.userLabel = QLabel(self.responseJson[0]['name'] + ' - Decks', mw.settings)
    mw.settings.userLabel.move(64, 32)
    
    self.createTable()
    
    mw.settings.redirect = QPushButton('Go to AnkiHub', mw.settings)
    mw.settings.redirect.clicked.connect(self.redirect())
    mw.settings.redirect.move(200, 265)
    
    mw.settings.show()
    
  def createTable(self):
    mw.settings.deckTable = QTableWidget(mw.settings)
    deckTable = mw.settings.deckTable
    deckTable.resize(432, 192)
    deckTable.move(64, 64)
    deckTable.setRowCount(len(self.responseJson))
    deckTable.setColumnCount(2)
    deckTable.verticalHeader().setVisible(False)
    deckTable.horizontalHeader().setVisible(False)
    deckTable.horizontalHeader().setResizeMode(0, QHeaderView.Stretch)
    
    for i in range(len(self.responseJson)):
      pWidget = QWidget()
      pButton = QPushButton()
      pButton.setText('Sync')
      pButton.clicked.connect(self.syncDeck(i))
      pLayout = QHBoxLayout(pWidget)
      pLayout.addWidget(pButton)
      pLayout.setAlignment(Qt.AlignCenter)
      pLayout.setContentsMargins(0,0,0,0)
      pWidget.setLayout(pLayout)
      
      deckTable.setItem(i, 0, QTableWidgetItem(self.responseJson[i]['name']))
      deckTable.setCellWidget(i, 1, pWidget)
      
  def syncDeck(self, index):
    def syncDeckAction():
      showInfo('User: %s' % self.responseJson[index]['name'])
    return syncDeckAction
    
  def redirect(self):
    def redirectAction():
      showInfo('Redirecting to AnkiHub')
      webbrowser.open('http://corgiorgy.com/')
    return redirectAction
    
  def sendDecks(self, decks):
    #crashes
    #requests.post(myurl+'/api/deck', data=json.dumps(decks))
    print('blah')
  
  def uploadDecks(self):
    #ids = mw.col.db.all("select did from cards")
    #showInfo("IDS: %s" % ids[1:10])
    ids = mw.col.findCards("")
    for id in ids[1:3]:
        if not id in self.decks:
            decks[id] = []
        self.decks[id].append(mw.col.getCard(id))
    self.sendDecks(self.decks)
    #showInfo(str([method for method in dir(mw) if callable(getattr(mw, method))]))
    
ankiHub = AnkiHub()
action = QAction('AnkiHub', mw)
# uncomment the function to test
mw.connect(action, SIGNAL('triggered()'), ankiHub.userApiTest)
#mw.connect(action, SIGNAL('triggered()'), ankiHub.uploadDecks)
mw.form.menuTools.addAction(action)