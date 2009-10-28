from google.appengine.ext import db
from models.user import User

class Event(db.Model):
  time_added = db.DateTimeProperty(auto_now_add=True)
  user = db.ReferenceProperty(User,required=True)
  event_text = db.StringProperty(required=True)