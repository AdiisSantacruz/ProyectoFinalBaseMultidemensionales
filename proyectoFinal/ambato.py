import couchdb  # Libreria de CouchDB (requiere ser instalada primero)
from tweepy import \
    Stream  # tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json  # Libreria para manejar archivos JSON

###Credenciales de la cuenta de Twitter########################
ckey = "unksC6a2wXM5JoZ5cFwqxD8F6"
csecret = "EJiqOoTUSQIPNLQpTgJnDFk6IJsjpt7EzeD7sgBGOGl43HCWm0"
atoken = "999027538243588098-gAoMQKa1Na0YSvHB3g5Q9558jXCMSgQ"
asecret = "UcQU3N0SibSMRHbekjYjG1eBjuwaqPJpnKYMfspiQZ6jN"
#####################################

class listener(StreamListener):

    def on_data(self, data):
        dictTweet = json.loads(data)
        try:
            dictTweet["_id"] = str(dictTweet['id'])
            # Antes de guardar el documento puedes realizar parseo, limpieza y cierto analisis o filtrado de datos previo
            # a guardar en documento en la base de datos
            doc = db.save(dictTweet)  # Aqui se guarda el tweet en la base de couchDB
            print
            "Guardado " + "=> " + dictTweet["_id"]
        except:
            print
            "Documento ya existe"
            pass
        return True

    def on_error(self, status):
        print
        status


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

# Setear la URL del servidor de couchDB
server = couchdb.Server('http://localhost:5984/')
try:
    # Si no existe la Base de datos la crea
    db = server.create('ambato')
except:
    # Caso contrario solo conectarse a la base existente
    db = server['ambato']

# Aqui se define el bounding box con los limites geograficos donde recolectar los tweets
twitterStream.filter(track=["ambato","Luis Amoroso","#LuisAmoroso","Fernando Naranjo","#FernandoNaranjo","Javier Altamirano", "#JavierAltamirano", "Maria Fernanda Naranjo","#MariaFernandaNaranjo","Salome Marin","#SalomeMarin","elecciones de alcaldia ambato"])
twitterStream.filter(locations=[-78.937982,-1.470916,-78.5368,-1.1098])


