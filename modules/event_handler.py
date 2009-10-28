from modules.request_object import RequestObject
from models.user import User
from models.event import Event
from google.appengine.ext import db
import hashlib, random
import logging

class EventHandler(RequestObject):
  def do_init(self):
    pass
    
  def get_event_from_key(self, key):
    event = db.get(db.Key(key))
    if event is None:
      raise Exception, 'event not found'
    return event
  
  def get_events(self, for_user):
    query = db.Query(Event)
    query.filter('user', for_user)
    return list(query)
  
  def delete_event(self, for_user, key):
    event = self.get_event_from_key(key)
    
    if event.user.key() != for_user.key():
      raise Exception, 'can\'t delete that event'
    
    event.delete()