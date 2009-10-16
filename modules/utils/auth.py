from django.http import HttpResponseRedirect

from google.appengine.ext import db
from model.models import User
from modules.appengine_utilities import sessions

import hashlib, random

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

def get_stored_user():
  session = sessions.Session()
  query = db.Query(User)
  query.filter('username =', session.get('username'))
  return query.get()

def create_token():
  session = sessions.Session()
  session['token'] = "sa-auto-adder|%s" % hashlib.sha1(str(random.random())).hexdigest()[:15]
  return session['token']

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
  import datetime
  session = sessions.Session()
  session['username'] = user.username
  user.last_login = datetime.datetime.now()
  
  if 'redirected_from' in session:
    redirect_to = session.get('redirected_from', '/')
    del session['redirected_from']
  
  response = HttpResponseRedirect(redirect_to)  
  if set_cookie:
    set_cookie_header(response, user)
  user.put()
  return response
  
def set_cookie_header(response, user):
  cookie_token = hashlib.sha1(str(random.random())).hexdigest()
  cookie_value = "token=%s|%s; expires=Fri, 31-Dec-2020 23:59:59 GMT" % (cookie_token, user.username)
  response['Set-Cookie'] = cookie_value
  user.cookie_token = cookie_token

def authenticate(username, password):
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
