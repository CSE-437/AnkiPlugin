from AnkiHubLibs import webbrowser

from urllib2 import Request, urlopen, URLError, HTTPError
from pprint import pprint
import json
import urllib
import threading
import time

# import the main window object (mw) from ankiqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *
# import the text importer to import text files as decks
from anki.importing import TextImporter

###############################################################
#    Wrapper for QWidget to overwrite closeEvent function.    #
###############################################################
class AnkiWidget(QWidget):
  def __init__(self, AnkiHubInstance, parent=None):
    super(AnkiWidget, self).__init__(parent)
    self.ankiHubInstance = AnkiHubInstance

  def closeEvent(self, event):
    self.ankiHubInstance.terminate()
    super(AnkiWidget, self).closeEvent(event)

###############################################################
#                   Main program for AnkiHub                  #
###############################################################
class AnkiHub:
  '''
  Instance/global variables.
  '''
  url = 'http://ankihub.herokuapp.com'
  username = ''
  sessionToken = ''
  deckCol = []

  '''
  Initial entry point of function. Should be the only function called by global.
  '''
  def initialize(self):
    #TO-DO: Create a destructor to clear data when the QWidget is closed. Currently hacking by manually clearing instance variables.
    self.createLoginWindow()

  '''
  Destructor function to clean data when closing AnkiHub window.
  '''
  def terminate(self):
    self.username = ''
    sessionToken = ''
    self.deckCol = []

  ####################################################################################
  #  GUI setup methods. Creates the QT widget that holds all AnkiHub functionality.  #
  ####################################################################################

  '''
  Creates the login window.
  '''
  def createLoginWindow(self):
    mw.login = QWidget()
    mw.login.resize(500, 250);
    mw.login.setWindowTitle('AnkiHub Login')

    mw.login.instructions = QLabel('Please input your username and password.', mw.login)
    mw.login.instructions.move(30, 30)

    mw.login.usernameLabel = QLabel('Username:', mw.login)
    mw.login.usernameLabel.move(30, 100)
    mw.login.username = QLineEdit(mw.login)
    mw.login.username.resize(300,30)
    mw.login.username.move(150, 100)

    mw.login.passwordLabel = QLabel('Password:', mw.login)
    mw.login.passwordLabel.move(30, 150)
    mw.login.password = QLineEdit(mw.login)
    mw.login.password.setEchoMode(QLineEdit.Password)
    mw.login.password.resize(300,30)
    mw.login.password.move(150, 150)

    mw.login.signup = QPushButton('Register', mw.login)
    mw.login.signup.move(100,200)
    mw.login.signup.clicked.connect(self.connect('signup/'))

    mw.login.submit = QPushButton('Login', mw.login)
    mw.login.submit.move(300,200)
    mw.login.submit.clicked.connect(self.connect('login/'))

    mw.login.show()

  '''
  Creates the deck settings window.
  '''
  def createSettings(self):
    mw.settings = AnkiWidget(self)
    mw.settings.resize(1024, 520)
    mw.settings.setWindowTitle('AnkiHub Settings')

    mw.settings.userLabel = QLabel(self.username + ' - Decks', mw.settings)
    mw.settings.userLabel.move(64, 32)

    self.createTree()

    mw.settings.redirect = QPushButton('Go to AnkiHub', mw.settings)
    mw.settings.redirect.clicked.connect(self.redirect())
    mw.settings.redirect.move(440, 460)

    mw.settings.show()

  '''
  Creates tree view to display deck hierarchy.
  '''
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

  '''
  Helper method to add children to parent decks.
  '''
  def createTreeChildren(self, deckTree, parentDeck, parentNode):
    for child in parentDeck['children']:
      treeNode = QTreeWidgetItem(parentNode)
      treeNode.setText(0, child['name'])
      treeButton = QPushButton('Sync')
      treeButton.clicked.connect(self.syncDeck(child))
      deckTree.setItemWidget(treeNode, 1, treeButton)

      self.createTreeChildren(deckTree, child, treeNode)

  '''
  Creates loading window for visual feedback on data processing.
  '''
  def createLoadingScreen(self):
    mw.loading = QWidget()
    mw.loading.resize(275, 100)
    mw.loading.loadingLabel = QLabel('Loading, please wait...', mw.loading)
    mw.loading.loadingLabel.move(30, 30)

    mw.loading.show()
    mw.loading.repaint()

  '''
  Creates dialog for syncing/uploading decks.
  '''
  def createSyncScreen(self, deckName, syncThread):
    syncLabel = QLabel('Syncing deck "%s", please wait...' % deckName)

    syncLabel.show()
    syncLabel.repaint()

    syncThread.join()

  ###################################################
  #       Callback functions and API calls.         #
  ###################################################

  def uploadTranasactions(self):
    # GET request to ankihub.herokuapp.com/api/decks?name=deckName
    print urllib2.urlopen("http://ankihub.herokuapp.com/api/decks?name=Default").read()
    # Get JSON copy of local deck (processDeck)
    # Pass JSON from request and local copy of deck to transactionCalculator
    # POST request to transations endpoint

  '''
  Callback function for Sync button. Uses multithreading to process POST requests to /api/decks/
  '''
  def syncDeck(self, deck):
    # Temp Call to getTrans
    def syncDeckAction():
      requestURL = self.url + '/api/decks/'
      request = Request(requestURL, json.dumps(deck), {'Content-Type' : 'application/json'})
      syncThread = threading.Thread(target=self.processRequest, args=('Sync', request))
      loadThread = threading.Thread(target=self.createSyncScreen, args=(deck['name'], syncThread))
      try:
        syncThread.start()
        loadThread.start()
      except:
        showInfo('Could not start sync thread')
    return syncDeckAction

  '''
  Callback function to redirect user to AnkiHub.
  '''
  def redirect(self):
    def redirectAction():
      showInfo('Redirecting to AnkiHub')
      webbrowser.open(self.url)
    return redirectAction

  '''
  Callback function that makes POST requests to /api/users/login/ or /api/users/signup/
  '''
  def connect(self, endpoint):
    def connectAction():
      self.createLoadingScreen()

      self.username = mw.login.username.text()
      password = mw.login.password.text()
      loginJson = {'username' : self.username, 'password' : password}

      # Sends POST request for login or signup
      requestURL = self.url + '/api/users/' + endpoint
      req = Request(requestURL, json.dumps(loginJson), {'Content-Type' : 'application/json'})

      try:
        response = urlopen(req)
        jsonResponse = json.loads(response.read())
        mw.login.close()
        self.username = jsonResponse['user']['username']
        self.sessionToken = jsonResponse['user']['sessionToken']
        showInfo('Success! Logged in as ' + jsonResponse['user']['username'])
        self.processDecks()
        mw.loading.close()
        self.createSettings()
      except HTTPError, e:
        showInfo(str('Login Error: %d - %s' % (e.code, json.loads(e.read()))))
      except URLError, e:
        showInfo(str(e.args))
    return connectAction

  '''
  GET request to get decks that a user is subscribed to.
  '''
  def getSubscribeDecks(self, subs):
    for sub in subs:
      requestURL = self.url + '/api/decks/'

      try:
        response = urlopen(requestURL+sub)
        jsonResponse = json.loads(response.read())

        # Uncomment this line to see data in retrieved deck
        #showInfo('Success! Result is ' + str(jsonResponse[0]))
        if len(jsonResponse) > 0:
          self.deckCol.append(jsonResponse[0])    # Adds retrieved deck to internal AnkiHub Deck Collection
      except HTTPError, e:
        showInfo(str('Subscription Download Error: %d - %s' % (e.code, str(json.loads(e.read())))))
      except URLError, e:
        showInfo(str(e.args))

  '''
  Allows for general requests (both GET and POST) to be made asynchronously when used as target for threads. Currently only used for Sync.
  '''
  def processRequest(self, requestFrom, request):
    try:
      response = urlopen(request)
      jsonResponse = json.loads(response.read())
      showInfo('%s Request Successful!' % requestFrom)
    except HTTPError, e:
      showInfo(str('%s Error: %d - %s' % (requestFrom, e.code, e.read())))
    except URLError, e:
      showInfo(str(e.args))

  '''
  CSV to Anki deck importer. If the note type has multiple card types,
  multiple cards will automatically be generated for each note.
  '''
  def importDeck(self):
    file = r"C:\Users\Tyler\Documents\Anki\test.txt"
    # select deck
    did = mw.col.decks.id("ImportDeck")
    model = self.addNewModel()

    mw.col.decks.select(did)
    # set note type for deck
    deck = mw.col.decks.get(did)
    deck['mid'] = model['id']
    mw.col.decks.save(deck)

    # Assign new deck to model
    mw.col.models.setCurrent(model)
    model['did'] = did
    mw.col.models.save(model)

    # import into the collection
    ti = TextImporter(mw.col, file)
    ti.initMapping()
    ti.run()

    mw.col.reset()
    mw.reset()

  '''
  Add new custom note type, card type, and templates (collectively a "model").
  '''
  def addNewModel(self):
    models = mw.col.models # models = note types
    m = models.new("Test")
    fm = models.newField("Foo")
    models.addField(m, fm)
    fm = models.newField("Bar")
    models.addField(m, fm)
    fm = models.newField("Baz")
    models.addField(m, fm)
    t = models.newTemplate("Card 1") # template = card type
    t['qfmt'] = "{{Foo}}" # qfmt = front template
    t['afmt'] = "{{FrontSide}}\n\n<hr id=answer>\n\n{{Bar}}" # afmt = back template
    models.addTemplate(m, t)
    t = models.newTemplate("Card 2")
    t['qfmt'] = "{{Bar}}"
    t['afmt'] = "{{FrontSide}}\n\n<hr id=answer>\n\n{{Baz}}"
    models.addTemplate(m, t)
    models.add(m)
    return m

  #################################################
  #         Algorithms to serialize JSONs.        #
  #################################################

  '''
  Main function to process decks. Gets decks from Anki and creates the overall JSON.
  '''
  def processDecks(self):
    decks = mw.col.decks.all()    #decks from local anki
    deckDict = {}                 #AnkiHub dictionary of processed decks: name -> json object 
    for deckObj in decks:
      if deckObj['name'] not in deckDict:   #if we haven't processed this deck yet
        deckDict[deckObj['name']] = {}      #create a json-object for that deck's name
        self.initializeDeckValues(deckDict[deckObj['name']], deckObj)   #fill empty deck-json with values

      deck = deckDict[deckObj['name']]    #deck is processed, get our json object value
      parents = mw.col.decks.parents(deckObj['id'])   #get list of parents for deck

      if not parents:
        self.deckCol.append(deck)     #no parents, deck is top level, just add to our master deck list
      else:
        if parents[-1]['name'] not in deckDict:   #check if immediate parent is not processed
          deckDict[parents[-1]['name']] = {}      #process immediate parent as above
          self.initializeDeckValues(deckDict[parents[-1]['name']], parents[-1])
        deckDict[parents[-1]['name']]['children'].append(deck)  #add deck-json to parent-json's children list, don't add to master list yet

  '''
  Initializer function to create a deck with the proper fields.
  '''
  def initializeDeckValues(self, deckDict, deck):
    deckDict['sessionToken'] = self.sessionToken
    deckDict['gid'] = '%s:%d' % (self.username, deck['id'])
    deckDict['did'] = deck['id']
    deckDict['description'] = deck['desc']
    deckDict['name'] = deck['name']
    deckDict['keywords'] = []
    deckDict['isPublic'] = True
    deckDict['owner'] = self.username
    deckDict['children'] = []
    deckDict['newCards'] = []
    self.populateCards(deck, deckDict['newCards'])

  '''
  Initializer function to create a card with the proper fields.
  '''
  def populateCards(self, deck, cardList):
    cardIds = mw.col.decks.cids(deck['id'])
    for cardId in cardIds:
      card = mw.col.getCard(cardId)
      cardDict = {}
      cardDict['did'] = str('%s:%d' % (self.username, deck['id']))
      cardDict['cid'] = str(cardId)
      cardDict['front'] = card.q()
      cardDict['back'] = card.a()
      cardDict['notes'] = []
      self.parseNotes(deck['id'], card, cardDict['notes'])
      cardDict['tags'] = []
      self.parseTags(cardId, cardDict['tags'])
      cardDict['keywords'] = []

      cardList.append(cardDict)

  '''
  Helper function to parse the notes of a card.
  '''
  def parseNotes(self, deckId, card, noteList):
    note = card.note()
    '''
    #Tagging experiment, please ignore
    if 'gid' not in note.items():
      tag = '%s:%d' % (self.username, deckId)
      note.addTag(tag)
      #showInfo(note.stringTags())
    note.flush()
    '''
    for item in note.items():
      noteList.append(item)

  '''
  Helper function to parse the tags of a card.
  '''
  def parseTags(self, cardId, tagList):
    query = 'select n.tags from cards c, notes n WHERE c.nid = n.id AND c.id = ?'
    response = mw.col.db.list(query, cardId)
    tags = list(set(mw.col.tags.split(' '.join(response))))
    for tag in tags:
      tagList.append(tag)

#############################################################
#       Anki runs from here and calls our functions.        #
#############################################################
QCoreApplication.setAttribute(Qt.AA_X11InitThreads)
ankiHub = AnkiHub()
action = QAction('AnkiHub', mw)
mw.connect(action, SIGNAL('triggered()'), ankiHub.initialize)
mw.form.menuTools.addAction(action)

action = QAction("AnkiHub Deck Import", mw)
mw.connect(action, SIGNAL("triggered()"), ankiHub.importDeck)
mw.form.menuTools.addAction(action)