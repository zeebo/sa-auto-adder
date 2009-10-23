from modules.request_object import RequestObject
from models.user import User
from models.waveletinfo import WaveletInfo
from models.taskqueue import TaskQueue
from google.appengine.ext import db
import hashlib, random
import logging

class WaveletHandler(RequestObject):
  def do_init(self):
    pass
  
  @property
  def visible_wavelets(self):
    query = db.Query(WaveletInfo)
    query.filter('visible =', True)
    return query