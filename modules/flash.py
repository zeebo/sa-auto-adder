from modules.request_object import RequestObject
import logging

class Flash(RequestObject):  
  def do_init(self):
    self.__info = []
    self.__error = []
  
  @property
  def info(self):
    try:
      return self.__info.pop()
    except IndexError:
      return None
  
  @property
  def infos(self):
      temp, self.__info = self.__info, []
      return temp
  
  def add_info(self, message):
    self.__info.append(message)
  
