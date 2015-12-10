from google.appengine.ext import ndb

class KnjigaGostov(ndb.Model):
    ime_in_priimek = ndb.StringProperty(default = "neznanec")
    email = ndb.StringProperty()
    sporocilo = ndb.TextProperty()
    nastanek = ndb.DateTimeProperty(auto_now_add=True)
    izbrisan = ndb.BooleanProperty(default=False)
