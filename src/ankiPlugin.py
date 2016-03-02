from AnkiHubLibs import webbrowser

from urllib2 import Request, urlopen, URLError, HTTPError
from pprint import pprint
import json
import urllib

# import the main window object (mw) from ankiqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *

class AnkiHub:

  url = 'http://ankihub.herokuapp.com'
  username = ''
  deckCol = []

  '''
  Initial entry point of function. Should be the only function called by global.
  '''
  def initialize(self):
    #TO-DO: Create a destructor to clear data when the QWidget is closed. Currently hacking by manually clearing instance variables.
    self.username = ''
    self.deckCol = []
  
    self.login()
    self.processDecks()

    self.createSettings()
    
  '''
  GUI setup methods. Creates the QT widget that holds all AnkiHub functionality.
  '''
  def createSettings(self):
    mw.settings = QWidget()
    mw.settings.resize(1024, 520)
    mw.settings.setWindowTitle("AnkiHub")
    
    mw.settings.userLabel = QLabel(self.username + ' - Decks', mw.settings)
    mw.settings.userLabel.move(64, 32)
    
    #self.createTable()
    self.createTree()
    
    mw.settings.redirect = QPushButton('Go to AnkiHub', mw.settings)
    mw.settings.redirect.clicked.connect(self.redirect())
    mw.settings.redirect.move(440, 460)
    
    mw.settings.show()
      
  def createTree(self):
    mw.settings.deckTree = QTreeWidget(mw.settings)
    deckTree = mw.settings.deckTree
    deckTree.resize(896, 384)
    deckTree.move(64, 64)
    
    header = QTreeWidgetItem(['Decks', ''])
    deckTree.setHeaderItem(header)
    deckTree.setColumnWidth(0,750)
    
    for rootDeck in self.deckCol:
      treeNode = QTreeWidgetItem(deckTree)
      treeNode.setText(0, rootDeck['name'])
      treeButton = QPushButton('Sync')
      treeButton.clicked.connect(self.syncDeck(rootDeck))
      deckTree.setItemWidget(treeNode, 1, treeButton)
      
      self.createTreeChildren(deckTree, rootDeck, treeNode)

  def createTreeChildren(self, deckTree, parentDeck, parentNode):
    for child in parentDeck['children']:
      treeNode = QTreeWidgetItem(parentNode)
      treeNode.setText(0, child['name'])
      treeButton = QPushButton('Sync')
      treeButton.clicked.connect(self.syncDeck(child))
      deckTree.setItemWidget(treeNode, 1, treeButton)
      
      self.createTreeChildren(deckTree, child, treeNode)
  
  '''
  Callback functions and API calls.
  '''    
  def syncDeck(self, deck):
    def syncDeckAction():
      showInfo(str(deck))
      requestURL = self.url + '/api/decks/'
      req = Request(requestURL, json.dumps(deck), {'Content-Type' : 'application/json'})
      
      try:
        response = urlopen(req)
        showInfo(response.read())
      except HTTPError, e:
        showInfo(str('Sync Error: %d' % e.code))
      except URLError, e:
        showInfo(str(e.args))
    return syncDeckAction
    
  def redirect(self):
    def redirectAction():
      showInfo('Redirecting to AnkiHub')
      webbrowser.open(self.url)
    return redirectAction
    
  def login(self):
    loginJson = {'username' : 'fluffluff', 'password' : 'password'}
    requestURL = self.url + '/api/users/login/'
    req = Request(requestURL, json.dumps(loginJson), {'Content-Type' : 'application/json'})
    
    try:
      response = urlopen(req)
      jsonResponse = json.loads(response.read())
      self.username = jsonResponse['user']['username']
    except HTTPError, e:
      showInfo(str('Login Error: %d' % e.code))
    except URLError, e:
      showInfo(str(e.args))
    
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
        #       that consists of a string (the name) and a dictionary and have it hash on the string.
        #       pls do this aarthi ty.
        if not any(child['name'] == deck['name'] for child in deckDict[parents[-1]['name']]['children']):
          deckDict[parents[-1]['name']]['children'].append(deck)
  
  def initializeDeckValues(self, deckDict, deck):
    deckDict['did'] = deck['id']
    deckDict['description'] = deck['desc']
    deckDict['name'] = deck['name']
    deckDict['keywords'] = ''
    deckDict['ispublic'] = True
    deckDict['owner'] = 'fluffluff'  #TO-DO: change this to actual owner
    deckDict['children'] = []
    deckDict['newCards'] = []
    self.populateCards(deck, deckDict['newCards'])
    
  def populateCards(self, deck, cardList):
    cardIds = mw.col.decks.cids(deck['id'])
    for cardId in cardIds:
      card = mw.col.getCard(cardId)
      cardDict = {}
      cardDict['cid'] = cardId
      cardDict['front'] = card.q()
      cardDict['back'] = card.a()
      cardDict['tags'] = []                        #TO-DO: Aarthi figure out how to get tags ty
      cardDict['notes'] = []                       #card.note()   #TO-DO: make notes JSON serializable
      cardDict['keywords'] = []
      
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