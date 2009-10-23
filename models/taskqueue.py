from google.appengine.ext import db
from models.user import User

class TaskQueue(db.Expando):
  time_added = db.DateTimeProperty(auto_now_add=True)
  user = db.ReferenceProperty(User,required=True)
  op_type = db.StringProperty(required=True)