from appengine_django.models import BaseModel
from google.appengine.ext import db

# Create your models here.
class Poll(BaseModel):
    question = db.StringProperty()
    pub_date = db.DateTimeProperty('date published')

class Choice(BaseModel):
    poll = db.ReferenceProperty(Poll)
    choice = db.StringProperty()
    votes = db.IntegerProperty()