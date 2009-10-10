# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from google.appengine.ext import db
from models import User
from appengine_utilities import sessions
import datetime

def require_login(method):
  def new(request):
    session = sessions.Session()
    if 'username' in session:
      return method(request)

    if "token" in request.COOKIES:
      if check_cookie_token(request.COOKIES["token"]):
        session['username'] = request.COOKIES["token"].split('|')[1]
        return method(request)
        
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
  
def main(request):
  values = {"login_failed":False}
  session = sessions.Session()
  
  if 'username' in session:
    return HttpResponseRedirect('/panel')
    #return redirect("/panel")

  if "token" in request.COOKIES:
    if check_cookie_token(request.COOKIES["token"]):
      session['username'] = request.COOKIES["token"].split('|')[1]
      return HttpResponseRedirect('/panel')
      #return redirect("/panel")
  
  if request.META["REQUEST_METHOD"] == "POST":    
    user = authenticate(request.POST['username'], request.POST['password'])
    if user is not None:
      import hashlib, random, Cookie
      session['username'] = user.username
      user.last_login = datetime.datetime.now()
      response = HttpResponseRedirect('/panel')
      if "remember" in request.POST:
        cookie_token = hashlib.sha1(str(random.random())).hexdigest()
        cookie_value = "token=%s|%s; expires=Fri, 31-Dec-2020 23:59:59 GMT" % (cookie_token, user.username)
        response['Set-Cookie'] = cookie_value
        user.cookie_token = cookie_token
      user.put()
      return response
    else:
      values["login_failed"] = True
  return render_to_response('main.html', values)
  
def logout(request):
  session = sessions.Session()
  response = HttpResponseRedirect("/")
  query = db.Query(User)
  if "username" in session:
    query.filter("username =",session['username'])
    user = query.get()
    if user is not None:
      user.cookie_token = ""
      user.put()
  session.delete()
  response['Set-Cookie'] = "token=; expires=Thu, 01-Jan-1970 00:00:01 GMT"
  return response

def create(request):
  return HttpResponse("create page")

@require_login
def panel(request):
  return HttpResponse("you made it brah <a href=\"/logout\">logout</a>")
  