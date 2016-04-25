import urllib2
import urllib
import Cookie
#import pickle
import json
import datetime

configFileName = "ankiHubSettings.p"
cookieFileName = "ankiHubCookies.p"
class AnkiHubServer:
    '''
    Initialize Global Variables
    '''
    url = 'http://ankihub.herokuapp.com'
    username = ''
    sessionToken = ''
    configDict = dict()
    cookie = None
    #logFile = None
    def __init__(self, configDict, cookie = Cookie.SimpleCookie()):
        self.cookie = cookie
        self.configDict = configDict
        me = self.whoami()
        #logFile = open('AnkiHubLog.txt', "a+")
        if me.get('sessionToken') and me.get('username'):
            self.username= me['username']
            self.sessionToken = me['sessionToken']

    def log(self, str):
        #logFile.write("[%s]: %s"%(datetime.datetime.now(), str))
        pass
    def terminate(self):
        self.username = ''
        self.sessionToken = ''
        #self.logFile.close()
        #pickle.dump(self.configDict, open(configFileName, "wb+"))
        #pickle.dump(self.cookie, open(cookieFileName, "wb+"))

    def uploadDeck(self, deckJson):
        req = urllib2.Request('%s/api/decks'%(self.url))
        req.add_header('cookie', self.cookie)
        self.log(str(urllib2.urlopen(req, deckJson).read()))
        
    def getDeck(self, gid):
      req = urllib2.Request('%s/api/decks/%s' %(self.url,gid))
      req.add_header('cookie', self.cookie)
      return json.loads(urllib2.urlopen(req).read())

    def getTransactions(self, gid):
        req = urllib2.Request('%s/api/decks/%s/transactions' %(self.url,gid))
        req.add_header('cookie', self.cookie)
        return json.loads(urllib2.urlopen(req).read())

    def postTransactions(self, gid, transactions):
        data_encoded = urllib.urlencode(transactions)
        req = urllib2.Request('%s/api/decks/%s'%(self.url, gid))
        req.add_header('cookie', self.cookie)
        return json.loads(urllib2.urlopen(req, data_encoded).read())

    def login(self, username, password):
        data = {"username": username, "password": password}
        data_encoded = urllib.urlencode(data)
        req = urllib2.Request('%s/api/users/login'%self.url)
        response = urllib2.urlopen(req, data_encoded)
        self.cookie = response.headers.get('Set-Cookie')
        body = json.loads(response.read())
        self.username = body['user']['username']
        self.sessionToken = body['user']['sessionToken']
        self.configDict['user'] = body['user']
        return body

    def signup(self, username, password):
        data = {"username": username, "password": password}
        data_encoded = urllib.urlencode(data)
        req = urllib2.Request('%s/api/users/signup'%self.url)
        response = urllib2.urlopen(req, data_encoded)
        self.cookie = response.headers.get('Set-Cookie')
        body = json.loads(response.read())
        self.username = body['user']['username']
        self.sessionToken = body['user']['sessionToken']
        self.configDict['user'] = body['user']
        return body

    def hasUser(self):
        return (self.configDict.get('user') is not None)

    def getMySubscriptions(self):
        if self.hasUser():
            return self.configDict['user']['subscriptions']
        else:
            return list()
    def getMyDecks(self):
        if self.hasUser():
            return self.configDict['user']['decks']
        else:
            return list()

    def whoami(self):
        req = urllib2.Request('%s/api/users/whoami'%self.url)
        req.add_header('cookie', self.cookie)
        return json.loads(urllib2.urlopen(req).read())

    def getSubscribedDecks(self, subs):
        decks = []
        for sub in subs:
            req = urllib2.Request('%s/api/decks/%s'%(self.url, sub))
            req.add_header('cookie', self.cookie)
            jsonResponse = json.loads(urllib2.urlopen(req).read())
            if isinstance(jsonResponse, list) and len(jsonResponse) != 0:
                 decks.append(jsonResponse[0])

        return decks
        '''
      Allows for general requests (both GET and POST) to be made asynchronously when used as target for threads. Currently only used for Sync.
      '''
    def recursiveSync(self, requestFrom, deck):
        deckCopy = deck.copy()
        deckCopy['children'] = []

        #to ignore all children, comment out the following for-loop
        #for childDeck in deck['children']:
        #    childResponse = self.recursiveSync(requestFrom, childDeck)
        #    deckCopy['children'].append(childResponse['gid'])

        data_encoded = json.dumps(deckCopy)
        req = urllib2.Request('%s/api/decks'%self.url)
        req.add_header('cookie', self.cookie)
        req.add_header('content-type', 'application/json')
        response = urllib2.urlopen(req, data_encoded)
        return json.loads(response.read())
