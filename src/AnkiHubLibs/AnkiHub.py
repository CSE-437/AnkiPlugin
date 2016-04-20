import urllib2
import urllib
import Cookie
import pickle
import json

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
    def __init__(self, configDict, cookie = Cookie.SimpleCookie()):
        self.cookie = cookie
        self.configDict = configDict
        me = self.whoami()
        if me.get('sessionToken') and me.get('username'):
            self.username= me['username']
            self.sessionToken = me['sessionToken']

    def terminate(self):
        self.username = ''
        self.sessionToken = ''
        pickle.dump(self.configDict, open(configFileName, "wb+"))
        pickle.dump(self.cookie, open(cookieFileName, "wb+"))

    def uploadDeck(self, deckJson):
        data_encoded = urllib.urlencode(deckJson)
        req = urllib2.Request('%s/api/decks'%(self.url))
        req.add_header('cookie', self.cookie)
        urllib2.urlopen(req, data_encoded)

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
