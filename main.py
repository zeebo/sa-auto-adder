from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from modules import url_list
import pages
import logging

urls = url_list.UrlList({
  'auth':{
    'base_url':('', None),
    'pages':[
      ('Home', '/', pages.LoginPage),
      ('Create Account', '/create', pages.CreatePage),
    ],
    'right-pages':[],
    'actions':[
      ('', '/login', pages.LoginAction),
      ('', '/make_user', pages.CreateAction),
    ],
  },
  'panel':{
    'base_url':('/panel', pages.PanelPage),
    'pages':[
      ('Events', '/events', pages.PanelEventHandler),
      ('Join Waves', '/waves', pages.PanelWavesHandler),
      ('Admin Waves', '/admin', pages.PanelAdminHandler),
      ('Task Queue', '/queue', pages.PanelQueueHandler),
    ],
    'right-pages':[
      ('Logout', '/logout', pages.LogoutAction),
      ('Edit Account', '/edit', pages.EditUserHandler),
    ],
    'actions':[
      ('', '/join/(.*?)', pages.JoinAction),
      ('', '/admin/(.*?)', pages.AdminAction),
      ('', '/leave/(.*?)', pages.LeaveAction),
      ('', '/erase/(.*?)', pages.DeleteEventAction),
    ],
  },
})

application = webapp.WSGIApplication(urls.build_url_list(), debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()