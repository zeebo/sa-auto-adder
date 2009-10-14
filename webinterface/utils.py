from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from google.appengine.ext import db
from model.models import User, WaveletInfo, TaskQueue
from appengine_utilities import sessions
from sa_auth import profile
import utils, datetime, hashlib, random, urllib, settings, logging

def add_participant(wave_id, wavelet_id):
  me = get_stored_user()
  
  query = db.Query(TaskQueue)
  query.filter('wavelet_id =', wavelet_id)
  query.filter('wave_id =', wave_id)
  query.filter('user =', me)
  
  if query.get() is None:
    task = TaskQueue(op_type="add_participant", user=me)
    task.wavelet_id = wavelet_id
    task.wave_id = wave_id
    task.participant_id = me.wave_address
    task.text = "Adding to wavelet_id %s" % wavelet_id
    task.put()

def gets_username(default_value=[]):
  def decorator(method):
    def new(user=None):
      if user is not None:
        return method(user)
    
      user = get_stored_user()
      if user is None:
        return default_value
        
      return method(user)
    return new
  return decorator

@gets_username()
def get_tasks(user):
  query = db.Query(TaskQueue)
  query.filter('user =', user)
  tasks = []
  for task in query:
    tasks.append(task)
  return tasks
  
@gets_username()
def get_waves(user):
  query = db.Query(WaveletInfo)
  query.filter('admin !=', user)
  return make_wavelist_from_waves(query)
  
@gets_username()
def get_admin_waves(user):  
  query = db.Query(WaveletInfo)
  query.filter('admin =', user)
  return make_wavelist_from_waves(query)

def make_wavelist_from_waves(query):
  return_list = []
  
  for wavelet in query:
    wavelet_dict = {}
    properties = wavelet.properties()
    for p in properties:
      wavelet_dict[p] = getattr(wavelet, p)
    wavelet_dict['link'] = "/panel/add/%s/%s/" % (wavelet.wave_id, wavelet.wavelet_id)
    return_list.append(wavelet_dict)
    
  return return_list

def get_stored_username():
  session = sessions.Session()
  return session.get('username', '')

def get_user(username):
  query = db.Query(User)
  query.filter('username =', username)
  return query.get()

def get_stored_user():
  return get_user(get_stored_username())

def get_user_id(profile):
  search_string = '<input type="hidden" name="userid" value="'
  start = profile.find(search_string) + len(search_string)
  end = profile.find('">', start)
  uid = None
  try:
    uid = int(profile[start:end])
  except (IndexError, ValueError):
    pass
  return uid

def check_auth_token(username):
  session = sessions.Session()
  
  if get_stored_user() is not None:
    return (False, 'username is taken', None)
    
  user_profile = profile.get_profile(username)
  error = None
  if user_profile is None:
    return (False, 'couldn\'t get your sa profile. PANIC', None)
  
  #check for sa user id dupes
  user_profile_data = user_profile.read()
  user_id = get_user_id(user_profile_data)
  if user_id is None:
    return (False, 'couldn\'t get your sa user id. PANIC', user_id)
  
  query = db.Query(User)
  query.filter('sa_uid =', user_id)
  if query.get() is not None:
    return (False, 'that sa account has already been activated', user_id)
  

  found_token = session.get('token', user_profile_data+'a') in user_profile_data
  
  if found_token == False:
    error = 'couldn\'t find token in your profile'
  return (found_token, error, user_id)

#this is a dumb function.
def create_user(username, password, wave_address, user_id):
  pass_hash = hashlib.sha1(password).hexdigest()
  new_user = User(username=username, password=pass_hash, wave_address=wave_address, sa_uid=user_id)
  new_user.put()

def create_token():
  session = sessions.Session()
  token = "sa-auto-adder|%s" % hashlib.sha1(str(random.random())).hexdigest()[:15]
  session['token'] = token
  return token

def logout(redirect_to):
  session = sessions.Session()
  response = HttpResponseRedirect(redirect_to)
  query = db.Query(User)
  if "username" in session:
    query.filter("username =",session.get('username', ''))
    user = query.get()
    if user is not None:
      user.cookie_token = ""
      user.put()
  session.delete()
  response['Set-Cookie'] = "token=; expires=Thu, 01-Jan-1970 00:00:01 GMT"
  return response

def login(user, redirect_to, set_cookie):
  session = sessions.Session()
  session['username'] = user.username
  user.last_login = datetime.datetime.now()
  
  if 'redirected_from' in session:
    redirect_to = session.get('redirected_from', '/')
    del session['redirected_from']
  
  response = HttpResponseRedirect(redirect_to)  
  if set_cookie:
    utils.set_cookie_header(response, user)    
  user.put()
  return response
  
def set_cookie_header(response, user):
  cookie_token = hashlib.sha1(str(random.random())).hexdigest()
  cookie_value = "token=%s|%s; expires=Fri, 31-Dec-2020 23:59:59 GMT" % (cookie_token, user.username)
  response['Set-Cookie'] = cookie_value
  user.cookie_token = cookie_token

def require_login(method):
  def new(request, *args, **kwargs):
    session = sessions.Session()
    if 'username' in session:
      return method(request, *args, **kwargs)
    
    if "token" in request.COOKIES:
      if check_cookie_token(request.COOKIES["token"]):
        session['username'] = request.COOKIES["token"].split('|')[1]
        return method(request, *args, **kwargs)
    
    session['redirected_from'] = request.META['PATH_INFO']
    return HttpResponseRedirect('/')
  return new

def authenticate(username, password):
  import hashlib
  query = db.Query(User)
  query.filter('username =', username)
  query.filter('password =', hashlib.sha1(password).hexdigest())
  return query.get()

def check_cookie_token(token):
  cookie_token, username = token.split('|')
  query = db.Query(User)
  query.filter('username =', username)
  query.filter('cookie_token =', cookie_token)
  return query.get() != None

def redirect_if_authenticated(url):
  def redirect(method):
    def new(request, *args, **kwargs):
      session = sessions.Session()
      if 'username' in session:
        return HttpResponseRedirect(url)
      
      if "token" in request.COOKIES:
        if check_cookie_token(request.COOKIES["token"]):
          session['username'] = request.COOKIES["token"].split('|')[1]
          return HttpResponseRedirect(url)
      return method(request, *args, **kwargs)
    return new
  return redirect