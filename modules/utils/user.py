from google.appengine.ext import db

from model.models import User

from modules.utils import sa_utils
from modules.appengine_utilities import sessions

import hashlib

def check_sa_token(username):
  import logging
  session = sessions.Session()
  
  user_profile = sa_utils.get_profile(username)
  error = None
  if user_profile is None:
    return (False, 'couldn\'t get your sa profile. PANIC', None)
  
  #get the user id out
  user_profile_data = user_profile.read()
  user_id = sa_utils.get_user_id(user_profile_data)
  if user_id is None:
    return (False, 'couldn\'t get your sa user id. PANIC', user_id)
  
  if session.get('token'):
    found_token = session['token'] in user_profile_data
  else:
    found_token = False
  
  if found_token == False:
    error = 'couldn\'t find token in your profile'
    
  return (found_token, error, user_id)

def create_user(post):
  #check all the fields are there
  required_fields = ['sa_username', 'username', 'password', 'google_wave_address']
  if any([post.get(field,'').strip() == '' for field in required_fields]):
    return False, 'fill all the fields out dumbo'
  
  #check if the username is taken
  query = db.Query(User)
  query.filter('username =', post['username'])
  if query.get() is not None:
    return False, 'username taken'
  
  #check the token in the profile
  valid, error, user_id = check_sa_token(post['sa_username'])
  if not valid:
    return False, error
    
  #check the user id
  query = db.Query(User)
  query.filter('sa_uid =', user_id)
  if query.get() is not None:
    return False, 'that sa account has already been activated'
  
    
  pass_hash = hashlib.sha1(post['password']).hexdigest()
  new_user = User(username=post['username'],
                  password=pass_hash,
                  wave_address=post['google_wave_address'],
                  sa_uid=user_id)
  new_user.put()
  
  return True, ''
