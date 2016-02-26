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
  deckCol = []

  '''
  Initial entry point of function. Should be the only function called by global.
  '''
  def initialize(self):
    #TO-DO: Create a destructor to clear data when the QWidget is closed. Currently hacking by manually clearing instance variables.
    self.responseJson = []
    self.deckCol = []
  
    self.processDecks()
    deckJson = json.dumps(self.deckCol)
    #showInfo(str(self.deckCol))
    showInfo(deckJson)
    request = Request(self.myurl + '/users')
    
    try:
      response = urlopen(request)
      user = json.loads(response.read())
      pprint(user)
    except URLError, e:
      print 'sadness shit sucks', e
    
    self.responseJson = user
    self.createSettings()
    
  '''
  GUI setup methods. Creates the QT widget that holds all AnkiHub functionality.
  '''
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
  
  '''
  Callback functions and API calls.
  '''
  def syncDeck(self, index):
    def syncDeckAction():
      showInfo('User: %s' % self.responseJson[index]['name'])
    return syncDeckAction
    
  def redirect(self):
    def redirectAction():
      showInfo('Redirecting to AnkiHub')
      webbrowser.open('http://corgiorgy.com/')
    return redirectAction
    
  '''
  David functions.
  '''
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
    
  '''
  Algorithms to serialize JSONs.
  '''
  def processDecks(self):
    decks = mw.col.decks.all()
    deckDict = {}
    for deckObj in decks:
      if deckObj['name'] not in deckDict:
        deckDict[deckObj['name']] = {}
        self.initializeDeckValues(deckDict[deckObj['name']], deckObj)
      
      deck = deckDict[deckObj['name']]
      parents = mw.col.decks.parents(deckObj['id'])
      
      if not parents:
        self.deckCol.append(deck)
      else:
        if parents[-1]['name'] not in deckDict:
          deckDict[parents[-1]['name']] = {}
          self.initializeDeckValues(deckDict[parents[-1]['name']], parents[-1])
        
        #TO-DO: Make this not a shitty linear time search. You can do this by making the lists into sets and creating a hashable object
        #       that consists of a string (the name) and a dictionary and have it hash on the string. Also do this on the other search below.
        #       pls do this aarthi ty.
        if not any(child['name'] == deck['name'] for child in deckDict[parents[-1]['name']]['children']):
          deckDict[parents[-1]['name']]['children'].append(deck)
      
      for i in range(1, len(parents)+1):
        if parents[-i]['name'] not in deckDict:
          deckDict[parents[-i]['name']] = {}
          self.initializeDeckValues(deckDict[parents[-i]['name']], parents[-i])
        
        if not any(child['name'] == deck['name'] for child in deckDict[parents[-i]['name']]['children']):
          deckDict[parents[-i]['name']]['children'].append(deckDict[parents[-(i-1)]['name']])
  
  def initializeDeckValues(self, deckDict, deck):
    #deckDict['desc'] = deck['desc']
    deckDict['name'] = deck['name']
    #deckDict['owner'] = 42  #TO-DO: change this to actual owner
    #deckDict['session-token'] = 'chocolate rain'  #TO-DO: replace with actual session token
    deckDict['children'] = []
    deckDict['cards'] = []
    self.populateCards(deck, deckDict['cards'])
    
  def populateCards(self, deck, cardList):
    cardIds = mw.col.decks.cids(deck['id'])
    for cardId in cardIds:
      card = mw.col.getCard(cardId)
      cardDict = {}
      cardDict['front'] = card.q()
      cardDict['back'] = card.a()
      #cardDict['tags']                        TO-DO: Aarthi figure out how to get tags ty
      #cardDict['notes'] = card.note()         TO-DO: make notes JSON serializable
      cardDict['owner'] = 42
      cardDict['did'] = '%d:%d' % (42, deck['id'])
      
      cardList.append(cardDict)

'''
Anki runs from here and calls our functions.
'''      
ankiHub = AnkiHub()
action = QAction('AnkiHub', mw)
# uncomment the function to test
mw.connect(action, SIGNAL('triggered()'), ankiHub.initialize)
#mw.connect(action, SIGNAL('triggered()'), ankiHub.uploadDecks)
mw.form.menuTools.addAction(action)