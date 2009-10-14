# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from google.appengine.ext import db
from model.models import User
from appengine_utilities import sessions
from sa_auth import profile
import utils, datetime

def dump(request):
  return HttpResponse(str(request))

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
  required_fields = ['sa_username', 'username', 'password', 'google_wave_address']
  values = {}
  if request.META["REQUEST_METHOD"] == "POST":
    if all([request.POST.get(field,'').strip() != '' for field in required_fields]):
      valid, error, uid = utils.check_auth_token(request.POST['sa_username'])
      if valid:
        utils.create_user(request.POST['username'], request.POST['password'], request.POST['google_wave_address'], uid)
        values['user_created'] = True
      else:
        values['token_failed'] = True
        values['error'] = error
    else:
      values['token_failed'] = True
      values['error'] = "fill out all the fields dumbo"
  if 'user_created' not in values:
    values['token'] = utils.create_token()
  return render_to_response('create.html', values)

@utils.require_login
def panel(request):
  session = sessions.Session()
  values = {
    'admin_waves' : utils.get_admin_waves(),
    'waves' : utils.get_waves(),
    'tasks' : utils.get_tasks(),
    'username' : utils.get_stored_username(),
  }
  return render_to_response('panel.html', values)

@utils.require_login
def add_participant(request, wave_id, wavelet_id):
  utils.add_participant(wave_id, wavelet_id)
  return HttpResponseRedirect('/panel')