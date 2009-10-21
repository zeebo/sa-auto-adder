from google.appengine.ext import db

class TaskQueue(db.Expando):
  time_added = db.DateTimeProperty(auto_now_add=True)
  user = db.ReferenceProperty(User,required=True)
  op_type = db.StringProperty(required=True)