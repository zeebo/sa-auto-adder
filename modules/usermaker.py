from modules.requestobject import RequestObject
import hashlib, random, urllib
import logging

class UserMaker(RequestObject):  
  def do_init(self):
    self.generate_token()
    pass
  
  @property
  def token(self):
    return self.__token
    
  def generate_token(self):
    self.__token = 'sa-auto-adder|%s' % \
                          hashlib.sha1(str(random.random())).hexdigest()[:15]

class SAProfile(object):
  def __init__(self, username):
    self.__username = urllib.quote(username, '')
    self.__profile_data = None
    
  @property
  def profile(self):
    if self.__profile_data is None:
      self.__download_profile_data()
    return self.__profile_data
    
  @property
  def uid(self):
    return 1
  
  def has_token(self, token):
    return token in self.profile
  
  def __download_profile_data(self):
    url = 'http://forums.somethingawful.com/member.php?\
                      s=&action=getinfo&username=%s' % self.username
    
  