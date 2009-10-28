from modules.appengine_utilities import sessions
import logging

def updates_session(method):
  def new_method(self, *args, **kwargs):
    return_value = method(self, *args, **kwargs)
    self.update_session()
    return return_value
  return new_method


class RequestObject(object):
  
  def __new__(cls, *args, **kwargs):
    session = sessions.Session()
    
    if cls.__name__ not in session:
      return super(cls.__class__, cls).__new__(cls, *args, **kwargs)
    return session[cls.__name__]

  def __init__(self):
    session = sessions.Session()
    if self.__class__.__name__ not in session:
      #logging.error("Created a %s object" % self.__class__.__name__)
      self.__error = []
      self.do_init()
    session[self.__class__.__name__] = self

  def do_init(self):
    pass
  
  def update_session(self):
    session = sessions.Session()
    session[self.__class__.__name__] = self

  @property
  @updates_session
  def error(self):
    try:
      return str(self.__error.pop()) + " PANIC!"
    except IndexError:
      return None
      
  @property
  @updates_session
  def errors(self):
    temp, self.__error = self.__error, []
    return temp

  @updates_session
  def add_error(self, message):
    self.__error.append(message)