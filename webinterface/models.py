from appengine_django.models import BaseModel
from google.appengine.ext import db

# Create your models here.
class User(db.Model):
  username = db.StringProperty(required=True)
  password = db.StringProperty(required=True)
  wave_address = db.StringProperty(required=True)
  reg_date = db.DateTimeProperty(auto_now_add=True)
  last_login = db.DateTimeProperty()
  cookie_token = db.StringProperty()
