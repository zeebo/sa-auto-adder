# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from google.appengine.ext import db
from models import User
from appengine_utilities import sessions
import utils, datetime


@utils.authenticated_redirect('/panel')
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

def create(request):
  return HttpResponse("create page")

@utils.require_login
def panel(request):
  return HttpResponse("you made it brah <a href=\"/logout\">logout</a>")
  
@utils.require_login
def page_name(request):
  return HttpResponse("SUP")
  