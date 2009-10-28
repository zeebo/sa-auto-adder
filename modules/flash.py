from modules.request_object import RequestObject, updates_session
import logging

class Flash(RequestObject):  
  def do_init(self):
    self.__info = []
    self.__error = []
  
  @property
  @updates_session
  def info(self):
    try:
      return self.__info.pop()
    except IndexError:
      return None
  
  @property
  @updates_session
  def infos(self):
      temp, self.__info = self.__info, []
      return temp
      
  @updates_session
  def add_info(self, message):
    self.__info.append(message)
  
