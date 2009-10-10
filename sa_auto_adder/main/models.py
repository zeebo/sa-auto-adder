from google.appengine.ext import db

class User(db.Model):
  username = db.StringProperty(required=True)
  password = db.StringProperty(required=True)
  reg_date = db.DateTimeProperty(auto_now_add=True)