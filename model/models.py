from google.appengine.ext import db

# Create your models here.
class User(db.Model):
  username = db.StringProperty(required=True)
  password = db.StringProperty(required=True)
  wave_address = db.StringProperty(required=True)
  reg_date = db.DateTimeProperty(auto_now_add=True)
  sa_uid = db.IntegerProperty(required=True)
  last_login = db.DateTimeProperty()
  cookie_token = db.StringProperty()


class WaveletInfo(db.Model):
  wave_id = db.StringProperty(required=True)
  users_added = db.StringListProperty()
  wavelet_id = db.StringProperty(required=True)
  admin = db.ReferenceProperty(User,required=True)