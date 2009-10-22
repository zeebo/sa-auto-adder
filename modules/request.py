from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from modules.auth import Auth
from modules.user_maker import UserMaker
import os, logging

def NotAuthenticatedBuilder(redirect):
  class NotAuthenticatedHandler(RequestHandler):
    @RequestHandler.all_require_authentication(to_be=False, otherwise=redirect)
    def __new__(): pass
  
  return NotAuthenticatedHandler

def AuthenticatedBuilder(redirect):
  class AuthenticatedHandler(RequestHandler):
    @RequestHandler.all_require_authentication(to_be=True, otherwise=redirect)
    def __new__(): pass

  return AuthenticatedHandler


class RequestHandler(webapp.RequestHandler):
  def __init__(self):
    self.__auth = Auth()
    self.__user_maker = UserMaker()
    self.__template = {}
  
  def set_template_value(self, key, value):
    """These values overwrite anything sent to render"""
    self.__template[key] = value
  
  def del_template_value(self, key):
    if key in self.__template:
      del self.__template[key]
  
  def render(self, filename, values):
    values.update(self.__template)
    path = os.path.join('templates', filename)
    self.response.out.write(template.render(path, values))
  
  def initialize(self, request, response):
    self.auth.check_cookies(request.cookies)
    super(RequestHandler, self).initialize(request, response)
  
  @property
  def auth(self):
    return self.__auth
  
  @property
  def user_maker(self):
    return self.__user_maker
    
  @classmethod
  def sends_request_url(self, method):
    def new_function(self, *args, **kwargs):
      self.set_template_value('path', self.request.path)
      method(self, *args, **kwargs)
    return new_function
    
  #I find the following code to be so cool and meta
  #it gives me butterflies in my stomache. Python <3
  #decorating a function that returns a decorator.
  #SO META
  @classmethod
  def require_authentication(self, to_be, otherwise):
    """Only decorate instance methods"""
    def redirect_decroator(method):
      def new_function(self, *args, **kwargs):
        condition = (self.auth.user is not None) ^ to_be
        if condition:
          #person's auth does not match requirement
          #so redirect
          self.redirect(otherwise)
        else:
          #auth does match the requirement
          method(self, *args, **kwargs)
      return new_function
    return redirect_decroator
  
  @classmethod
  def all_require_authentication(self, to_be, otherwise):
    """Only decorate __new__ with this decorator!"""
    
    def decorator(to_be, otherwise):
      def the_decorator(method):
        method = RequestHandler.require_authentication(to_be, otherwise)(method)
        method = RequestHandler.sends_request_url(method)
        return method
      return the_decorator
    
    def new_decorator(method):
      if method.__name__ != '__new__':
        return method #Dont do anything
      def __new__(cls, *args, **kwargs):
        if not getattr(cls, '__decorated', False):
          cls.get = decorator(to_be=to_be, otherwise=otherwise)(cls.get)
          cls.post = decorator(to_be=to_be, otherwise=otherwise)(cls.post)
          cls.__decorated = True
          cls.otherwise = property(lambda self: otherwise)
        return super(cls.__class__, cls).__new__(cls, *args, **kwargs)
      return __new__
    return new_decorator
