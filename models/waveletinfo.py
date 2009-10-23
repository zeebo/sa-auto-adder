from google.appengine.ext import db
from models.user import User

class WaveletInfo(db.Model):
  wave_id = db.StringProperty(required=True)
  users_added = db.StringListProperty()
  wavelet_id = db.StringProperty(required=True)
  admin = db.ReferenceProperty(User, required=True)
  visible = db.BooleanProperty(default=False)
  short_url = db.StringProperty()
  title = db.StringProperty()
  root_blip = db.StringProperty()