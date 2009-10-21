from google.appengine.ext import db

class WaveletInfo(db.Model):
  wave_id = db.StringProperty(required=True)
  users_added = db.StringListProperty()
  wavelet_id = db.StringProperty(required=True)
  admin = db.ReferenceProperty(User,required=True)
  title = db.StringProperty()
  root_blip = db.StringProperty()