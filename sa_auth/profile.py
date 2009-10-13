import urllib, urllib2, Cookie, sys, logging, pickle
from appengine_utilities import cache
try:
    import settings
except:
    import settings_default as settings
  
def valid_cookies(jar):
  valid = False
  if isinstance(jar,Cookie.BaseCookie):
    valid = 'bbpassword' in jar and 'bbuserid' in jar
  return valid

def download_cookies():
  logging.info('Attempting to log into SA')
  data = {
    "username": settings.SA_INFO['username'],
    "password": settings.SA_INFO['password'],
    "action": 'login',
  }
  try:
      handle = urllib2.urlopen('http://forums.somethingawful.com/account.php', urllib.urlencode(data))
  except urllib2.HTTPError:
    logging.error('Unable to get data from Something Awful')
    return None
  info = handle.info()
  jar = Cookie.BaseCookie()
  logging.info(info['set-cookie'])
  jar.load(info['set-cookie'])
  if valid_cookies(jar):
    return jar
  logging.error('Invalid SA username/password. Check sa_settings.py')
  return None

def get_cookies(cached=True, clear_cache=False):
  picklejar = cache.Cache()
  
  #horrible hack
  in_cache = False
  try:
    throw_away = picklejar['jar']
    in_cache = True
  except KeyError:
    pass
  
  if in_cache and clear_cache:
    del picklejar['jar']
    in_cache = False
  if in_cache and cached:
    jar = pickle.loads(picklejar['jar'])
  else:
    jar = download_cookies()
    if valid_cookies(jar):
      picklejar['jar'] = pickle.dumps(jar)
  
  return jar

def get_profile(username):
  jar = get_cookies()
  
  if jar is None:
    logging.error('Unable to retrieve profile for %s.' % username)
    return None
  
  header = ' '.join(["%s=%s;" % (key, jar[key].value) for key in jar if key[0:2] == 'bb'])
  logging.info(header)
  request = urllib2.Request('http://forums.somethingawful.com/member.php?s=&action=getinfo&username=%s' % username)
  request.add_header('Cookie', header)
  return urllib2.urlopen(request)


#SA_LOGIN = {
#  "bbpassword": "fa2916dbd4bb084157e5eb88dd4c8c6c",
#  "bbuserid": "62165",
#}

