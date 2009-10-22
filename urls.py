import pages
import logging
from modules import url_list


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
      ('Events', '/events', pages.PanelHandler),
      ('Join Waves', '/waves', pages.PanelHandler),
      ('Admin Waves', '/admin', pages.PanelHandler),
      ('Task Queue', '/queue', pages.PanelHandler),
    ],
    'right-pages':[
      ('Logout', '/logout', pages.LogoutAction),
      ('Edit Account', '/edit', pages.PanelHandler),
    ],
    'actions':[],
  },
})

