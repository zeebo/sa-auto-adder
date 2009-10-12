import urllib, urllib2, Cookie, sys, logging
from appengine_utilities import cache
try:
    import settings
except:
    import settings_default as settings
  
def valid_cookies(jar):
  valid = False
  if isinstance(jar,Cookie.SimpleCookie):
    for cookie in jar:
      logging.info(str(cookie))
    valid = 'bbpaswword' in jar and 'bbuserid' in jar
  
  return True or valid

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
  jar = Cookie.SimpleCookie()
  jar.load(info['set-cookie'])
  if valid_cookies(jar):
    return jar
  logging.error('Invalid SA username/password. Check sa_settings.py')
  return None

def get_cookies(cached=True):
  picklejar = cache.Cache()
  if 'jar' in picklejar and cached:
    cookies = picklejar['jar']
  else:
    cookies = download_cookies()
  if valid_cookies(cookies):
    picklejar['jar'] = cookies
    return cookies
  return None


def get_profile(username):
  jar = get_cookies()
  
  if jar is None:
    logging.error('Unable to retrieve profile for %s.' % username)
    return None
  
  request = urllib2.Request('http://localhost:8080/display_post')
  #request = urllib2.Request('http://forums.somethingawful.com/member.php?s=&action=getinfo&username=%s' % username)
    
  request.add_header('Set-Cookie', str(jar))
  return urllib2.urlopen(request)


#SA_LOGIN = {
#  "bbpassword": "fa2916dbd4bb084157e5eb88dd4c8c6c",
#  "bbuserid": "62165",
#}

