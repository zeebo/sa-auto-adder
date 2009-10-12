# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from google.appengine.ext import db
from models import User
from appengine_utilities import sessions
from sa_auth import profile
import utils, datetime


@utils.redirect_if_authenticated('/panel')
def main(request):
  values = {"login_failed":False}
  if request.META["REQUEST_METHOD"] == "POST":    
    user = utils.authenticate(request.POST['username'], request.POST['password'])
    if user is not None:
      return utils.login(user=user, redirect_to='/panel', set_cookie=("remember" in request.POST))
    else:
      values["login_failed"] = True
  return render_to_response('main.html', values)

@utils.require_login
def logout(request):
  return utils.logout(redirect_to='/')

@utils.redirect_if_authenticated('/panel')
def create(request):
  values = {}
  if request.META["REQUEST_METHOD"] == "POST":
    valid, error = utils.check_auth_token(request.POST['user_id'])
    if valid:
      return HttpResponse("FOUND YOUR TOKEN OMG")
    else:
      values['token_failed'] = True
      values['error'] = error
  values['token'] = utils.create_token()
  return render_to_response('create.html', values)

@utils.require_login
def panel(request):
  return HttpResponse("you made it brah <a href=\"/logout\">logout</a>")
  
def display_post(request):
  return HttpResponse(str(request.POST) + str(request.COOKIES))
  
def send_cookie(request):
  response = HttpResponse("test")
  response['Set-Cookie'] = 'penis=lol;'
  return response

def test_cookie(request):
  return HttpResponse(profile.get_profile("penis"))