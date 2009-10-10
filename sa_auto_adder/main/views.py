from django.http import HttpResponse
from django.template import Context, loader
from sa_auto_adder.main.models import User
from google.appengine.ext import db
import hashlib

def create(request):
  return HttpResponse("create!")

def panel(request):
  return HttpResponse("panel!")

def login(request):
  return HttpResponse("login!")
  
def main(request):
  context = {'login_failed': False}
  t = loader.get_template('main.html')
  c = Context(context)
  return HttpResponse(t.render(c))