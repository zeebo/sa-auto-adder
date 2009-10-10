from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import os, hashlib

class User(db.Model):
  username = db.StringProperty(required=True)
  password = db.StringProperty(required=True)
  
class MainPage(webapp.RequestHandler):
  """Main page handles:
    1. Login and redirect if sucessful (post)
    2. Linking to create page (get)
  """
  def get(self):
    parameters = {'login_failed':False}
    if self.request.cookies.get('username',False):
      parameters['cookie'] = True
      
    path = os.path.join(os.path.dirname(__file__), 'main.html')
    self.response.out.write(template.render(path, parameters))
  
  def post(self):
    query = db.Query(User)
    query.filter('username = ',self.request.get('username'))
    query.filter('password = ',hashlib.sha1(self.request.get('password')).hexdigest())
    if query.get():
      if self.request.get('remember'):
        self.response.headers.add_header(
                'Set-Cookie', 
                'username=%s&hash=%s; expires=Fri, 31-Dec-2020 23:59:59 GMT' \
                  % (self.request.get('username').encode(),
                     hashlib.sha1(self.request.get('username') + self.request.get('password')).hexdigest()))
        self.redirect('/panel/')
    else:
      path = os.path.join(os.path.dirname(__file__), 'main.html')
      self.response.out.write(template.render(path, {'login_failed':True}))


class CreatePage(webapp.RequestHandler):
  """Create page handles:
    1. Creating accounts
  """
  def get(self):
    pass


class PanelPage(webapp.RequestHandler):
  """Panel page handles:
    1. Displaying the waves and stuff
  """
  def get(self):
    pass

class DebugPage(webapp.RequestHandler):
  def get(self):
    zeebo = User(username="zeebo", password=hashlib.sha1('lol').hexdigest())
    zeebo.put()

application = webapp.WSGIApplication(
                                     [
                                        ('/', MainPage),
                                        ('/create', CreatePage),
                                        ('/panel/', PanelPage),
                                        ('/debug', DebugPage)
                                     ],
                                     debug=True)
def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()