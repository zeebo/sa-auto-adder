import pages
urls = {
  'auth':{
    'base_url':('', None),
    'pages':[
      ('Home', '/', pages.LoginPage),
      ('Create User', '/create', pages.CreatePage),
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
      ('Edit Account', '/edit', pages.PanelHandler),
      ('Logout', '/logout', pages.LogoutAction),
    ],
    'actions':[],
  },
}

def build_url_list():
  return_list = []
  for section_key in urls:
    section = urls[section_key]
    base_url = section['base_url'][0]
    if section['base_url'][1] is not None:
      return_list.append(section['base_url'])
    for subsection in ['pages', 'right-pages', 'actions']:
      for page in section[subsection]:
        return_list.append((base_url + page[1], page[2]))
  return return_list