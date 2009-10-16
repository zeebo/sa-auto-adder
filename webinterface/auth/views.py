from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from modules.utils import user, auth


@auth.redirect_if_authenticated('/panel')
def main(request):
  values = {"login_failed" : False}
  if request.META["REQUEST_METHOD"] == "POST":    
    user = auth.authenticate(request.POST['username'], request.POST['password'])
    if user is not None:
      return auth.login(user=user, redirect_to='/panel', set_cookie=("remember" in request.POST))
    else:
      values["login_failed"] = True
  return render_to_response('main.html', values)

@auth.require_login
def logout(request):
  return auth.logout(redirect_to='/')

@auth.redirect_if_authenticated('/panel')
def create(request):
  values = {'valid' : False}
  if request.META['REQUEST_METHOD'] == "POST":
    values['valid'], values['error'] = user.create_user(request.POST)
  if not values['valid']:
    values['token'] = auth.create_token()
  return render_to_response('create.html', values)
