from modules.appengine_utilities import sessions
import logging

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

  @property
  def error(self):
    try:
      return self.__error.pop()
    except IndexError:
      return None
      
  @property
  def errors(self):
    temp, self.__error = self.__error, []
    return temp

  def add_error(self, message):
    self.__error.append(message)