from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from modules.myrequesthandler import AuthenticatedBuilder, NotAuthenticatedBuilder
import logging

#this shit is so meta
NotAuthenticatedHandler = NotAuthenticatedBuilder('/panel')
AuthenticatedHandler = AuthenticatedBuilder('/')

class LoginPage(NotAuthenticatedHandler):
  def get(self):
    self.render('main.html', {'login_failed': self.auth.error})

class LoginAction(NotAuthenticatedHandler):
  def post(self):
    self.auth.login(self.request.get('username'), self.request.get('password'))
    if self.auth.user:
      if self.request.get('remember'):
        self.auth.add_cookies(self.response)
      self.redirect('/panel')
    else:
      self.redirect('/')

class LogoutAction(AuthenticatedHandler):
  def get(self):
    self.auth.logout()
    self.auth.del_cookies(self.response)
    self.redirect('/')

class CreatePage(NotAuthenticatedHandler):
  def get(self):
    self.render('create.html', {})

class CreateAction(NotAuthenticatedHandler):
  def post(self):
    self.render('create.html', {})

    
application = webapp.WSGIApplication([
                                        ('/', LoginPage),
                                        ('/login', LoginAction),
                                        ('/logout', LogoutAction),
                                        ('/create', CreatePage),
                                        ('/make_user', CreateAction),
                                     ], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()