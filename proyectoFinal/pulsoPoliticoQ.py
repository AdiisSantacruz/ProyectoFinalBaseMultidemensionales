import couchdb
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json


ckey = "unksC6a2wXM5JoZ5cFwqxD8F6"
csecret = "EJiqOoTUSQIPNLQpTgJnDFk6IJsjpt7EzeD7sgBGOGl43HCWm0"
atoken = "999027538243588098-gAoMQKa1Na0YSvHB3g5Q9558jXCMSgQ"
asecret = "UcQU3N0SibSMRHbekjYjG1eBjuwaqPJpnKYMfspiQZ6jN"


class listener(StreamListener):

    def on_data(self, data):
        dictTweet = json.loads(data)
        try:
            dictTweet["_id"] = str(dictTweet['id'])
            doc = db.save(dictTweet)
            print("Guardado " + "=> " + dictTweet["_id"])
        except:
            print("Documento ya existe")
            pass
        return True

    def on_error(self, status):
        print(status)


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())


server = couchdb.Server('http://localhost:5984/')
try:
    db = server.create('pulsoPQuito')
except:
    db = server['pulsoPQuito']


twitterStream.filter(track=["Paco Moncayo ", "#PacoMoncayo", "Izquierda Democratica"])
# twitterStream.filter(locations=[-78.586922,-0.395161,-78.274155,0.021973])
