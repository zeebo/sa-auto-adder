from modules.request_object import RequestObject
from modules.sa_profile import SAProfile
from modules.appengine_utilities import cache
from models.user import User
from google.appengine.ext import db
import hashlib, random
import logging

class UserMaker(RequestObject):  
  def do_init(self):
    self.generate_token()
    self.__uid = None
    pass
  
  @property
  def token(self):
    return self.__token
    
  def generate_token(self):
    self.__token = 'sa-auto-adder|%s' % \
                          hashlib.sha1(str(random.random())).hexdigest()[:15]
  
  def valid_data(self, post_data):
    if not self.filled_post_data(post_data):
      self.add_error('fill out the fields')
      return False
    
    if self.username_taken(post_data):
      self.add_error('username taken')
      return False
    
    sa_user = SAProfile(post_data['sa_username'])
    
    if self.sa_uid_taken(sa_user.uid):
      self.add_error('sa user has an account already')
      return False
    
    if not sa_user.has_token(self.__token):
      self.add_error('token not found')
      return False
    
    self.__uid = sa_user.uid
    return True
  
  def filled_post_data(self, post_data):
    #just makes sure theres something in every field
    fields = ['username', 'password', 'sa_username', 'google_wave_address']
    return all([post_data.get(field, '').strip() != '' for field in fields])
  
  def username_taken(self, post_data):
    query = db.Query(User)
    query.filter('username =', post_data['username'])
    return query.get() is not None
      
  def sa_uid_taken(self, sa_uid):
    query = db.Query(User)
    query.filter('sa_uid =', sa_uid)
    return query.get() is not None
  
  def make_user(self, request):
    post_data = dict([(key, request.get(key)) for key in request.arguments()])
    
    if not self.valid_data(post_data):
      return None
    
    new_user = User(
                    username=request.get('username'),
                    password=hashlib.sha1(request.get('password')).hexdigest(),
                    sa_uid=self.__uid,
                    wave_address=request.get('google_wave_address'),
                    )
    new_user.put()
    return new_user




#actions:
  #check if post_data is filled
  #check if username is taken
  #download the profile
  #check the user id
  #check the profile for the token
  