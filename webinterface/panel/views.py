from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from modules.utils import auth

@auth.require_login
def panel(request):
  values = {
    #'admin_waves' : utils.get_admin_waves(),
    #'waves' : utils.get_waves(),
    #'tasks' : utils.get_tasks(),
  }
  return render_to_response('panel.html', values)
