from google.appengine.ext import db
from models.user import User
from modules.request_object import RequestObject
import hashlib, random
import logging

class Auth(RequestObject):  
  def do_init(self):
    self.user = None
    self.__token_cache = ''
  
  def login_as(self, user):
    self.user = user
  
  def login(self, username, password):
    query = db.Query(User)
    query.filter('username =', username)
    query.filter('password =', hashlib.sha1(password).hexdigest())
    self.user = query.get()
    if self.user is None:
      raise Exception, "login failed"
  
  def logout(self):
    self.user = None
    self.__token_cache = ''
  
  def check_cookies(self, cookies):
    if 'token' in cookies:
      if self.__token_cache != cookies['token']:
        token, username = cookies['token'].split('|')
        query = db.Query(User)
        query.filter('username', username)
        query.filter('cookie_token', token)
        self.user = query.get()
        if self.user is None:
          raise Exception, 'cookie error'
        self.__token_cache = cookies['token']
  
  def add_cookies(self, response):
    if self.user is not None:
      token = hashlib.sha1(str(random.random())).hexdigest()
      cookie_header = 'token=%s|%s; path=/; ' % (token, self.user.username) + \
                      'expires=Fri, 31-Dec-2020 23:59:59 GMT'
                      
      response.headers.add_header('Set-Cookie', cookie_header)
      self.user.cookie_token = token
      self.user.put()
  
  def del_cookies(self, response):
    response.headers.add_header('Set-Cookie', 'token=; path=/; ' + \
                                      'expires=Thu, 22-Oct-2009 00:00:00 GMT')
