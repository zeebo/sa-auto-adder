from modules.request_object import RequestObject
import logging

class Flash(RequestObject):  
  def do_init(self):
    self.__info = []
    self.__error = []
  
  @property
  def info(self):
    try:
      info = self.__info.pop()
      self.update_session()
      return info
    except IndexError:
      return None
  
  @property
  def infos(self):
      temp, self.__info = self.__info, []
      self.update_session()
      return temp
  
  def add_info(self, message):
    self.__info.append(message)
    self.update_session()
  
